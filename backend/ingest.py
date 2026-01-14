import os
import json
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "nour_knowledge"
EMBEDDING_MODEL = "models/text-embedding-004"

def get_embedding(text):
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document",
        title="Knowledge Base Document"
    )
    return result['embedding']

def ingest_data():
    # 1. Initialize ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Reset/Create Collection
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass # Collection didn't exist or couldn't be deleted

    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"Created collection: {COLLECTION_NAME}")

    # 2. Load Data
    data_path = os.path.join("data", "knowledge.json")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"Loading {len(documents)} documents...")

    # 3. Embed and Add to Chroma
    ids = []
    embeddings = []
    metadatas = []
    documents_content = []

    for doc in documents:
        doc_id = doc["id"]
        content = doc["content"]
        category = doc["category"]

        print(f"Embedding document: {doc_id}...")
        emb = get_embedding(content)

        ids.append(doc_id)
        embeddings.append(emb)
        metadatas.append({"category": category})
        documents_content.append(content)

    # Batch add
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents_content
    )
    
    print("Ingestion complete!")
    print(f"Total documents in collection: {collection.count()}")

if __name__ == "__main__":
    ingest_data()
