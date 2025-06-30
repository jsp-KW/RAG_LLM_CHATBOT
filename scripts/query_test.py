import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json

from chromadb import PersistentClient

# 1. ChromaDB 경로 설정
persist_path = r"C:\Users\jungs\LLM_RAG_PROJECT\chroma_store"


client = PersistentClient(path=persist_path)

# 2. 컬렉션 로드
try:
    collection = client.get_collection("finance_terms")
    print(" 컬렉션 로드 완료")
except Exception as e:
    print(" 컬렉션 로드 실패:", e)
    exit()

# 3. 임베딩 모델 로딩
model = SentenceTransformer("jhgan/ko-sroberta-multitask")

# 4. 테스트용 쿼리들
queries = [
    "중앙은행이 통화를 조절하는 정책은 무엇인가요?",
    "MMF란 무엇인가요?",
    "기준금리란?",
    "환율 변동이란 어떤 개념인가요?",
    "금리평가이론이란?"
]

with open("scripts/data/rag_definitions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for keyword in ["MMF", "기준금리", "통화정책", "환율"]:
    found = [item for item in data if keyword in item["term"]]
    print(f"'{keyword}' 검색 결과: {len(found)}개")
    for item in found:
        print(" -", item["term"])

# 5. 쿼리 수행 및 결과 출력
for query in queries:
    print(f"\n🔍 사용자 질문: {query}")
    query_vector = model.encode(query).tolist()

    try:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=3
        )

        for i, doc in enumerate(results["documents"][0]):
            term = results["metadatas"][0][i].get("term", "N/A")
            score = results["distances"][0][i]
            print(f"\n Top {i+1}")
            print(f" 용어: {term}")
            print(f" 정의: {doc}")
            print(f" 유사도 점수 (낮을수록 유사함): {score:.4f}")

    except Exception as e:
        print(" 검색 중 오류 발생:", e)
