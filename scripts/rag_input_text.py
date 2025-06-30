import json

# 1. JSON 파일 로딩 (딕셔너리 형태)
with open('scripts/data/merged_definitions.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 2. 딕셔너리를 리스트로 변환
data = [
    {"term": k, "definition": v}
    for k, v in raw_data.items()
]

# 3. "text" 필드 추가 (정의 미완성 제거 포함)
rag_ready = [
    {
        "term": item["term"],
        "definition": item["definition"],
        "text": f"용어: {item['term']}\n정의: {item['definition']}"
    }
    for item in data
    if item["term"] and item["definition"] and "[정의 상세 작성 필요]" not in item["definition"]
]

# 4. JSON과 JSONL 저장
with open('scripts/data/rag_definitions.json', 'w', encoding='utf-8') as f:
    json.dump(rag_ready, f, ensure_ascii=False, indent=2)

with open('scripts/data/rag_definitions.jsonl', 'w', encoding='utf-8') as f:
    for entry in rag_ready:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
