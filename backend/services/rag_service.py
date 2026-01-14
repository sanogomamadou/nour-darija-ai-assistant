import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "nour_knowledge"
EMBEDDING_MODEL = "models/text-embedding-004"

# Global Client
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    print("RAG Service: ChromaDB collection loaded.")
except Exception as e:
    print(f"RAG Service Error: Could not load ChromaDB collection. {e}")
    collection = None

def get_query_embedding(text):
    if not GEMINI_API_KEY:
        return None
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding Error: {e}")
        return None

def retrieve_context(query: str, n_results: int = 2):
    """
    Retrieves relevant context from ChromaDB using Gemini Embeddings.
    """
    if not collection:
        return ""
    
    query_embedding = get_query_embedding(query)
    if not query_embedding:
        return ""

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        # results['documents'] is a list of lists (one list per query)
        documents = results['documents'][0]
        
        if documents:
            context_str = "\n\n".join(documents)
            return context_str
        return ""
        
    except Exception as e:
        print(f"RAG Query Error: {e}")
        return ""
