from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from src.agents.nlsql_agent import nlsql_parse
from src.auth.rbac import is_allowed
from src.mcp.router import route_to_tool
from src.audit.logger import log_event, get_audit_logs

router = APIRouter()

class QueryRequest(BaseModel):
    text: str

TOKEN_ROLE_MAP = {
    "viewer-token": "viewer",
    "editor-token": "editor",
    "admin-token": "admin",
}

def _extract_token(auth_header: Optional[str]) -> str:
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")

    raw = auth_header.strip()
    if raw.lower().startswith("bearer "):
        token = raw.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        return token

    return raw  # Swagger convenience

def _get_role_from_token(token: str) -> str:
    role = TOKEN_ROLE_MAP.get(token)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")
    return role

@router.post("/query")
def query(
    req: QueryRequest,
    auth_header: Optional[str] = Header(default=None, alias="Authorization"),
):
    token = _extract_token(auth_header)
    role = _get_role_from_token(token)

    parsed = nlsql_parse(req.text)
    op = parsed.get("operation", "").upper()
    table = parsed.get("table", "")

    allowed = is_allowed(role, op)
    if not allowed:
        log_event({
            "endpoint": "/query",
            "role": role,
            "operation": op,
            "table": table,
            "allowed": False,
            "status": 403,
            "reason": "insufficient_role",
            "raw_text": req.text,
        })
        raise HTTPException(status_code=403, detail="insufficient_role")

    result = route_to_tool(parsed)
    if not result.get("ok"):
        log_event({
            "endpoint": "/query",
            "role": role,
            "operation": op,
            "table": table,
            "allowed": True,
            "status": 400,
            "reason": result.get("error", "tool_error"),
            "raw_text": req.text,
        })
        raise HTTPException(status_code=400, detail=result.get("error", "tool_error"))

    log_event({
        "endpoint": "/query",
        "role": role,
        "operation": op,
        "table": table,
        "allowed": True,
        "status": 200,
        "raw_text": req.text,
        "result_count": result.get("count"),
    })

    return {"ok": True, "role": role, "parsed": parsed, "result": result}


@router.post("/query/structured")
def query_structured(
    req: QueryRequest,
    auth_header: Optional[str] = Header(default=None, alias="Authorization"),
):
    token = _extract_token(auth_header)
    role = _get_role_from_token(token)

    parsed = nlsql_parse(req.text)
    op = parsed.get("operation", "").upper()
    table = parsed.get("table", "")

    allowed = is_allowed(role, op)

    # Denied: return debug JSON + audit log
    if not allowed:
        log_event({
            "endpoint": "/query/structured",
            "role": role,
            "operation": op,
            "table": table,
            "allowed": False,
            "status": 403,
            "reason": "insufficient_role",
            "raw_text": req.text,
        })
        return {
            "ok": False,
            "debug": True,
            "role": role,
            "allowed": False,
            "reason": "insufficient_role",
            "parsed": parsed,
        }

    tool_result = route_to_tool(parsed)

    log_event({
        "endpoint": "/query/structured",
        "role": role,
        "operation": op,
        "table": table,
        "allowed": True,
        "status": 200 if tool_result.get("ok") else 400,
        "reason": None if tool_result.get("ok") else tool_result.get("error", "tool_error"),
        "raw_text": req.text,
        "result_count": tool_result.get("count"),
    })

    return {
        "ok": tool_result.get("ok", False),
        "debug": True,
        "role": role,
        "allowed": True,
        "parsed": parsed,
        "tool_result": tool_result,
    }

@router.get("/audit-log")
def audit_log(limit: int = Query(default=50, ge=1, le=200)):
    return {"ok": True, "count": len(get_audit_logs(limit)), "logs": get_audit_logs(limit)}
