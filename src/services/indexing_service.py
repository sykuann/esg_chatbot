import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path

from src.processing.document_processor import DocumentProcessor
from src.storage.vector_store import VectorStoreManager
from src.config.settings import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class IndexingService:
    """Service for orchestrating document indexing process"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        
    def index_documents(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """Main indexing process"""
        start_time = time.time()
        
        try:
            logger.info("Starting document indexing process")
            
            # Check if collection exists and handle force rebuild
            if force_rebuild:
                logger.info("Force rebuild requested, deleting existing collection")
                self.vector_store_manager.delete_collection()
            
            # Create collection if it doesn't exist
            self.vector_store_manager.create_collection()
            
            # Load documents
            logger.info("Loading documents...")
            documents = self.document_processor.load_documents()
            
            if not documents:
                raise ValueError("No documents found to index")
            
            # Get document statistics
            doc_stats = self.document_processor.get_document_stats(documents)
            logger.info(f"Document stats: {doc_stats}")
            
            # Process documents through ingestion pipeline
            logger.info("Processing documents through ingestion pipeline...")
            nodes = self.document_processor.process_documents(documents)
            
            if not nodes:
                raise ValueError("No nodes created from documents")
            
            # Add metadata to nodes
            logger.info("Adding metadata to nodes...")
            nodes = self.document_processor.add_metadata_to_nodes(nodes)
            
            # Create index from nodes
            logger.info("Creating vector store index...")
            index = self.vector_store_manager.create_index_from_nodes(nodes)
            
            # Persist index
            logger.info("Persisting index...")
            self.vector_store_manager.persist_index(index, config.INDEX_STORAGE_PATH)
            
            # Get final statistics
            collection_stats = self.vector_store_manager.get_collection_stats()
            
            # Calculate timing
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Compile results
            results = {
                'success': True,
                'processing_time_seconds': processing_time,
                'documents_processed': len(documents),
                'nodes_created': len(nodes),
                'document_stats': doc_stats,
                'collection_stats': collection_stats,
                'index_path': config.INDEX_STORAGE_PATH,
                'qdrant_path': config.QDRANT_DATA_PATH
            }
            
            logger.info(f"Indexing completed successfully in {processing_time:.2f} seconds")
            logger.info(f"Results: {results}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during indexing: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_time_seconds': time.time() - start_time
            }
    
    def validate_index(self) -> Dict[str, Any]:
        """Validate the existing index"""
        try:
            logger.info("Validating existing index...")
            
            # Check if collection exists
            collection_info = self.vector_store_manager.get_collection_info()
            if not collection_info:
                return {
                    'valid': False,
                    'error': 'No collection found'
                }
            
            # Get collection statistics
            collection_stats = self.vector_store_manager.get_collection_stats()
            
            # Try to load index
            index = self.vector_store_manager.load_index()
            if index is None:
                return {
                    'valid': False,
                    'error': 'Failed to load index'
                }
            
            # Test a simple search
            test_results = self.vector_store_manager.search_similar("ESG sustainability", 1)
            
            validation_result = {
                'valid': True,
                'collection_info': collection_info,
                'collection_stats': collection_stats,
                'test_search_successful': len(test_results) > 0,
                'test_search_results_count': len(test_results)
            }
            
            logger.info("Index validation completed successfully")
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating index: {e}")
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_index_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the indexing system"""
        try:
            # Check document directory
            doc_path = Path(config.DOCUMENT_PATH)
            doc_files = list(doc_path.rglob("*")) if doc_path.exists() else []
            doc_files = [f for f in doc_files if f.is_file() and f.suffix.lower() in ['.pdf', '.txt', '.md', '.docx']]
            
            # Get collection info
            collection_info = self.vector_store_manager.get_collection_info()
            collection_stats = self.vector_store_manager.get_collection_stats()
            
            # Check storage paths
            index_path = Path(config.INDEX_STORAGE_PATH)
            qdrant_path = Path(config.QDRANT_DATA_PATH)
            
            status = {
                'document_directory': {
                    'path': str(doc_path),
                    'exists': doc_path.exists(),
                    'file_count': len(doc_files),
                    'files': [f.name for f in doc_files[:10]]  # Show first 10 files
                },
                'vector_store': {
                    'collection_exists': bool(collection_info),
                    'collection_info': collection_info,
                    'collection_stats': collection_stats
                },
                'storage': {
                    'index_path': {
                        'path': str(index_path),
                        'exists': index_path.exists()
                    },
                    'qdrant_path': {
                        'path': str(qdrant_path),
                        'exists': qdrant_path.exists()
                    }
                },
                'configuration': {
                    'embedding_model': config.EMBEDDING_MODEL,
                    'chunk_size': config.CHUNK_SIZE,
                    'chunk_overlap': config.CHUNK_OVERLAP,
                    'top_k_retrieval': config.TOP_K_RETRIEVAL,
                    'similarity_threshold': config.SIMILARITY_THRESHOLD
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting index status: {e}")
            return {
                'error': str(e)
            }
    
    def cleanup_index(self) -> Dict[str, Any]:
        """Clean up the index and storage"""
        try:
            logger.info("Cleaning up index and storage...")
            
            # Delete collection
            self.vector_store_manager.delete_collection()
            
            # Remove storage directories
            import shutil
            
            index_path = Path(config.INDEX_STORAGE_PATH)
            qdrant_path = Path(config.QDRANT_DATA_PATH)
            
            if index_path.exists():
                shutil.rmtree(index_path)
                logger.info(f"Removed index storage: {index_path}")
            
            if qdrant_path.exists():
                shutil.rmtree(qdrant_path)
                logger.info(f"Removed Qdrant storage: {qdrant_path}")
            
            return {
                'success': True,
                'message': 'Index and storage cleaned up successfully'
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up index: {e}")
            return {
                'success': False,
                'error': str(e)
            } 