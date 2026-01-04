from typing import Dict, Any, List

# Fake in-memory "DB"
FAKE_CUSTOMERS: List[Dict[str, Any]] = [
    {"id": 1, "name": "Asha", "city": "Dubai"},
    {"id": 2, "name": "Neha", "city": "Mumbai"},
    {"id": 3, "name": "Ishita", "city": "Dubai"},
]

DEFAULT_CUSTOMERS = [
    {"id": 1, "name": "Asha", "city": "Dubai"},
    {"id": 2, "name": "Neha", "city": "Mumbai"},
    {"id": 3, "name": "Ishita", "city": "Dubai"},
]

def mcp_health() -> Dict[str, Any]:
    return {"ok": True, "service": "mcp-server", "tools": ["db_select", "db_insert", "seed", "reset"]}

def db_select(table: str, filters: Dict[str, Any]) -> Dict[str, Any]:
    if table != "customers":
        return {"ok": False, "error": f"unknown_table: {table}"}

    rows: List[Dict[str, Any]] = FAKE_CUSTOMERS

    for k, v in (filters or {}).items():
        rows = [r for r in rows if str(r.get(k, "")).lower() == str(v).lower()]

    return {"ok": True, "rows": rows, "count": len(rows)}

def db_insert(table: str, values: Dict[str, Any]) -> Dict[str, Any]:
    if table != "customers":
        return {"ok": False, "error": f"unknown_table: {table}"}

    if not values or "name" not in values or "city" not in values:
        return {"ok": False, "error": "missing_fields: name, city required"}

    new_id = max([c["id"] for c in FAKE_CUSTOMERS]) + 1 if FAKE_CUSTOMERS else 1
    row = {"id": new_id, "name": values["name"], "city": values["city"]}
    FAKE_CUSTOMERS.append(row)

    return {"ok": True, "inserted": row}

def reset_db() -> Dict[str, Any]:
    FAKE_CUSTOMERS.clear()
    return {"ok": True, "message": "db reset", "count": 0}

def seed_db() -> Dict[str, Any]:
    FAKE_CUSTOMERS.clear()
    FAKE_CUSTOMERS.extend([dict(x) for x in DEFAULT_CUSTOMERS])
    return {"ok": True, "message": "db seeded", "count": len(FAKE_CUSTOMERS)}
