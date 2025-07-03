import os
import logging
from typing import List, Dict, Any
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter
from llama_index.core.schema import TextNode
from llama_index.readers.file import PDFReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.transformations import TitleExtractor, QuestionsAnsweredExtractor

from src.config.settings import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Advanced document processing with multiple text splitting strategies"""
    
    def __init__(self):
        self.document_path = Path(config.DOCUMENT_PATH)
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        
    def load_documents(self) -> List[Document]:
        """Load documents from the specified directory"""
        logger.info(f"Loading documents from {self.document_path}")
        
        if not self.document_path.exists():
            raise FileNotFoundError(f"Document path {self.document_path} does not exist")
        
        # Use SimpleDirectoryReader for general file types
        reader = SimpleDirectoryReader(
            input_dir=str(self.document_path),
            recursive=True,
            filename_as_id=True,
            required_exts=[".pdf", ".txt", ".md", ".docx"]
        )
        
        documents = reader.load_data()
        logger.info(f"Loaded {len(documents)} documents")
        
        return documents
    
    def create_advanced_text_splitter(self) -> TokenTextSplitter:
        """Create an advanced text splitter with semantic boundaries"""
        return TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separator="\n",
            backup_separators=["\n\n", ". ", "! ", "? ", "; ", ": "]
        )
    
    def create_sentence_splitter(self) -> SentenceSplitter:
        """Create a sentence-based splitter for more natural chunks"""
        return SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separator="\n",
            secondary_chunking_regex_split=[r"\n\n", r"\n", r" ", r""]
        )
    
    def create_ingestion_pipeline(self) -> IngestionPipeline:
        """Create an advanced ingestion pipeline with metadata extraction"""
        transformations = [
            self.create_advanced_text_splitter(),
            TitleExtractor(nodes=5, llm=None),  # Will use default LLM
            QuestionsAnsweredExtractor(questions=3, llm=None)  # Will use default LLM
        ]
        
        return IngestionPipeline(transformations=transformations)
    
    def process_documents(self, documents: List[Document]) -> List[TextNode]:
        """Process documents through the ingestion pipeline"""
        logger.info("Processing documents through ingestion pipeline")
        
        pipeline = self.create_ingestion_pipeline()
        nodes = pipeline.run(documents=documents)
        
        logger.info(f"Created {len(nodes)} nodes from {len(documents)} documents")
        return nodes
    
    def add_metadata_to_nodes(self, nodes: List[TextNode]) -> List[TextNode]:
        """Add additional metadata to nodes for better retrieval"""
        for node in nodes:
            # Add document type metadata
            if hasattr(node, 'metadata') and 'file_name' in node.metadata:
                file_name = node.metadata['file_name']
                file_ext = Path(file_name).suffix.lower()
                node.metadata['document_type'] = file_ext[1:] if file_ext else 'unknown'
                
                # Add ESG category based on filename (you can customize this)
                node.metadata['esg_category'] = self._categorize_esg_document(file_name)
        
        return nodes
    
    def _categorize_esg_document(self, filename: str) -> str:
        """Categorize ESG documents based on filename"""
        filename_lower = filename.lower()
        
        if any(keyword in filename_lower for keyword in ['carbon', 'climate', 'emission']):
            return 'environmental'
        elif any(keyword in filename_lower for keyword in ['social', 'human', 'labor', 'community']):
            return 'social'
        elif any(keyword in filename_lower for keyword in ['governance', 'board', 'compliance', 'risk']):
            return 'governance'
        else:
            return 'general'
    
    def get_document_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """Get statistics about the processed documents"""
        stats = {
            'total_documents': len(documents),
            'total_text_length': sum(len(doc.text) for doc in documents),
            'document_types': {},
            'esg_categories': {}
        }
        
        for doc in documents:
            # Count document types
            file_name = doc.metadata.get('file_name', 'unknown')
            file_ext = Path(file_name).suffix.lower()
            doc_type = file_ext[1:] if file_ext else 'unknown'
            stats['document_types'][doc_type] = stats['document_types'].get(doc_type, 0) + 1
            
            # Count ESG categories
            esg_category = self._categorize_esg_document(file_name)
            stats['esg_categories'][esg_category] = stats['esg_categories'].get(esg_category, 0) + 1
        
        return stats 