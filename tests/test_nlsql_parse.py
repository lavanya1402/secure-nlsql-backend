import pytest

from src.agents.nlsql_agent import nlsql_parse


@pytest.mark.parametrize(
    "text, operation",
    [
        ("Show customers from Dubai", "SELECT"),
        ("Add customer Zoya from Dubai", "INSERT"),
        ("Update customer Zoya city to Mumbai", "UPDATE"),
        ("Delete customer Zoya", "DELETE"),
        # Words that only contain an operation word must not trigger it.
        ("Show customers created in Dubai", "SELECT"),
        ("Show the customer dataset", "SELECT"),
        ("List customers with an address in Pune", "SELECT"),
    ],
)
def test_operation_detection(text, operation):
    assert nlsql_parse(text)["operation"] == operation


def test_insert_extracts_values():
    out = nlsql_parse("Add customer Zoya from Dubai")
    assert out["values"] == {"name": "Zoya", "city": "Dubai"}


def test_update_extracts_filter_and_values():
    out = nlsql_parse("Update customer Zoya city to Mumbai")
    assert out["filters"] == {"name": "Zoya"}
    assert out["values"] == {"city": "Mumbai"}


def test_select_keeps_city_filter():
    assert nlsql_parse("Show customers in Dubai")["filters"] == {"city": "Dubai"}


def test_empty_text_defaults_to_select():
    assert nlsql_parse("")["operation"] == "SELECT"
