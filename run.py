#!/usr/bin/env python3
"""
Simple run script for ESG Chatbot
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    # Import and run the main application
    from app import create_interface
    
    print("🚀 Starting ESG Chatbot...")
    print("📖 Make sure you have:")
    print("   - Set your OpenAI API key in config.env")
    print("   - Added ESG documents to data/pdf_esg/")
    print("   - Run 'python setup.py' if this is your first time")
    print()
    
    interface = create_interface()
    interface.launch(share=True) 