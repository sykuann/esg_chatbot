import logging
import json
import gradio as gr

from src.config.settings import config
from src.services.indexing_service import IndexingService
from src.engine.rag_engine import AdvancedRAGEngine
from src.utils.logger import get_logger

# Configure logging
logger = get_logger(__name__)

class ESGChatbot:
    def __init__(self):
        self.indexing_service = IndexingService()
        self.rag_engine = AdvancedRAGEngine()
        self.is_initialized = False
        
    def initialize_system(self, force_rebuild=False):
        try:
            logger.info("Initializing ESG Chatbot system...")
            config.validate()
            
            validation_result = self.indexing_service.validate_index()
            if not validation_result.get('valid', False) or force_rebuild:
                indexing_result = self.indexing_service.index_documents(force_rebuild=force_rebuild)
                if not indexing_result.get('success', False):
                    return f"Failed to create index: {indexing_result.get('error', 'Unknown error')}"
            
            self.rag_engine.setup_query_engine(force_rebuild=force_rebuild)
            self.is_initialized = True
            return "✅ ESG Chatbot initialized successfully!"
            
        except Exception as e:
            return f"❌ Failed to initialize system: {str(e)}"
    
    def query_chatbot(self, question):
        if not self.is_initialized:
            return "❌ System not initialized. Please initialize the system first."
        
        if not question.strip():
            return "❌ Please enter a question."
        
        try:
            response = self.rag_engine.query(question)
            answer = response.get('answer', 'No answer generated')
            source_docs = response.get('source_documents', [])
            
            result = f"🤖 **Answer:**\n{answer}\n\n"
            
            if source_docs:
                result += "📚 **Sources:**\n"
                for i, doc in enumerate(source_docs[:3], 1):
                    metadata = doc.get('metadata', {})
                    filename = metadata.get('file_name', 'Unknown')
                    result += f"{i}. **{filename}**\n"
                    result += f"   Excerpt: {doc.get('text', '')[:200]}...\n\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"
    
    def get_system_status(self):
        try:
            status = self.indexing_service.get_index_status()
            status['initialized'] = self.is_initialized
            return json.dumps(status, indent=2)
        except Exception as e:
            return f"Error getting status: {str(e)}"
    
    def cleanup_system(self):
        try:
            result = self.indexing_service.cleanup_index()
            self.is_initialized = False
            return "✅ System cleaned up successfully." if result.get('success', False) else f"❌ Failed to clean up: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"❌ Error cleaning up: {str(e)}"

def create_interface():
    chatbot = ESGChatbot()
    
    with gr.Blocks(title="ESG Chatbot") as interface:
        gr.Markdown("# 🌱 ESG Chatbot")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### System Control")
                init_btn = gr.Button("🚀 Initialize System", variant="primary")
                force_rebuild = gr.Checkbox(label="Force Rebuild", value=False)
                status_btn = gr.Button("📊 Status")
                cleanup_btn = gr.Button("🧹 Cleanup", variant="stop")
                status_output = gr.Textbox(label="Status", lines=5)
            
            with gr.Column(scale=2):
                gr.Markdown("### Chat")
                chat_input = gr.Textbox(label="Question", placeholder="Ask about ESG topics...", lines=3)
                chat_btn = gr.Button("💬 Ask", variant="primary")
                chat_output = gr.Textbox(label="Response", lines=15)
        
        # Event handlers
        init_btn.click(fn=chatbot.initialize_system, inputs=[force_rebuild], outputs=[status_output])
        status_btn.click(fn=chatbot.get_system_status, outputs=[status_output])
        cleanup_btn.click(fn=chatbot.cleanup_system, outputs=[status_output])
        chat_btn.click(fn=chatbot.query_chatbot, inputs=[chat_input], outputs=[chat_output])
        chat_input.submit(fn=chatbot.query_chatbot, inputs=[chat_input], outputs=[chat_output])
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True) 