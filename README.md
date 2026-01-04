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
venv\Scripts\activate
pip install -r requirements.txt
python -m src.db.init_db
uvicorn src.main:app --reload
