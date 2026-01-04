from typing import Dict, Any, List
from datetime import datetime
import uuid

# In-memory audit store (next phase: DB)
_AUDIT_LOGS: List[Dict[str, Any]] = []

def log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stores an audit event with:
    - id, timestamp
    - user role, operation, table
    - allowed/denied
    - status + optional error
    """
    entry = {
        "id": str(uuid.uuid4()),
        "ts": datetime.utcnow().isoformat() + "Z",
        **event
    }
    _AUDIT_LOGS.append(entry)
    return entry

def get_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    return list(reversed(_AUDIT_LOGS))[:limit]
