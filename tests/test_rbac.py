import pytest

from src.auth.rbac import is_allowed


@pytest.mark.parametrize(
    "role, operation, allowed",
    [
        ("viewer", "SELECT", True),
        ("viewer", "INSERT", False),
        ("viewer", "DELETE", False),
        ("editor", "UPDATE", True),
        ("editor", "DELETE", False),
        ("admin", "DELETE", True),
        ("admin", "reset", True),
        ("unknown", "SELECT", False),
    ],
)
def test_role_permissions(role, operation, allowed):
    assert is_allowed(role, operation) is allowed
