#!/usr/bin/env python3
"""
Setup script for ESG Chatbot
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/pdf_esg",
        "storage", 
        "qdrant_data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_config():
    """Check if config.env exists and has required values"""
    config_file = Path("config.env")
    
    if not config_file.exists():
        print("❌ config.env not found!")
        print("Please create config.env with your OpenAI API key:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        return False
    
    # Check if OpenAI API key is set
    with open(config_file, 'r') as f:
        content = f.read()
        if "your_openai_api_key_here" in content or "OPENAI_API_KEY=" not in content:
            print("❌ Please set your OpenAI API key in config.env")
            return False
    
    print("✅ Configuration looks good")
    return True

def check_documents():
    """Check if documents exist"""
    doc_path = Path("data/pdf_esg")
    
    if not doc_path.exists():
        print("❌ Document directory not found")
        return False
    
    pdf_files = list(doc_path.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF documents found in data/pdf_esg/")
        print("Please add your ESG documents to this directory")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF documents")
    return True

def check_structure():
    """Check if the new folder structure is in place"""
    required_dirs = [
        "src",
        "src/config",
        "src/processing", 
        "src/storage",
        "src/engine",
        "src/services",
        "src/utils",
        "tests"
    ]
    
    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"❌ Required directory missing: {directory}")
            return False
    
    print("✅ Folder structure is correct")
    return True

def main():
    """Main setup function"""
    print("🚀 ESG Chatbot Setup")
    print("=" * 40)
    
    # Check folder structure
    print("\n📁 Checking folder structure...")
    if not check_structure():
        print("\n❌ Setup incomplete. Please ensure all source files are in place.")
        return False
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Check configuration
    print("\n🔧 Checking configuration...")
    if not check_config():
        print("\n❌ Setup incomplete. Please fix configuration issues.")
        return False
    
    # Check documents
    print("\n📄 Checking documents...")
    check_documents()
    
    print("\n✅ Setup completed!")
    print("\nNext steps:")
    print("1. Run: python tests/test_system.py")
    print("2. Run: python app.py")
    print("3. Initialize the system in the web interface")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 