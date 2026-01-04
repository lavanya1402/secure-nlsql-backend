from fastapi import APIRouter, Header, HTTPException
from typing import Optional

from src.audit.logger import log_event
from src.mcp.server import mcp_health
from src.mcp.sql_tools import seed_customers, reset_customers

router = APIRouter()

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
    return raw

def _get_role(token: str) -> str:
    role = TOKEN_ROLE_MAP.get(token)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")
    return role

def _require_admin(role: str):
    if role != "admin":
        raise HTTPException(status_code=403, detail="admin_only")

@router.get("/mcp/health")
def mcp_health_api():
    return mcp_health()

@router.post("/admin/seed")
def admin_seed(auth_header: Optional[str] = Header(default=None, alias="Authorization")):
    token = _extract_token(auth_header)
    role = _get_role(token)
    _require_admin(role)

    out = seed_customers()
    log_event({
        "endpoint": "/admin/seed",
        "role": role,
        "operation": "SEED",
        "table": "customers",
        "allowed": True,
        "status": 200,
        "raw_text": "admin seed",
        "result_count": out.get("count"),
    })
    return out

@router.post("/admin/reset")
def admin_reset(auth_header: Optional[str] = Header(default=None, alias="Authorization")):
    token = _extract_token(auth_header)
    role = _get_role(token)
    _require_admin(role)

    out = reset_customers()
    log_event({
        "endpoint": "/admin/reset",
        "role": role,
        "operation": "RESET",
        "table": "customers",
        "allowed": True,
        "status": 200,
        "raw_text": "admin reset",
        "result_count": out.get("count"),
    })
    return out
