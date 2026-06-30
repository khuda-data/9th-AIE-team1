# Backend

KHU:DArchive backend는 사용자의 커리어 기록을 경험 단위로 정리하고 검색 가능한 형태로 저장하는 FastAPI 애플리케이션입니다.

## 구현 중인 사항

- 텍스트 기록 입력 API
- 원문 문서 저장
- 텍스트 정제
- LLM 기반 경험 후보 추출
- 경험 카드 저장
- 경험별 source evidence 연결
- 경험 기반 RAG chunk 생성
- OpenAI embedding 저장
- 경험 완성도 점수 계산
- 부족한 정보에 대한 보완 질문 생성
- 보완 질문 답변 반영
- 답변 반영 후 chunk와 embedding 재생성
- 사용자별 경험 목록/상세 조회
- 사용자별 retrieval search
- OpenAPI export

## 주요 API

- `GET /health`
- `POST /api/documents/text`
- `POST /api/documents/{document_id}/process`
- `GET /api/documents/{document_id}/processing-result`
- `GET /api/experiences`
- `GET /api/experiences/{experience_id}`
- `POST /api/experience-questions/{question_id}/answer`
- `POST /api/retrieval/search`

## 실행

```bash
cd apps/backend
uvicorn app.main:app --reload
```

## 테스트

```bash
cd apps/backend
python -m pytest -q
```

## 설정

환경 변수는 루트의 `.env.example`을 기준으로 합니다.
