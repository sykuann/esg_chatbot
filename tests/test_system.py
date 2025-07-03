#!/usr/bin/env python3
"""
Test script for ESG Chatbot system components
"""

import logging
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.config.settings import config
from src.processing.document_processor import DocumentProcessor
from src.storage.vector_store import VectorStoreManager
from src.services.indexing_service import IndexingService
from src.engine.rag_engine import AdvancedRAGEngine
from src.utils.logger import get_logger

# Configure logging
logger = get_logger(__name__)

def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    try:
        config.validate()
        print("✅ Configuration is valid")
        print(f"   - OpenAI Model: {config.OPENAI_MODEL}")
        print(f"   - Embedding Model: {config.EMBEDDING_MODEL}")
        print(f"   - Document Path: {config.DOCUMENT_PATH}")
        print(f"   - Qdrant Collection: {config.QDRANT_COLLECTION_NAME}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_document_processor():
    """Test document processing"""
    print("\n📄 Testing Document Processor...")
    try:
        processor = DocumentProcessor()
        
        # Check if document path exists
        doc_path = Path(config.DOCUMENT_PATH)
        if not doc_path.exists():
            print(f"❌ Document path does not exist: {doc_path}")
            return False
        
        # Load documents
        documents = processor.load_documents()
        print(f"✅ Loaded {len(documents)} documents")
        
        # Get document stats
        stats = processor.get_document_stats(documents)
        print(f"   - Total text length: {stats['total_text_length']}")
        print(f"   - Document types: {stats['document_types']}")
        print(f"   - ESG categories: {stats['esg_categories']}")
        
        return True
    except Exception as e:
        print(f"❌ Document processor error: {e}")
        return False

def test_vector_store():
    """Test vector store operations"""
    print("\n🗄️ Testing Vector Store...")
    try:
        vector_store = VectorStoreManager()
        
        # Test collection creation
        vector_store.create_collection()
        print("✅ Collection created/verified")
        
        # Get collection info
        info = vector_store.get_collection_info()
        print(f"   - Collection: {info.get('name', 'N/A')}")
        print(f"   - Points: {info.get('points_count', 0)}")
        
        return True
    except Exception as e:
        print(f"❌ Vector store error: {e}")
        return False

def test_indexing_service():
    """Test indexing service"""
    print("\n🔍 Testing Indexing Service...")
    try:
        service = IndexingService()
        
        # Get status
        status = service.get_index_status()
        print("✅ Indexing service initialized")
        print(f"   - Document directory exists: {status['document_directory']['exists']}")
        print(f"   - Collection exists: {status['vector_store']['collection_exists']}")
        
        return True
    except Exception as e:
        print(f"❌ Indexing service error: {e}")
        return False

def test_rag_engine():
    """Test RAG engine"""
    print("\n🤖 Testing RAG Engine...")
    try:
        engine = AdvancedRAGEngine()
        print("✅ RAG engine initialized")
        
        # Get stats
        stats = engine.get_retrieval_stats()
        print(f"   - Collection info: {stats['collection_info']}")
        
        return True
    except Exception as e:
        print(f"❌ RAG engine error: {e}")
        return False

def run_full_test():
    """Run all tests"""
    print("🚀 Starting ESG Chatbot System Tests\n")
    
    tests = [
        ("Configuration", test_config),
        ("Document Processor", test_document_processor),
        ("Vector Store", test_vector_store),
        ("Indexing Service", test_indexing_service),
        ("RAG Engine", test_rag_engine)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the configuration and dependencies.")
        return False

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1) 