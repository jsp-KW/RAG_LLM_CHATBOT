import os
import json
import chromadb
from chromadb.config import Settings

# 저장 경로 절대 지정
persist_path = r"C:\Users\jungs\OneDrive\바탕 화면\LLM기반프로젝트\chroma_db"

# 클라이언트 생성
client = chromadb.Client(Settings(
    persist_directory=persist_path,
    anonymized_telemetry=False
))

# 컬렉션 생성
collection = client.get_or_create_collection("finance_terms")

# 병합된 용어 데이터 로드
with open("scripts/data/merged_definitions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 기존 데이터 제거 (이미 있다면 충돌 방지)
collection.delete(ids=[f"id_{i}" for i in range(len(data))])

# 데이터 삽입
for i, item in enumerate(data):
    collection.add(
        ids=[f"id_{i}"],
        documents=[item["definition"]],
        metadatas=[{"term": item["term"]}]
    )
    print(f"{i+1}/{len(data)} 저장 중...")

# ⚠️ 강제로 저장 트리거 (임시 트릭)
client._impl.persist()

print(" 저장 완료!")
