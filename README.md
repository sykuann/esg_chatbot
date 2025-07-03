# 🌱 ESG Chatbot - Advanced RAG System

A sophisticated RAG (Retrieval-Augmented Generation) chatbot for ESG (Environmental, Social, and Governance) topics, built with advanced document processing, vector storage, and OpenAI integration.

## 🏗️ Project Structure

```
esg_chatbot/
├── src/                          # Source code
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py          # Environment and app settings
│   ├── processing/              # Document processing
│   │   ├── __init__.py
│   │   └── document_processor.py # Advanced document ingestion
│   ├── storage/                 # Vector storage
│   │   ├── __init__.py
│   │   └── vector_store.py      # Qdrant vector store management
│   ├── engine/                  # RAG engine
│   │   ├── __init__.py
│   │   └── rag_engine.py        # Advanced RAG query engine
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   └── indexing_service.py  # Indexing orchestration
│   └── utils/                   # Utilities
│       ├── __init__.py
│       └── logger.py            # Centralized logging
├── tests/                       # Test files
│   └── test_system.py          # System testing
├── docs/                        # Documentation
├── data/                        # Data directory
│   └── pdf_esg/                # ESG documents
├── storage/                     # Index storage
├── qdrant_data/                # Vector database storage
├── logs/                       # Application logs
├── app.py                      # Main application
├── setup.py                    # Setup script
├── config.env                  # Environment configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd esg_chatbot

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Edit config.env with your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
DOCUMENT_PATH=./data/pdf_esg
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

### 3. Setup

```bash
# Run setup script
python setup.py

# Add your ESG documents to data/pdf_esg/
```

### 4. Testing

```bash
# Run system tests
python tests/test_system.py
```

### 5. Launch

```bash
# Start the application
python app.py
```

## 🔧 Key Features

### **Advanced Document Processing**
- Multiple text splitting strategies (token-based, sentence-based)
- Advanced ingestion pipeline with metadata extraction
- Automatic ESG categorization (Environmental, Social, Governance)
- Support for multiple formats (PDF, TXT, MD, DOCX)

### **Vector Storage**
- Qdrant integration with advanced collection management
- Metadata filtering and similarity search
- Configurable similarity thresholds and top-k retrieval
- Comprehensive statistics and monitoring

### **RAG Engine**
- OpenAI GPT-4 integration for generation
- Custom ESG-focused prompts
- Advanced post-processing with similarity and keyword filtering
- Detailed source attribution and confidence scoring

### **User Interface**
- Modern Gradio interface with system management
- Real-time chat with source document display
- System status monitoring and cleanup tools

## 📋 Configuration

### Environment Variables (`config.env`)

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Vector Database Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=esg_documents

# Document Processing
DOCUMENT_PATH=./data/pdf_esg
INDEX_STORAGE_PATH=./storage
QDRANT_DATA_PATH=./qdrant_data

# Embedding Model
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# RAG Configuration
CHUNK_SIZE=512
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.7

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
```

## 🧪 Testing

Run comprehensive system tests:

```bash
python tests/test_system.py
```

This will test:
- ✅ Configuration loading
- ✅ Document processing
- ✅ Vector store operations
- ✅ Indexing service
- ✅ RAG engine initialization

## 📚 Usage

### Web Interface

1. Start the application: `python app.py`
2. Open the web interface (usually at `http://localhost:7860`)
3. Click "🚀 Initialize System" to set up the RAG system
4. Ask ESG-related questions in the chat interface

### Programmatic Usage

```python
from src.services.indexing_service import IndexingService
from src.engine.rag_engine import AdvancedRAGEngine

# Initialize the system
indexing_service = IndexingService()
indexing_service.index_documents()

# Create RAG engine
rag_engine = AdvancedRAGEngine()
rag_engine.setup_query_engine()

# Query the system
response = rag_engine.query("What are ESG best practices?")
print(response['answer'])
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is set in `config.env`
   - Verify the key has sufficient credits

2. **Document Loading Issues**
   - Check that documents exist in `data/pdf_esg/`
   - Ensure documents are in supported formats

3. **Vector Store Errors**
   - Check Qdrant is running (if using remote)
   - Verify storage permissions for local Qdrant

4. **Import Errors**
   - Ensure you're running from the project root
   - Check that all dependencies are installed

### Debug Mode

Enable debug logging by setting in `config.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 🏗️ Architecture Details

### **Document Processing Pipeline**
1. **Document Loading**: Multi-format document loading
2. **Text Splitting**: Advanced chunking with overlap
3. **Metadata Extraction**: ESG categorization and document typing
4. **Embedding Generation**: Vector embeddings for semantic search

### **RAG Query Flow**
1. **Query Processing**: User question analysis
2. **Vector Search**: Semantic similarity search in Qdrant
3. **Post-processing**: Similarity and keyword filtering
4. **Response Generation**: OpenAI-powered answer synthesis
5. **Source Attribution**: Document source tracking

### **Vector Storage Schema**
- **Collection**: `esg_documents`
- **Vector Size**: 384 (BGE-small-en-v1.5)
- **Distance Metric**: Cosine similarity
- **Metadata**: Document type, ESG category, filename, etc.

## 🔄 Updating Documents

To add new documents:

1. Place new documents in `data/pdf_esg/`
2. Click "Force Rebuild" in the interface
3. Or programmatically: `indexing_service.index_documents(force_rebuild=True)`

## 📈 Performance Optimization

### For Large Document Collections
1. **Increase Chunk Size**: Set `CHUNK_SIZE=1024` for longer context
2. **Adjust Overlap**: Increase `CHUNK_OVERLAP` for better context continuity
3. **Batch Processing**: Process documents in smaller batches
4. **Memory Management**: Monitor memory usage during indexing

### For Better Retrieval
1. **Fine-tune Similarity Threshold**: Adjust `SIMILARITY_THRESHOLD`
2. **Increase Top-K**: Set `TOP_K_RETRIEVAL=10` for more sources
3. **Custom Prompts**: Modify prompts in `src/engine/rag_engine.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LlamaIndex**: Advanced RAG framework
- **Qdrant**: High-performance vector database
- **OpenAI**: GPT-4 language model
- **Gradio**: Web interface framework
- **BGE Embeddings**: High-quality text embeddings

---

**Note**: Make sure to replace `your_openai_api_key_here` in `config.env` with your actual OpenAI API key before running the system.
