import pytest

from sdtp import ContainerTable, InvalidDataException, RowTable
from sdtp.sdtp_schema import (
    ContainerTableSchema,
    RemoteTableSchema,
    RowTableSchema,
    parse_table_spec,
    validate_table_schema,
)
from sdtp.sdtp_table_factory import TableBuilder
from sdtp.sql_base_table import BaseSQLTable


SCHEMA = [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "number"},
    {"name": "city", "type": "string"},
]


def test_parse_table_spec_returns_specific_pydantic_models():
    row_spec = parse_table_spec({"type": "RowTable", "schema": SCHEMA[:1], "rows": [["Ada"]]})
    remote_spec = parse_table_spec(
        {
            "type": "RemoteSDMLTable",
            "schema": SCHEMA[:1],
            "url": "https://example.test",
            "table_name": "people",
        }
    )
    container_spec = parse_table_spec(
        {
            "type": "ContainerTable",
            "schema": SCHEMA[:1],
            "table_name": "people",
            "container": {"service_name": "people-service", "env": {"MODE": "test"}},
        }
    )

    assert isinstance(row_spec, RowTableSchema)
    assert isinstance(remote_spec, RemoteTableSchema)
    assert isinstance(container_spec, ContainerTableSchema)


def test_table_builder_constructs_row_table_from_validated_model():
    table = TableBuilder.build_table(
        {
            "type": "RowTable",
            "schema": SCHEMA[:2],
            "rows": [["Ada", "36"], ["Grace", 37]],
        }
    )

    assert isinstance(table, RowTable)
    assert table.schema == SCHEMA[:2]
    assert table.rows == [["Ada", 36], ["Grace", 37]]
    assert table.to_dictionary()["type"] == "RowTable"


def test_container_table_accepts_current_and_legacy_aliases():
    current = TableBuilder.build_table(
        {
            "type": "ContainerTable",
            "schema": SCHEMA[:1],
            "table_name": "people",
            "container": {"service_name": "people-service", "env": {"MODE": "test"}},
        }
    )
    legacy = TableBuilder.build_table(
        {
            "type": "ContainerTable",
            "schema": SCHEMA[:1],
            "name": "people",
            "computation": {"service_name": "legacy-service"},
        }
    )

    assert isinstance(current, ContainerTable)
    assert current.table_name == "people"
    assert current.service_name == "people-service"
    assert current.env == {"MODE": "test"}
    assert current.to_dictionary()["container"]["service_name"] == "people-service"

    assert isinstance(legacy, ContainerTable)
    assert legacy.table_name == "people"
    assert legacy.service_name == "legacy-service"
    assert legacy.env == {}


def test_validate_table_schema_rejects_legacy_columns_key():
    with pytest.raises(ValueError, match="only 'schema' is supported"):
        validate_table_schema({"type": "RowTable", "columns": SCHEMA[:1], "rows": [["Ada"]]})


class RecordingSQLTable(BaseSQLTable):
    def __init__(self):
        super().__init__(SCHEMA, "people")
        self.calls = []
        self.next_rows = [["Ada", 36], ["Grace", 37]]

    def _execute_sql(self, query, params=None):
        self.calls.append((query, params))
        return self.next_rows

    def _compile_dialect_operator(self, operator, column, spec):
        if operator == "REGEX_MATCH":
            return f"{column} REGEXP ?", [spec["expression"]]
        return "", []

    def all_values(self, column_name):
        return []

    def range_spec(self, column_name):
        return []


def test_sql_table_pushes_projection_and_predicates_into_parameterized_sql():
    table = RecordingSQLTable()

    rows = table.get_filtered_rows(
        {
            "operator": "ALL",
            "arguments": [
                {"operator": "IN_LIST", "column": "city", "values": ["Oakland", "Berkeley"]},
                {"operator": "GE", "column": "age", "value": 30},
            ],
        },
        columns=["name", "age"],
    )

    assert rows == [["Ada", 36], ["Grace", 37]]
    assert table.calls == [
        (
            "SELECT name, age FROM people WHERE (city IN (?, ?)) AND (age >= ?)",
            ["Oakland", "Berkeley", 30],
        )
    ]


def test_sql_table_handles_any_none_in_range_and_dialect_operator():
    table = RecordingSQLTable()

    table.get_filtered_rows(
        {
            "operator": "ANY",
            "arguments": [
                {"operator": "REGEX_MATCH", "column": "name", "expression": "^A"},
                {"operator": "IN_RANGE", "column": "age", "min_val": 30, "max_val": 40},
            ],
        },
        columns=["name"],
        format="dict",
    )

    assert table.calls == [
        (
            "SELECT name FROM people WHERE (name REGEXP ?) OR ((age >= ?) AND (age <= ?))",
            ["^A", 30, 40],
        )
    ]

    table.get_filtered_rows({"operator": "NONE", "arguments": []})
    assert table.calls[-1] == ("SELECT name, age, city FROM people WHERE 1=1", [])


def test_sql_table_returns_projected_sdml_and_rejects_bad_columns():
    table = RecordingSQLTable()
    table.next_rows = [["Ada"], ["Grace"]]

    result = table.get_filtered_rows(columns=["name"], format="sdml")

    assert isinstance(result, RowTable)
    assert result.schema == [SCHEMA[0]]
    assert result.rows == [["Ada"], ["Grace"]]

    with pytest.raises(InvalidDataException, match="'missing' is not a valid column"):
        table.get_filtered_rows(columns=["missing"])
