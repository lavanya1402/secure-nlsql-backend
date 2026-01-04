from typing import Dict, Any
from src.mcp.sql_tools import (
    db_select_customers,
    db_insert_customer,
    db_update_customer,
    db_delete_customers,
)

def route_to_tool(structured_op: Dict[str, Any]) -> Dict[str, Any]:
    op = (structured_op.get("operation") or "").upper()
    table = structured_op.get("table") or ""
    filters = structured_op.get("filters") or {}
    values = structured_op.get("values") or {}

    # Whitelist table
    if table != "customers":
        return {"ok": False, "error": f"unknown_table: {table}"}

    if op == "SELECT":
        return db_select_customers(filters)

    if op == "INSERT":
        return db_insert_customer(values)

    if op == "UPDATE":
        return db_update_customer(filters, values)

    if op == "DELETE":
        return db_delete_customers(filters)

    return {"ok": False, "error": f"unsupported_operation: {op}"}
