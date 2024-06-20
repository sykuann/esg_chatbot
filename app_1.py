import qdrant_client

from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from llama_index.core import load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import set_global_service_context 

import gradio as gr

DOC_PATH = '/Users/simyinkuan/Documents/rag_llama/ollama-llamaindex-mixtral-python-playground/data/pdf_esg'
INDEX_PATH = '//Users/simyinkuan/Documents/rag_llama/ollama-llamaindex-mixtral-python-playground/storage'
Settings.llm = Ollama(model="mistral")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
service_context = ServiceContext.from_defaults(llm=Ollama(model="mistral"),embed_model = embed_model)
set_global_service_context(service_context)

def construct_index(doc_path=DOC_PATH, index_store=INDEX_PATH, use_cache=False):
    client = qdrant_client.QdrantClient(path="./qdrant_data")
    vector_store = QdrantVectorStore(client=client, collection_name="esg")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if use_cache:
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=index_store)
        index = load_index_from_storage(storage_context)  # load index
    else:
        reader = SimpleDirectoryReader(input_dir="/Users/simyinkuan/Documents/rag_llama/ollama-llamaindex-mixtral-python-playground/data/pdf_esg")
        documents = reader.load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(index_store)
    return None

def qabot(input_text, index_store = INDEX_PATH):
  

    storage_context = StorageContext.from_defaults(persist_dir=index_store)

    # Load the data
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response

if __name__ == "__main__":
    construct_index(DOC_PATH, use_cache=False)
    # create_index_retriever_query_engine()
    iface = gr.Interface(fn=qabot, inputs=gr.Textbox(lines=7, label='Enter your query'),
                         outputs="text",
                         title="ESG Chatbot")
    iface.launch(share=True)