import json

# 기존 정의 로딩
with open("term_definitions.json", "r", encoding="utf-8") as f:
    base_dict = json.load(f)

# 새 정의 로딩
with open("filled_missed_terms_definition.json", "r", encoding="utf-8") as f:
    filled_list = json.load(f)

# 병합: term → definition 형태로 추가
for entry in filled_list:
    term = entry["term"]
    definition = entry["definition"]
    if term not in base_dict:
        base_dict[term] = definition

# 저장
with open("merged_definitions.json", "w", encoding="utf-8") as f:
    json.dump(base_dict, f, ensure_ascii=False, indent=2)

print("✅ 병합 완료 → merged_definitions.json 저장됨")
