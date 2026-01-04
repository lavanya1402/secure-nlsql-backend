import re
from typing import Dict, Any

def nlsql_parse(text: str) -> Dict[str, Any]:
    t = (text or "").strip()
    low = t.lower()

    out: Dict[str, Any] = {
        "operation": "SELECT",
        "table": "customers",
        "filters": {},
        "values": {},
        "raw_text": t,
    }

    # Detect operation
    if any(x in low for x in ["delete", "remove"]):
        out["operation"] = "DELETE"
    elif any(x in low for x in ["update", "change", "set"]):
        out["operation"] = "UPDATE"
    elif any(x in low for x in ["insert", "add", "create", "new customer"]):
        out["operation"] = "INSERT"
    else:
        out["operation"] = "SELECT"

    # Common: city filter like "from Dubai" / "in Dubai"
    m_city = re.search(r"\b(from|in)\s+([a-zA-Z]+)\b", low)
    if m_city:
        out["filters"]["city"] = m_city.group(2).strip().title()

    # INSERT: "Add customer Zoya from Dubai"
    if out["operation"] == "INSERT":
        m = re.search(r"(add|insert|create)\s+(a\s+)?customer\s+([a-zA-Z]+)\s+(from|in)\s+([a-zA-Z]+)", low)
        if m:
            name = m.group(3).strip().title()
            city = m.group(5).strip().title()
            out["values"] = {"name": name, "city": city}
        return out

    # UPDATE: "Update customer Zoya city to Mumbai"
    if out["operation"] == "UPDATE":
        m = re.search(r"(update|change|set)\s+(a\s+)?customer\s+([a-zA-Z]+)\s+city\s+(to|as)\s+([a-zA-Z]+)", low)
        if m:
            name = m.group(3).strip().title()
            city = m.group(5).strip().title()
            out["filters"] = {"name": name}
            out["values"] = {"city": city}
        return out

    # DELETE by name: "Delete customer Zoya"
    if out["operation"] == "DELETE":
        m = re.search(r"(delete|remove)\s+(a\s+)?customer\s+([a-zA-Z]+)", low)
        if m:
            name = m.group(3).strip().title()
            out["filters"] = {"name": name}
            return out

        # DELETE by city: already handled via "from/in <city>" above
        return out

    # SELECT: keep city filter if present
    return out
