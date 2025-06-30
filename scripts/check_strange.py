# check_chroma_get.py
from chromadb import PersistentClient

persist_path = r"C:\Users\jungs\LLM_RAG_PROJECT\chroma_store"
client = PersistentClient(path=persist_path)
collection = client.get_collection("finance_terms")

results = collection.get(where={"term": {"$eq": "기준금리"}})

print(" 기준금리 결과:")
print("documents:", results.get("documents"))
print("metadatas:", results.get("metadatas"))
