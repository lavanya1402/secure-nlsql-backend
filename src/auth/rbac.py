from typing import Literal

Role = Literal["viewer", "editor", "admin"]

# Permissions map (Project 180 rules)
ROLE_PERMS = {
    "viewer": {"SELECT"},
    "editor": {"SELECT", "INSERT", "UPDATE"},
    "admin": {"SELECT", "INSERT", "UPDATE", "DELETE", "RESET", "SEED"},
}

def is_allowed(role: Role, operation: str) -> bool:
    op = operation.upper().strip()
    return op in ROLE_PERMS.get(role, set())
