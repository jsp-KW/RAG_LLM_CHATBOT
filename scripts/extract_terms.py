# extract_terms.py
# 한국은행 경제금융용어 pdf 에서 금융 용어들과 용어 설명 텍스트를 추출
# 추출한 텍스트 기반으로 rag 기반 챗봇 시스템
import pdfplumber
import re


terms = []

def extract_terms_from_line(line):
    # 용어 + 점들 + 숫자 구조의 반복 패턴 찾기
    pattern = r"([가-힣A-Za-z·/()\-·\s]+)[ㆍ·•・.\s]+(\d+)" # 흔히 알고 있는 점이 아닌 다른 형식의 점이여서 이 부분 해결에 큰 시간이 소요됨...
    matches = re.findall(pattern, line) # 패턴과 매치되는 텍스트 찾기
    for term, page in matches:
        cleaned = term.strip()
        terms.append((cleaned, int(page)))

with pdfplumber.open("scripts/data/2024_경제금융용어 700선.pdf") as pdf:
    for i in range(3, 15): # 2페이지부터 14페이지 단어 목차에 해당하는 부분들 ->  단어와 단어의 의미 설명 부분 페이지 번호 추출을 위해서 
        text = pdf.pages[i].extract_text()
        if not text:
            continue
        lines = text.split('\n')
        for line in lines:
            extract_terms_from_line(line)

# 출력 확인
print(f"\n 총 용어 수: {len(terms)}개")
for t, p in terms[:714]:
    print(f"{t} -> {p}")
