# API Reference

## Table Classes

### Abstract Base

::: sdtp.SDMLTable

### Concrete Table Types

::: sdtp.SDMLFixedTable
::: sdtp.RowTable
::: sdtp.RemoteSDMLTable

## Table Factories

### Abstract Base

::: sdtp.SDMLTableFactory

### Concrete Factories

::: sdtp.RowTableFactory
::: sdtp.RemoteSDMLTableFactory

### Table Builder

::: sdtp.TableBuilder

## Filtering

### Abstract Base

::: sdtp.SDQLFilter

### Atomic Filters

::: sdtp.InListFilter
::: sdtp.GEFilter
::: sdtp.GTFilter
::: sdtp.LEFilter
::: sdtp.LTFilter
::: sdtp.RegexFilter

### Compound Filters

::: sdtp.AllFilter
::: sdtp.AnyFilter
::: sdtp.NoneFilter

### Utility Functions

::: sdtp.make_filter
::: sdtp.check_valid_spec
::: sdtp.check_valid_spec_return_boolean

### Filter Constants

::: sdtp.SDQL_FILTER_OPERATORS
::: sdtp.SDQL_FILTER_FIELDS

## Schema

### SDML Type Constants

::: sdtp.SDML_STRING
::: sdtp.SDML_NUMBER
::: sdtp.SDML_BOOLEAN
::: sdtp.SDML_DATE
::: sdtp.SDML_DATETIME
::: sdtp.SDML_TIME_OF_DAY

### SDML Type Definitions

::: sdtp.SDMLType
::: sdtp.SDML_SCHEMA_TYPES
::: sdtp.SDML_PYTHON_TYPES

### Schema Construction & Validation

::: sdtp.type_check
::: sdtp.make_table_schema
::: sdtp.is_valid_sdml_type
::: sdtp.validate_column_spec
::: sdtp.validate_table_schema

### Schema Structures

::: sdtp.ColumnSpec
::: sdtp.BaseTableSchema
::: sdtp.RowTableSchema
::: sdtp.RemoteAuthSpec
::: sdtp.RemoteTableSchema
::: sdtp.TableSchema

## Utilities

### Exceptions

::: sdtp.InvalidDataException

### Serialization Utilities

::: sdtp.json_serialize
::: sdtp.jsonifiable_value
::: sdtp.jsonifiable_row
::: sdtp.jsonifiable_rows
::: sdtp.jsonifiable_column

### Type Checking & Conversion

::: sdtp.check_sdml_type_of_list
::: sdtp.convert_to_type
::: sdtp.convert_list_to_type
::: sdtp.convert_row_to_type_list
::: sdtp.convert_rows_to_type_list
::: sdtp.convert_dict_to_type

### Authentication Utilities

::: sdtp.EnvAuthMethod
::: sdtp.PathAuthMethod
::: sdtp.ValueAuthMethod
::: sdtp.AuthMethod
::: sdtp.resolve_auth_method

## Table Server

### Exceptions

::: sdtp.TableNotFoundException
::: sdtp.ColumnNotFoundException

### Table Server

::: sdtp.TableServer

### Table Loader Adapters

::: sdtp.TableLoader
::: sdtp.FileTableLoader
::: sdtp.HTTPTableLoader
::: sdtp.HeaderInfo

## SDTP Web Server

The `SDTPServer` blueprint exposes the following REST API endpoints:

- `/get_table_names`
- `/get_tables`
- `/get_table_schema`
- `/get_filtered_rows`
- `/get_range_spec`
- `/get_all_values`
- `/get_column`

All endpoints return JSON; see the SDTP protocol docs for usage.


### Flask Blueprint

::: sdtp.SDTPServer
::: sdtp.sdtp_server_blueprint


## SDTP Client

### Exceptions

::: sdtp.SDTPClientError

### Configuration

::: sdtp.load_config

### Main Client

::: sdtp.SDTPClient





      

