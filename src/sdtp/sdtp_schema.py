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

from typing import TypedDict, Literal, Union, List, Set, Optional
import datetime
import pandas as pd

""" Types for the SDTP schema """
# Prefer SDMLType literals or schema specs in new code
# These constants remain for legacy compatibility


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

# Optional: list for runtime introspection
SDML_SCHEMA_TYPES =  {
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
    '''
    Check to make sure that the Python type of val matches the implementation
    of sdml_type
    Arguments:
      sdml_type: an SDMLType ()
      val:  a Python value (can be anything)
    '''
    """Check whether a value matches the given SDML type."""
    return type(val) in SDML_PYTHON_TYPES[sdml_type]

# ---- Schema Definitions ----

class ColumnSpec(TypedDict):
    '''
    A column is a dictionary: {"name", "type"} where 
    '''
    name: str
    type: Literal["string", "number", "boolean", "date", "datetime", "timeofday"]


def is_valid_sdml_type(t: str) -> bool:
    '''
    Returns True iff t is a valid SDML Type (["string", "number", "boolean", "date", "datetime", "timeofday"])
    Argument:
      t: a string
    '''
    return t in SDML_SCHEMA_TYPES

def validate_column_spec(col: dict) -> None:
    '''

    Validates that the given column dictionary includes required fields and a valid SDML type.
    Raises ValueError if invalid.

    Argument:
      col: a dictionary
    '''
    if "name" not in col or "type" not in col:
        raise ValueError("Column spec must include 'name' and 'type'")
    if not is_valid_sdml_type(col["type"]):
        raise ValueError(f"Invalid SDML type: {col['type']}")
    
    

def validate_remote_auth(auth: dict) -> None:
    '''
    Ensure that the selected auth type has the required parameters.
    Throws a ValueError if the auth type is unrecognized or the required
    parameter is not present.
    '''
    required_fields = {
        'env': 'env_var',
        'file': 'path',
        'token': 'value'
    }
    if not 'type' in auth:
        raise ValueError(f'Authorization object {auth} must have a type')
    if not auth['type'] in required_fields:
        raise ValueError(f'Authorization type {auth["type"]} is invalid.  Valid types are {required_fields.keys()}')
    required_field = required_fields[auth['type']]
    if required_field not in auth:
        raise ValueError(f'{auth["type"]} requires parameter {required_field} but this is not present in {auth}')
    
def _check_required_fields(table_schema: dict, table_type: str, required_fields: set):
    missing = required_fields - set(table_schema.keys())
    if missing:
        raise ValueError(
            f"{table_type} requires fields {required_fields}. Missing: {missing} from schema {table_schema}"
        )

def validate_table_schema(table_schema: dict) -> None:
    """
    Validates a table schema dictionary against known SDML types and structure.
    Raises ValueError on failure.

    This function supports both 'schema' and 'columns' as input keys for column definitions,
    but normalizes the schema in-place to use 'columns'. This ensures compatibility with
    legacy schemas while standardizing all downstream usage to 'columns'.
    Argument:
        table_schema: the schema as a dictionary
    """
    schema_keys = ["columns", "schema"]
    chosen_keys = [key for key in schema_keys if key in table_schema]
    if len(chosen_keys) == 0:
        raise ValueError(f"Schema {table_schema} must include a 'schema' or 'columns' list")
    elif len(chosen_keys) == 2:
        raise ValueError(f"Schema {table_schema} can only contain one of 'schema', 'columns'")
    chosen_key = chosen_keys[0]
    if chosen_key == 'schema': # normalise to columns
        table_schema["columns"] = table_schema.pop("schema")
    if not isinstance(table_schema["columns"], list):
        raise ValueError(f"{table_schema[chosen_key]} must be a list of columns")

    for col in table_schema['columns']:
        validate_column_spec(col)

    table_type = table_schema.get("type")
    if not table_type:
        raise ValueError("Schema must include a 'type' field")
    
    required_fields_by_type = {
        "FileTable": {"path"},
        "GCSTable": {"bucket", "blob"},
        "HTTPTable": {"url"},
        "RemoteSDMLTable": {"url", "table_name"},
        "RowTable": {"rows"}
    }

    if table_type not in required_fields_by_type:
        raise ValueError(f"Unknown or unsupported table type: {table_type}")

    if table_type == "remote" and "auth" in table_schema:
        validate_remote_auth(table_schema["auth"])

    _check_required_fields(table_schema, table_type, required_fields_by_type[table_type])



# --- Base Table Schema ---
class BaseTableSchema(TypedDict):
    '''
    The base schema for a Table.  A Table MUST have a type, which is a valid table, and
    a schema, which is a ColumnSpec
    '''
    type: str  # Table type: "row", "remote", etc.
    schema: list[ColumnSpec]
    columns: list[ColumnSpec]

# --- Row Table Schema ---
class RowTableSchema(BaseTableSchema):
    '''
    The schema for a RowTable.  The type of a RowTable is "row", and it must have a "rows"
    field
    '''
    type: Literal["row"]
    rows: list[list]

# --- RemoteAuthSpec ---
class RemoteAuthSpec(TypedDict, total=False):
    '''
    Specification of a Remote Authentication, for use with RemoteTables.
    It currently supports tokens, env variables, and 
    '''
    type: Literal["bearer"]
    value: str
    file_path: str
    env_var: str

# --- Remote Table Schema ---
class RemoteTableSchema(BaseTableSchema):
    '''
    The schema for a RemoteTable.  The type of a RemoteTable is "remote", and it must have  "url"
    and "table_name" fields.  An auth field is optional
    '''
    type: Literal["remote"]
    url: str
    table_name: str
    auth: Optional[RemoteAuthSpec]

# --- File Table Schema ---
class FileTableSchema(BaseTableSchema):
    '''
    The schema for a FileTable.  The type of a FileTable is "file", and it must have  a "path"
    field. 
    '''
    type: Literal["file"]
    path: str

# --- GCS Table Schema ---
class GCSTableSchema(BaseTableSchema):
    '''
    The schema for a GCSTable.  The type of a GCSTable is "gcs", and it must have  "bucket" and "blob" fields 
    '''
    type: Literal["gcs"]
    bucket: str
    blob:str

# --- HTTP Table Schema ---
class HTTPTableSchema(BaseTableSchema):
    '''
    The schema for an HTTPTable.  The type of an HTTPTable is "http", and it must have a "url"
    field.  An auth field is optional
    '''
    type: Literal["http"]
    url: str
    auth: Optional[RemoteAuthSpec]
    
    

# --- Unified Table Schema Union ---
TableSchema = Union[RowTableSchema, RemoteTableSchema, FileTableSchema, GCSTableSchema, HTTPTableSchema]

# --- Simple make_schema() dispatcher ---
def _make_table_schema(obj: dict):
    '''
    Converts a dict into the right kind of TableSchema
    '''
    table_type = obj.get("type")
    validate_table_schema(obj) 
    return obj  # type: ignore
    
