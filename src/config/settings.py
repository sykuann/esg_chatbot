import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv('config.env')

class Config:
    """Configuration class for ESG Chatbot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    
    # Vector Database Configuration
    QDRANT_HOST: str = os.getenv('QDRANT_HOST', 'localhost')
    QDRANT_PORT: int = int(os.getenv('QDRANT_PORT', '6333'))
    QDRANT_COLLECTION_NAME: str = os.getenv('QDRANT_COLLECTION_NAME', 'esg_documents')
    
    # Document Processing
    DOCUMENT_PATH: str = os.getenv('DOCUMENT_PATH', './data/pdf_esg')
    INDEX_STORAGE_PATH: str = os.getenv('INDEX_STORAGE_PATH', './storage')
    QDRANT_DATA_PATH: str = os.getenv('QDRANT_DATA_PATH', './qdrant_data')
    
    # Embedding Model
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')
    
    # RAG Configuration
    CHUNK_SIZE: int = int(os.getenv('CHUNK_SIZE', '512'))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', '50'))
    TOP_K_RETRIEVAL: int = int(os.getenv('TOP_K_RETRIEVAL', '5'))
    SIMILARITY_THRESHOLD: float = float(os.getenv('SIMILARITY_THRESHOLD', '0.7'))
    
    # Application Configuration
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        return True

# Global config instance
config = Config() 