# SDTP Protocol Reference

The SDTP (Simple Data Transfer Protocol) defines a minimal REST API for exposing, querying, and retrieving tabular data described in SDML format. SDTP is designed for clarity, composability, and compatibility, and provides explicit endpoints for accessing table metadata, schema, and filtered row/column data.

**Note:** SDTP does not provide authentication, security, or advanced search. It is intended to be composed with external tools for authentication, proxying, and orchestration.

---

## Route Index

| Endpoint             | Method | Description                             |
| -------------------- | ------ | --------------------------------------- |
| /get\_table\_names   | GET    | Returns a list of available table names |
| /get\_tables         | GET    | Returns a list of all tables (as dicts) |
| /get\_table\_schema  | GET    | Returns schema for a table              |
| /get\_range\_spec    | POST   | Returns min/max values for a column     |
| /get\_all\_values    | POST   | Returns all distinct values in column   |
| /get\_column         | POST   | Returns all values (with duplicates)    |
| /get\_filtered\_rows | POST   | Returns filtered rows (list or SDML)    |

---

## `/get_table_names`

Returns a JSON list of available table names (not full URLs).

**Example response:**

```json
["nightingale", "elections"]
```

---

## `/get_tables`

Returns a JSON list of all tables, each as a dictionary.

**Example response:**

```json
[
  {
    "name": "nightingale",
    "schema": [...],
    "description": "..."
  },
  ...
]
```

---

## `/get_table_schema`

Returns the schema for a given table.

**Request:**
`GET /get_table_schema?table=nightingale`

**Returns:**
An object with a `columns` key, whose value is a list of dictionaries defining each column (name, type, etc).

**Example response:**

```json
{
  "columns": [
    {"name": "Month", "type": "string"},
    {"name": "Year", "type": "number"},
    ...
  ]
}
```

---

## `/get_range_spec`

Returns the minimum and maximum values for a column in a table.

**Request:**

```json
{
  "table": "nightingale",
  "column": "Year"
}
```

**Response:**

```json
{
  "min": 1854,
  "max": 1856
}
```

Returns HTTP 4xx error if the column or table is not found.

---

## `/get_all_values`

Returns all distinct values for a column.

**Request:**

```json
{
  "table": "nightingale",
  "column": "Month"
}
```

**Response:**

```json
["Jan", "Feb", "Mar", ...]
```

---

## `/get_column`

Returns all values for a column, including duplicates and in table order.

**Request:**

```json
{
  "table": "nightingale",
  "column": "Disease"
}
```

**Response:**

```json
[150, 200, 180, ...]
```

---

## `/get_filtered_rows`

Returns rows matching a filter, either as a list of lists (default), or as a full SDML table (if `result_format` is set to "sdml").

**Request (list format):**

```json
{
  "table": "nightingale",
  "columns": ["Month", "Disease"],
  "filter_spec": {
    "column": "Year",
    "operator": "IN_LIST",
    "values": [1855]
  }
}
```

**Response (list format):**

```json
[
  ["Jan", 3150],
  ["Feb", 2230],
  ...
]
```

*The response is a list of lists, one per row, with values for the requested columns in order.*

**Request (SDML format):**

```json
{
  "table": "nightingale",
  "columns": ["Month", "Disease"],
  "filter_spec": {
    "column": "Year",
    "operator": "IN_LIST",
    "values": [1855]
  },
  "result_format": "sdml"
}
```

**Response (SDML format):**

```json
{
  "type": "RowTable",
  "schema": [
    {"name": "Month", "type": "string"},
    {"name": "Disease", "type": "number"}
  ],
  "rows": [
    ["Jan", 3150],
    ["Feb", 2230],
    ...
  ]
}
```

---

## Error Handling

All endpoints return HTTP 4xx or 5xx on error.

**Error response example:**

```json
{
  "error": "Table 'nightingale' not found"
}
```

---

## Protocol Conventions: Server-to-Server Queries

SDTP may be used for server-to-server requests, such as proxying SDTP tables from a remote server or integrating with multi-site data providers.

* **Standard headers:** Server-to-server requests may use HTTP headers for forwarding, proxy, or metadata, but SDTP endpoints themselves do not require or interpret these headers.
* **URL composition:** All endpoints accept POST (with JSON body) or GET (with query parameters) as specified.

**Example server-to-server request:**

```json
{
  "table": "experiment_data",
  "columns": ["Sample", "Result"],
  "filter_spec": {
    "operator": "GT",
    "column": "Result",
    "value": 0.9
  }
}
```

**Example server-to-server response:**

```json
[
  ["Sample1", 0.92],
  ["Sample3", 1.01]
]
```

---

## See Also

* [SDML Reference](sdml_reference.md)
* [SDQL Reference](sdql_reference.md)
* [Architecture](architecture.md)

