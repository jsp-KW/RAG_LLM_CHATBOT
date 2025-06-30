import os
import json
from chromadb import PersistentClient
from tqdm import tqdm

from sentence_transformers import SentenceTransformer
#  정제 함수 정의
def is_valid_term(term):
    if not term or len(term.strip()) < 2:
        return False
    if term.strip() in {")", "(", "-", ".", ",", "조", "A", "B"}:
        return False
    return True

# JSON 로드
with open("scripts/data/rag_definitions.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

#  정제 필터링
data = [item for item in raw_data if is_valid_term(item.get("term", ""))]

# Chroma 설정
persist_path = r"C:\Users\jungs\LLM_RAG_PROJECT\chroma_store"
print(f" persist path: {persist_path}")

client = PersistentClient(path=persist_path)
collection_name = "finance_terms"

# 기존 컬렉션 삭제
existing_collections = [col.name for col in client.list_collections()]
if collection_name in existing_collections:
    client.delete_collection(collection_name)
    print(f" 기존 컬렉션 '{collection_name}' 삭제")

# 새 컬렉션 생성
collection = client.get_or_create_collection(name=collection_name)
print(f"새 컬렉션 '{collection_name}' 생성")
model = SentenceTransformer("jhgan/ko-sroberta-multitask")  # 또는 all-MiniLM-L6-v2


# 데이터 삽입 (term + definition 결합)
for i, item in enumerate(tqdm(data, desc=" 저장 중")):
    try:
        term = item["term"]
        definition = item["definition"]
        combined_text = f"{term}: {definition}"
        
        embedding = model.encode(combined_text).tolist()
        safe_id = f"id_{i}"

    
        collection.add(
            ids=[safe_id],
            documents=[combined_text],
            embeddings=[embedding],   #  개선된 부분
            metadatas=[{"term": term}]
        )
    except Exception as e:
        print(f"⚠️ {i+1}번 항목 '{item.get('term', 'N/A')}' 저장 실패: {e}")

print(" ChromaDB 저장 완료")
