# check_terms.py
# 용어 잘 정리 되어있는지 json 형식 확인하기 위한 파이썬 파일

import json

with open("scripts/data/term_index.json", "r", encoding="utf-8") as f:
    terms = json.load(f)

print(f"용어 수: {len(terms)}개")
print("-----print -----")
for i, (term, page) in enumerate(terms.items()):
    print(f"{term} -> {page}")
    if i >= 14:
        break
