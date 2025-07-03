# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+
- OpenAI API key
- ESG documents (PDFs, etc.)

## 1. Setup (One-time)

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Edit config.env with your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

## 2. Add Documents
Place your ESG documents in `data/pdf_esg/`:
- PDF files
- Text files
- Markdown files
- Word documents

## 3. Test System
```bash
python tests/test_system.py
```

## 4. Run Application
```bash
# Option 1: Using run script
python run.py

# Option 2: Direct execution
python app.py
```

## 5. Use the Interface
1. Open the web interface (usually `http://localhost:7860`)
2. Click "🚀 Initialize System"
3. Wait for indexing to complete
4. Start asking ESG questions!

## Example Questions
- "What are the key environmental factors in ESG reporting?"
- "How do companies measure social impact?"
- "What governance practices are recommended for sustainability?"

## Troubleshooting
- **API Key Error**: Check `config.env` has your OpenAI API key
- **No Documents**: Ensure files are in `data/pdf_esg/`
- **Import Errors**: Run from project root directory
- **Memory Issues**: Reduce `CHUNK_SIZE` in `config.env`

## Need Help?
- Check the full `README.md` for detailed documentation
- Run `python tests/test_system.py` to diagnose issues
- Ensure all dependencies are installed: `pip install -r requirements.txt` 