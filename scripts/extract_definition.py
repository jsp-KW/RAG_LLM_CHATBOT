# to do list
# 설명이 한 슬라이드에만 존재하면 모르겠는데,
# 설명이 다른 슬라이드로 넘어가서까지 존재하는 경우에 
# 설명 추출할 시 설명이 완전 추출되지 않고 끊기는 문제 발생
import json
import re
import pdfplumber
from collections import defaultdict
import csv

# 설명 길이 제한 해제 기준
MIN_DESC_LENGTH = 20  # 이전에는 이보다 짧으면 제거했음

#  1. 용어 사전 불러오기
with open("scripts/data/term_index.json", "r", encoding="utf-8") as f:
    term_page_dict = json.load(f)

#  2. 페이지별 용어 분배
page_to_terms = defaultdict(list)
for term, page in term_page_dict.items():
    page_to_terms[int(page)].append(term)

#  3. PDF 슬라이드 vs 하단 페이지 번호 차이
PAGE_OFFSET = 16

#  4. 용어 위치 찾기 함수
def find_term_index(term, text):
    pattern = rf"(^|\n)\s*(■?\s*{re.escape(term)})(\s*[\n:])"
    match = re.search(pattern, text)
    return match.start() if match else -1

#  5. 텍스트 정제
def clean_text(text):
    text = re.sub(r'-\n\s*', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

#  6. 본문 추출
term_definitions = {}
missed_terms = []

with pdfplumber.open("scripts/data/2024_경제금융용어 700선.pdf") as pdf:
    for page_num, terms_on_page in page_to_terms.items():
        pdf_index = page_num + PAGE_OFFSET - 1
        if pdf_index >= len(pdf.pages):
            print(f"[ 텍스트 없음] 페이지 {pdf_index+1}")
            continue

        #  현재 페이지 + 다음 페이지 합쳐서 처리
        text = pdf.pages[pdf_index].extract_text() or ""
        if pdf_index + 1 < len(pdf.pages):
            text += "\n" + (pdf.pages[pdf_index + 1].extract_text() or "")
        text = clean_text(text)

        #  용어 순서대로 정렬
        term_positions = {term: find_term_index(term, text) for term in terms_on_page}
        found_terms = sorted(
            [(term, pos) for term, pos in term_positions.items() if pos != -1],
            key=lambda x: x[1]
        )

        for idx, (term, start) in enumerate(found_terms):
            end = found_terms[idx + 1][1] if idx + 1 < len(found_terms) else len(text)
            if start >= end:
                print(f"[ 범위 오류] '{term}' (start ≥ end) 페이지 {page_num}")
                missed_terms.append((term, page_num))
                continue

            content = text[start:end].strip()
            rel_idx = content.find("연관검색어")
            if rel_idx != -1:
                content = content[:rel_idx].strip()

            if len(content) < MIN_DESC_LENGTH:
                print(f"[ 너무 짧음] '{term}' 페이지 {page_num}")
                missed_terms.append((term, page_num))
                continue

            term_definitions[term] = content

        # 발견되지 않은 용어들
        for term in terms_on_page:
            if term not in term_definitions:
                if (term, page_num) not in missed_terms:
                    missed_terms.append((term, page_num))
                print(f"[미발견 용어] '{term}' (페이지 {page_num})")

#  7. 저장
with open("scripts/data/term_definitions.json", "w", encoding="utf-8") as f:
    json.dump(term_definitions, f, ensure_ascii=False, indent=2)

with open("scripts/data/missed_terms.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Term", "Page"])
    writer.writerows(missed_terms)

#  8. 샘플 출력
print(f"\n총 추출된 용어 수: {len(term_definitions)}개")
print(f" 누락된 용어 수: {len(missed_terms)}개 (missed_terms.csv에 저장됨)")
for i, (term, desc) in enumerate(term_definitions.items()):
    print(f"\n[{i+1}] {term}:\n{desc[:200]}...")
    if i >= 4:
        break
