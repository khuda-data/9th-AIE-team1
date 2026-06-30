# 로컬 개발 및 실행

## 요구 사항

- Python 3.11+
- Docker
- PostgreSQL
- pgvector

## 의존성 설치

```bash
cd apps/backend
python -m pip install -e ".[test]"
```

## 환경 변수

루트의 `.env.example`을 기준으로 설정합니다.

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/experience_vault
LLM_PROVIDER=fake
LLM_MODEL=gpt-4.1-mini
EMBEDDING_PROVIDER=fake
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
OPENAI_API_KEY=
```

로컬 테스트는 기본적으로 fake LLM과 fake embedding을 사용합니다.

OpenAI 연동을 사용하려면 다음 값을 설정합니다.

```env
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=...
```

LLM과 embedding 호출은 LangChain의 `langchain-openai` wrapper를 사용합니다.

## 로컬 DB 실행

```bash
docker compose up -d postgres
```

## 마이그레이션

```bash
cd apps/backend
alembic upgrade head
```

## 서버 실행

```bash
cd apps/backend
uvicorn app.main:app --reload
```

서버 실행 후 다음 주소를 사용할 수 있습니다.

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
- `http://localhost:8000/openapi.json`

## 테스트

```bash
cd apps/backend
python -m pytest -q
```

## OpenAPI Export

```bash
python scripts/export_openapi.py
```

생성 파일:

- `docs/openapi/openapi.json`
- `docs/openapi/openapi.yaml`
