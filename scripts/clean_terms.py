# 단어 이상치 제거 및 정리 
# clean_terms.py

from extract_terms import terms  # 혹은 import 방식에 맞게 수정
import re
cleaned_terms = {}
for term, page in terms:
    if len(term.strip()) <= 1:
        continue
    if re.search(r'[가-힣A-Za-z]', term) is None:
        continue
    if term.strip() in cleaned_terms:
        continue
    cleaned_terms[term.strip()] = page

# 저장 예시
import json
with open("scripts/data/term_index.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_terms, f, ensure_ascii=False, indent=2)
