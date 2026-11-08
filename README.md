# Secure NLSQL Backend

Enterprise-style backend system that converts natural language queries into **safe, role-controlled SQL operations**.

## Features
- Natural Language → Structured DB Ops (SELECT / INSERT / UPDATE / DELETE)
- Role-Based Access Control (Viewer / Editor / Admin)
- MCP Tool Router
- Audit Logging (Allowed + Denied)
- FastAPI REST backend
- SQLite (can be swapped to Postgres)

## Roles
| Role   | Permissions |
|-------|-------------|
| Viewer | SELECT |
| Editor | SELECT, INSERT, UPDATE |
| Admin | ALL (incl. DELETE, RESET, SEED) |

## Run Locally
```bash
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m src.db.init_db
uvicorn src.main:app --reload

## Configuration

Copy `.env.example` to `.env` and set your values. `.env` is ignored by git.

## Demo access tokens

The API accepts three demo bearer tokens, one per role: `viewer-token`, `editor-token` and `admin-token`. They exist so the role checks can be tried quickly in Swagger (`/docs`). Replace them with signed JWTs before any real deployment.

| Role | Allowed operations |
|---|---|
| viewer | SELECT |
| editor | SELECT, INSERT, UPDATE |
| admin | SELECT, INSERT, UPDATE, DELETE, RESET, SEED |

## Tests

```bash
pip install pytest
python -m pytest -q tests
```

Tests cover the role permissions and the natural-language parser, including words that must not trigger a write (for example "created" must not be read as "create").

## License

MIT, see [LICENSE](LICENSE). Built by [Lavanya Srivastava](https://github.com/lavanya1402), Lavanya AI Consultancy.
