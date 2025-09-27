# Backend
All requirements and project information are presented at [`pyproject.toml`](pyproject.toml)
Add `.env` file with variable `DATABASE_URL` or set it manually in [`database`](src/database/core.py)

To run the project using [`uv`](https://docs.astral.sh/uv/)
```bash
uv run fastapi dev ./src/main.py
```

Required libraries:
[`FastAPI`](https://fastapi.tiangolo.com/) + [`uvicorn`](https://uvicorn.dev/) + [`starlette`](https://www.starlette.dev/) + [`pydantic`](https://docs.pydantic.dev/latest/)

Or use standard fastapi libraries
```bash
uv add fastapi[standard]
```
Postgres driver (psycopg2)
```bash
uv add psycopg2
```