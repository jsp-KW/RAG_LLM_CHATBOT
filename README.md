# RAG 기반 금융 투자 용어 챗봇 프로젝트 진행 현황 

![image](https://github.com/user-attachments/assets/9885b932-41d0-44b9-aaf5-0c239340c16f)

## 기술 스택

### 임베딩 모델  
- 모델명: `jhgan/ko-sroberta-multitask`  
- 설명: 한국어에 특화된 다중 작업용 RoBERTa 기반 SentenceTransformer 모델로, 문장 및 문서 임베딩에 최적화되어 있습니다.  
- 용도: 사용자의 질의(query)와 금융 용어 정의 문서 간의 의미 기반 유사도 검색을 위해 임베딩 벡터를 생성합니다.  
- 장점: 한국어 자연어처리에 강하며, 문맥 이해가 우수해 금융 전문 용어 간 관계 파악에 효과적입니다.  
- 프레임워크: PyTorch 기반 SentenceTransformers 라이브러리 사용  

### LLM (대형언어모델)  
- 모델명: `MiniMaxAI/MiniMax-M1-80k` (Hugging Face Inference API)  
- 설명: 한국어 중심의 고용량 사전학습 대형언어모델(LLM)으로, 자연스러운 한국어 문장 생성과 요약, 쉬운 설명 제공에 적합합니다.  
- 용도:  
  - 금융 용어 설명을 20대 사회초년생도 이해할 수 있도록 쉬운 말로 재작성  
  - 용어 설명 요약 기능  
  - 누락된 용어에 대한 정의 생성 보완  
- 운영 환경: Hugging Face Inference API를 통한 원격 호출, API 토큰 방식 인증  
- 특징:  
  - 대화형 챗봇에 적합하도록 시스템 프롬프트가 친절한 금융 선생님 역할로 세팅되어 있음  
  - 외래어, 영어 단어 최소화 및 쉬운 한국어 위주 설명 지향  

### 기타 핵심 기술  
- 벡터 DB: ChromaDB (PersistentClient)  
  - 임베딩 벡터 저장 및 유사도 기반 검색 처리  
  - 로컬 디스크 기반 영속 저장 지원  
- 웹 프론트엔드: Streamlit  
  - 실시간 쿼리 입력 및 결과 표시  
  - 요약 및 쉬운 설명 기능 확장 UI 구현  
- Python 라이브러리:  
  - sentence-transformers (임베딩 생성)  
  - huggingface_hub (LLM API 클라이언트)  
  - pdfplumber (PDF 용어 및 정의 추출)  
  - re (정규표현식 기반 텍스트 정제)  


---

## 프로젝트 개요  
- 목적: 경제·금융 용어 JSON 데이터를 기반으로 RAG + LLM 구조로 질의응답 제공  
- 구성 요소:  
  - `rag_definitions.json`: 금융 용어 + 설명 정제된 JSON  
  - ChromaDB: 벡터 DB로 활용  
  - `ko-sroberta-multitask`: 질의-문서 임베딩용 SentenceTransformer  
  - Streamlit: 웹 GUI 프론트엔드  


---

## 주요 문제 및 해결 과정  

### 1. Python 버전 문제  
- ChromaDB는 내부적으로 sqlite3 >= 3.35.0 이상 요구  
- VS Code 인터프리터는 Python 3.10.11 (rag_bot)이었으나, CLI에서는 3.8.5 실행으로 오류 발생  
- Streamlit 실행 시 `RuntimeError: unsupported sqlite3 version` 발생  

  해결:  
- Python 3.10 전용 가상환경(rag310) 새로 생성  
- 필요한 패키지(`streamlit`, `chromadb`, `sentence-transformers`, `tqdm`)만 재설치 후 실행  


---

### 2. 단축어 질의 결과 이상 현상  
- 예: "인플레이션이 뭐야" → 관련 용어 정상 출력  
- "PER", "PBR" 등 단일 단축어 → 엉뚱한 결과, 무관 용어 반환  

원인 분석:  
- 단축어는 임베딩 차원에서 문맥 정보 부족  
- 문장형 쿼리 대비 의미 벡터 부정확  
- 벡터 DB 내 유사도 점수 미흡  

해결 방향 제안:  
- 쿼리 전처리: 단축어일 경우 "PER 이란 무엇인가요?" 형태로 자동 변환  
- term 필드 직접 비교 + definition 임베딩 결합한 하이브리드 검색 도입  


---

## 현재 상태  
- `query_web.py` GUI 정상 실행  
-  벡터 검색 기능 동작 확인  
-  임베딩 기반 유사도 정렬 정상 작동  
-  Hugging face LLM MODEL 크레딧 이슈로 텍스트 비교만 현재는 수행중  
-  LLM 사용 여부를 고려하여 리팩토링 완료  

   단축어 키워드 검색 개선 필요 (전처리 or 하이브리드 방식 고려 중)  


---

## 향후 계획  
- 단축어 및 구문 처리 고도화  
- LLM 크레딧 문제 해결 후 요약 및 쉬운 설명 기능 완전 활성화  
- 정의 누락 보완 자동화 및 정제 작업 추가  
- UI/UX 개선 및 실시간 채팅형 인터페이스 도입 검토  
