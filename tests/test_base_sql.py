import pytest
from sdtp.sql_base_table import BaseSQLTable

sdql_test_suite = [
    # --- 1. Basic Scalar Comparisons ---
    {
        "SDQL": {"operator": "GT", "column": "age", "value": 21},
        "SQL": "age > ?",
        "Params": [21]
    },
    {
        "SDQL": {"operator": "LE", "column": "account_balance", "value": 5000.50},
        "SQL": "account_balance <= ?",
        "Params": [5000.50]
    },

    # --- 2. Set Operations (IN_LIST) ---
    {
        "SDQL": {"operator": "IN_LIST", "column": "status", "values": ["active", "pending", "archived"]},
        "SQL": "status IN (?, ?, ?)",
        "Params": ["active", "pending", "archived"]
    },
    {
        "SDQL": {"operator": "IN_LIST", "column": "status", "values": ["active"]},
        "SQL": "status = ?",
        "Params": ["active"]
    },
    {
        "SDQL": {"operator": "IN_LIST", "column": "status", "values": []},
        "SQL": "1=0",
        "Params": []
    },

    # --- 3. Compound Logical Operators (ALL, ANY, NONE) ---
    {
        "SDQL": {
            "operator": "ALL",
            "arguments": [
                {"operator": "GT", "column": "age", "value": 18},
                {"operator": "IN_LIST", "column": "role", "values": ["admin", "staff"]}
            ]
        },
        "SQL": "(age > ?) AND (role IN (?, ?))",
        "Params": [18, "admin", "staff"]
    },
    {
        "SDQL": {
            "operator": "ANY",
            "arguments": [
                {"operator": "LT", "column": "score", "value": 50},
                {"operator": "GT", "column": "strikes", "value": 3}
            ]
        },
        "SQL": "(score < ?) OR (strikes > ?)",
        "Params": [50, 3]
    },
    {
        "SDQL": {
            "operator": "NONE",
            "arguments": [
                {"operator": "LE", "column": "age", "value": 12},
                {"operator": "IN_LIST", "column": "status", "values": ["banned"]}
            ]
        },
        "SQL": "NOT ((age <= ?) OR (status = ?))",
        "Params": [12, "banned"]
    },

    # --- 4. Compound Null Fallbacks (Empty Groups) ---
    {
        "SDQL": {"operator": "ALL", "arguments": []},
        "SQL": "1=1",
        "Params": []
    },
    {
        "SDQL": {"operator": "ANY", "arguments": []},
        "SQL": "1=0",
        "Params": []
    },
    {
        "SDQL": {"operator": "NONE", "arguments": []},
        "SQL": "1=1",
        "Params": []
    }
]

# Copy and paste this directly above or below your test suite array
mock_test_table_schema =  [
    {"name": "age", "type": "number"},
    {"name": "account_balance", "type": "number"},
    {"name": "status", "type": "string"},
    {"name": "role", "type": "string"},
    {"name": "score", "type": "number"},
    {"name": "strikes", "type": "number"},
    {"name": "created_year", "type": "number"}
]

def test_compile_filter_spec():
    sql_table = BaseSQLTable(mock_test_table_schema, "test")
    for test in sdql_test_suite:
        where_clause, params = sql_table._compile_filter_spec(test["SDQL"])
        assert where_clause == test["SQL"]
        assert params == test["Params"]