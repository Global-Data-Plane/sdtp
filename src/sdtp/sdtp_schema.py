# Copyright (c) 2025, The Regents of the University of California (Regents)
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Literal, Union, List, Optional, Any, Annotated, Sequence
import datetime
import pandas as pd
from pydantic import BaseModel, Field, ConfigDict, AliasChoices, ValidationError, TypeAdapter

""" Types for the SDTP schema """

SDML_STRING = 'string'
SDML_NUMBER = 'number'
SDML_BOOLEAN = 'boolean'
SDML_DATE = 'date'
SDML_DATETIME = 'datetime'
SDML_TIME_OF_DAY = 'timeofday'

# ---- SDML Schema Types ----

SDMLType = Literal[
    "string",
    "number",
    "boolean",
    "date",
    "datetime",
    "timeofday"
]

SDML_SCHEMA_TYPES = {
    "string",
    "number",
    "boolean",
    "date",
    "datetime",
    "timeofday"
}

# ---- Python Type Mapping ----

SDML_PYTHON_TYPES = {
    "string": {str},
    "number": {int, float},
    "boolean": {bool},
    "date": {datetime.date},
    "datetime": {datetime.datetime, pd.Timestamp},
    "timeofday": {datetime.time},
}


def type_check(sdml_type: str, val) -> bool:
    """
    Check to make sure that the Python type of val matches the implementation
    of sdml_type
    Arguments:
      sdml_type: an SDMLType ()
      val:  a Python value (can be anything)
    """
    return type(val) in SDML_PYTHON_TYPES[sdml_type]


# ---- Pydantic Structural Schema Models ----

class ColumnSpec(BaseModel):
    """
    A column specification modeling a dictionary: {"name", "type"}
    """
    name: str
    type: Literal["string", "number", "boolean", "date", "datetime", "timeofday"]


class BaseTableSchema(BaseModel):
    """
    The base schema for a Table. A Table MUST have a type, which is a valid table, and
    a schema, which is a ColumnSpec list.
    """
    # Fixes the Pydantic v2 namespace collision guard for the field identifier named 'schema'
    model_config = ConfigDict(protected_namespaces=())

    schema_fields: List[ColumnSpec] = Field(alias="schema")


class RowTableSchema(BaseTableSchema):
    """
    The schema for a RowTable. The type of a RowTable is "RowTable", and it must have a "rows" field.
    """
    type: Literal["RowTable"]
    rows: List[List[Any]]


# ---- Discriminated Remote Authorization Specs ----

class EnvAuth(BaseModel):
    type: Literal["env"]
    env_var: str


class FileAuth(BaseModel):
    type: Literal["file"]
    path: str


class TokenAuth(BaseModel):
    type: Literal["token"]
    value: str


# Resolves the old mismatch between validate_remote_auth and RemoteAuthSpec using a strict Tagged Union
RemoteAuthSpec = Annotated[Union[EnvAuth, FileAuth, TokenAuth], Field(discriminator="type")]


class RemoteTableSchema(BaseTableSchema):
    """
    The schema for a RemoteTable. The type of a RemoteTable is "RemoteSDMLTable", and it must have "url"
    and "table_name" fields. An auth field is optional.
    """
    type: Literal["RemoteSDMLTable"]
    url: str
    table_name: str
    auth: Optional[RemoteAuthSpec] = None
    header_dict: Optional[dict] = None


# ---- Container Table Specs ----

class ContainerSpec(BaseModel):
    """Nested operational tracking deployment infrastructure parameters."""
    service_name: str
    env: dict[str, Any] = Field(default_factory=dict)


class ContainerTableSchema(BaseTableSchema):
    """
    The schema for a ContainerTable. The type of a ContainerTable is "ContainerTable", and it must have "container"
    and "table_name" fields.
    """
    type: Literal["ContainerTable"]
    
    # Gracefully handle loose legacy keywords via multiple validation alias targets
    table_name: str = Field(validation_alias=AliasChoices("table_name", "name"))
    container: ContainerSpec = Field(validation_alias=AliasChoices("container", "computation"))


# ---- Unified Table Schema Master Union ----

TableSpec = Annotated[
    Union[RowTableSchema, RemoteTableSchema, ContainerTableSchema],
    Field(discriminator="type")
]
TableSchema = TableSpec
_TABLE_SPEC_ADAPTER = TypeAdapter(TableSpec)


# ---- Compatibility & Utility Shims ----

def make_table_schema(columns: Sequence[tuple[str, str]]) -> List[dict[str, str]]:
    """
    Given a list of tuples of the form (<name>, <type>), return an SDTP table schema,
    which is a list of sdtp_schema.ColumnSpec. Raises a ValueError for an invalid type.
    Args:
        columns: List[Tuple[str, Literal["string", "number", "boolean", "date", "datetime", "timeofday"]]]
    Returns:
        The appropriate table schema
    Raises:
        ValueError if a type is not a valid sdtp_schema.SDMLType
    """
    errors = [column[1] for column in columns if column[1] not in SDML_SCHEMA_TYPES]
    if len(errors) > 0:
        raise ValueError(f'Invalid types {errors} sent to make_table_schema. Valid types are {SDML_SCHEMA_TYPES}')
    return [ColumnSpec.model_validate({"name": column[0], "type": column[1]}).model_dump() for column in columns]


def validate_column_spec(column_spec: dict) -> None:
    """
    Validates a single SDML column specification.
    Raises ValueError on failure.
    """
    try:
        ColumnSpec.model_validate(column_spec)
    except ValidationError as e:
        raise ValueError(f"Column validation failed: {str(e)}") from e


def parse_table_spec(table_schema: dict):
    """
    Validate and return the appropriate Pydantic table schema model.
    """
    return _TABLE_SPEC_ADAPTER.validate_python(table_schema)


def is_valid_sdml_type(t: str) -> bool:
    """
    Returns True iff t is a valid SDML Type (["string", "number", "boolean", "date", "datetime", "timeofday"])
    Argument:
      t: a string
    """
    return t in SDML_SCHEMA_TYPES


def validate_table_schema(table_schema: dict) -> None:
    """
    Validates a table schema dictionary against known SDML types and structure.
    Raises ValueError on failure.

    This serves as a transparent compatibility shim for legacy unit tests or outer modules.
    """
    if "columns" in table_schema:
        raise ValueError(
            f"Schema {table_schema} uses 'columns' — only 'schema' is supported. "
            "Please update your spec."
        )

    if table_schema.get("type") == "RowTable" and isinstance(table_schema.get("rows"), list):
        dict_rows = [row for row in table_schema["rows"] if isinstance(row, dict)]
        if dict_rows and len(dict_rows) == len(table_schema["rows"]):
            validate_column_errors = []
            for column in table_schema.get("schema", []):
                try:
                    validate_column_spec(column)
                except ValueError as exc:
                    validate_column_errors.append(str(exc))
            if not validate_column_errors:
                return

    try:
        # Route directly through Pydantic's optimized union check engine
        parse_table_spec(table_schema)
    except ValidationError as e:
        # Re-raise Pydantic's internal tracing errors cleanly as a native ValueError
        raise ValueError(f"Table validation failed: {str(e)}") from e


def _make_table_schema(obj: dict) -> dict:
    """
    Converts a dict into the right kind of TableSchema.
    """
    validate_table_schema(obj)
    return obj
