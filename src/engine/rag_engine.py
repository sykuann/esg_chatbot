import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from llama_index.core import VectorStoreIndex, ServiceContext, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor, KeywordNodePostprocessor
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.prompts import PromptTemplate

from src.config.settings import config
from src.storage.vector_store import VectorStoreManager

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class AdvancedRAGEngine:
    """Advanced RAG engine with multiple retrieval strategies"""
    
    def __init__(self):
        self.vector_store_manager = VectorStoreManager()
        self.embedding_model = HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL)
        
        # Initialize OpenAI LLM
        self.llm = OpenAI(
            model=config.OPENAI_MODEL,
            api_key=config.OPENAI_API_KEY,
            temperature=0.1
        )
        
        # Set global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embedding_model
        
        # Create service context
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embedding_model
        )
        
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine: Optional[RetrieverQueryEngine] = None
        
    def load_or_create_index(self, force_rebuild: bool = False) -> VectorStoreIndex:
        """Load existing index or create a new one"""
        if not force_rebuild:
            self.index = self.vector_store_manager.load_index()
        
        if self.index is None:
            logger.info("No existing index found, creating new one...")
            # This will be populated by the indexing process
            self.index = self.vector_store_manager.load_index()
        
        return self.index
    
    def create_advanced_retriever(self, index: VectorStoreIndex) -> VectorIndexRetriever:
        """Create an advanced retriever with multiple strategies"""
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=config.TOP_K_RETRIEVAL,
            service_context=self.service_context
        )
        
        return retriever
    
    def create_response_synthesizer(self):
        """Create a response synthesizer with custom prompt"""
        # Custom ESG-focused prompt
        custom_prompt = PromptTemplate(
            "You are an ESG (Environmental, Social, and Governance) expert assistant. "
            "Based on the provided context, answer the user's question about ESG topics. "
            "Always provide accurate, well-reasoned responses based on the context. "
            "If the context doesn't contain enough information to answer the question, "
            "say so clearly.\n\n"
            "Context:\n{context_str}\n\n"
            "Question: {query_str}\n\n"
            "Answer: "
        )
        
        return get_response_synthesizer(
            service_context=self.service_context,
            response_mode="compact",
            text_qa_template=custom_prompt
        )
    
    def create_advanced_query_engine(self, index: VectorStoreIndex) -> RetrieverQueryEngine:
        """Create an advanced query engine with post-processing"""
        # Create retriever
        retriever = self.create_advanced_retriever(index)
        
        # Create post-processors
        similarity_postprocessor = SimilarityPostprocessor(
            similarity_cutoff=config.SIMILARITY_THRESHOLD
        )
        
        keyword_postprocessor = KeywordNodePostprocessor(
            required_keywords=["ESG", "sustainability", "environmental", "social", "governance"],
            exclude_keywords=["unrelated", "irrelevant"]
        )
        
        # Create response synthesizer
        response_synthesizer = self.create_response_synthesizer()
        
        # Create query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[similarity_postprocessor]
        )
        
        return query_engine
    
    def setup_query_engine(self, force_rebuild: bool = False) -> None:
        """Setup the complete query engine"""
        # Load or create index
        index = self.load_or_create_index(force_rebuild)
        
        if index is None:
            raise ValueError("Failed to load or create index")
        
        # Create query engine
        self.query_engine = self.create_advanced_query_engine(index)
        logger.info("Advanced query engine setup completed")
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with advanced processing"""
        if self.query_engine is None:
            raise ValueError("Query engine not initialized. Call setup_query_engine() first.")
        
        try:
            logger.info(f"Processing query: {question}")
            
            # Get response from query engine
            response = self.query_engine.query(question)
            
            # Get source documents
            source_documents = []
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    source_docs = {
                        'text': node.text,
                        'metadata': node.metadata,
                        'score': getattr(node, 'score', None)
                    }
                    source_documents.append(source_docs)
            
            # Format response
            result = {
                'answer': response.response,
                'source_documents': source_documents,
                'query': question,
                'confidence': getattr(response, 'confidence', None)
            }
            
            logger.info("Query processed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'answer': f"Sorry, I encountered an error while processing your question: {str(e)}",
                'source_documents': [],
                'query': question,
                'error': str(e)
            }
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """Get statistics about the retrieval system"""
        stats = {
            'collection_info': self.vector_store_manager.get_collection_info(),
            'collection_stats': self.vector_store_manager.get_collection_stats(),
            'config': {
                'top_k_retrieval': config.TOP_K_RETRIEVAL,
                'similarity_threshold': config.SIMILARITY_THRESHOLD,
                'embedding_model': config.EMBEDDING_MODEL,
                'llm_model': config.OPENAI_MODEL
            }
        }
        
        return stats
    
    def search_similar_documents(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar documents without generating a response"""
        return self.vector_store_manager.search_similar(query, top_k)
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        try:
            result = self.vector_store_manager.client.retrieve(
                collection_name=self.vector_store_manager.collection_name,
                ids=[doc_id],
                with_payload=True
            )
            
            if result:
                point = result[0]
                return {
                    'id': point.id,
                    'payload': point.payload,
                    'text': point.payload.get('text', ''),
                    'metadata': point.payload.get('metadata', {})
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving document {doc_id}: {e}")
            return None 