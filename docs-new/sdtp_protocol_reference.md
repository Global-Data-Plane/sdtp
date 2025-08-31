# SDTP Protocol Reference

This document describes the REST API endpoints implemented by the SDTP Server. It is intended for developers and systems that need to discover, inspect, and query tabular datasets over HTTP. All endpoints return data in JSON format.

---

## Design Philosophy

 The Simple Data Transfer Protocol (SDTP)  permits the execution of Simple Data Query Language (SDQL) queries on Simple Data Markup Language (SDML) tables over the network.   It is a set of seven  routes which can be implemented by any HTTP/S server; a reference implementation on a Flask server is available.  

The primary design goal of SDTP is _ease of adoption_.  It should be easy to implement SDTP in any existing web server.  SDTP is designed to require _no_ specialized software on either the client or the server side.  SDTP queries are standard HTTP/S POST/GET, and the return values are JSON dictionaries and lists.

This design goal led to a very spare, simple protocol.  The design mantra was "When in doubt, leave it out".  Useful protocols and standards add required features in response to user needs over time; simplicity in initial design permits the maximum flexibility in adding these features when and as they are needed, with specific use cases in mind.   It also permits the use of generic HTTP/S features for features and use cases. Finally, it permits implementers maximum freedom in enhancing the protocol for specific situations.

SDTP is not designed or intended to be a complete data hosting solution.  A number of features that are desirable or required in a hosting solution are absent from the basic SDTP protocol.  Search is one example.  It can be anticipated that a single SDTP server can host a large number of SDML tables, either physically or, through the SDML RemoteTable mechanism, virtually, or both.  data.gov, for example, has about 300,000 datasets, and almost all of these are easily convertible to SDML.  _Finding_ the right datasets for a problem is desirable; it's also a feature with a large number of existing implementations, and SDTP sites are free to implement the search mechanism appropriate for their domain -- or none at all.

SDTP is not a general-purpose database protocol. It does not implement distributed transactions, authorization, or query optimization. Its goal is to enable transparent, portable, and scriptable data access using standard HTTP calls.


Similar reasoning applies to a lack of security in the protocol.  Early versions of the SDTP anticipated per-table access control based on header variables.  This was dropped, because there are a plethora of HTTP/S access control mechanisms that are adapted for specific purposes.  At the end of the day, access to tabular data is no different from API access to document or image data, and access issues are well solved in HTTP/S.

In sum, SDTP is not designed as a standalone protocol.  It is a set of standard routes that must be implemented by a general HTTP/S server.

## SDTP Routes
There are three classes of route in the SDTP protocol: one for getting the names and schemas of the tables the server hosts, another for executing column queries on a specific table, and a third for executing row queries.  These routes enable:
* Listing available tables
* Inspecting schemas
* Discovering data value ranges
* Querying rows and columns, optionally with filters

A major design goal is that no specific client libraries or software beyond a standard HTTP/S request library (`fetch` in JavaScript, `requests` or the various `urllib`s in Python, `curl` or `wget` from the command line) are required.  Requests are standard HTTP/S `GET` requests with parameters or `POST` requests with a JSON body.  Returns are _always_ JSON objects or lists, and, when there is a tradeoff between contextual information and ease of parsing, the latter consideration dominates.  For example, in early versions of the protocol, a `get_range` request returned a JSON dictionary with two fields, `max_val` and `min_val`.  This was dropped in favor of returning a two-element ordered list: `{"min_val: <v1>, "max_val": <v2>}` became `[v1, v2]`, because every client has the ability to parse a JSON list in a single API call.  This is a very simple and trivial example, but it illustrates the design philosophy.

Similarly, SDTP uses standard HTTP/S error codes.

---

## Route Index

| Endpoint             | Method | Parameters                                                                                                                              | Description                                    |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `/get_table_names`   | GET    |                                                                                                                                         | List all tables accessible by this user (URLs) |
| `/get_tables`        | GET    |                                                                                                                                         | List schemas for all accessible tables         |
| `/get_table_schema`  | GET    | `table` (string)                                                                                                                        | Schema of a specific table                     |
| `/get_range_spec`    | GET    | `table` (string), `column` (string)                                                                                                     | Min/max of a column, as JSON                   |
| `/get_all_values`    | GET    | `table` (string), `column` (string)                                                                                                     | Distinct values in a column, as JSON list      |
| `/get_column`        | GET    | `table` (string), `column` (string)                                                                                                     | All values in a column, as JSON list           |
| `/get_filtered_rows` | POST   | `table` (string, required); `columns` (list, optional); `filter_spec` (SDQL, optional), `result_format` ("list", or "sdml", or "dict"). | Rows matching the filter                       |

All routes require no authentication in the reference implementation. Other deployments may apply access controls using standard HTTP/S mechanisms (e.g., Bearer tokens in the header)

---

## Endpoint Reference & Examples (using Nightingale Data)

### Table Routes
This class consists of three  routes, `get_table_names`, `get_table_schema?table=<table_name>`, `get_tables`.


#### 1. `GET /get_table_names`

* **Description:**
  Returns a JSON list of table names accessible to the user.
* **Methods:** `GET`
* **Parameters**: None
* **Body:** None
* **Headers:** None
* **Returns:** A JSON list of the names of the tables hosted by this server
* **Errors:** None
* **Response Example:**

  ```json
  ["nightingale.sdml"]
  ```

---

#### 2. `GET /get_tables`

* **Description:**
  Returns a mapping of table names to their SDML schemas.
* **Methods:** `GET`
* **Parameters**: None
* **Body:** None
* **Headers:** None
* **Returns:** A JSON  dictionary of the form:
    `{table_name: <table_schema>}`, where <table_schema> is a list of dictionaries of the form 
    `{"name": name, "type": type}`
* **Errors:** None
* **Response Example:**

  ```json
  {
    "nightingale.sdml": {
      "columns": [
        {"name": "Month_Number", "type": "int"},
        {"name": "Date", "type": "date"},
        {"name": "Month", "type": "string"},
        {"name": "Year", "type": "int"},
        {"name": "Army", "type": "int"},
        {"name": "Disease", "type": "int"},
        {"name": "Wounds", "type": "int"},
        {"name": "Other", "type": "int"},
        {"name": "Disease.rate", "type": "float"},
        {"name": "Wounds.rate", "type": "float"},
        {"name": "Other.rate", "type": "float"}
      ]
    }
  }
  ```

---

### 3. `GET /get_table_schema`

* **Description:**
  Returns the schema for a single table.
* **Methods:** `GET`
* **Parameters:**

  * `table` (string): Table name.

 
* **Returns:** A JSON   a list of dictionaries of the form 
    `{"name": name, "type": type}`
* **Errors:** 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server.
* **Example Request:**
  `/get_table_schema?table=nightingale`
* **Response Example:**

  ```json
  {
    "columns": [
      {"name": "Month_Number", "type": "int"},
      {"name": "Date", "type": "date"},
      {"name": "Month", "type": "string"},
      {"name": "Year", "type": "int"},
      {"name": "Army", "type": "int"},
      {"name": "Disease", "type": "int"},
      {"name": "Wounds", "type": "int"},
      {"name": "Other", "type": "int"},
      {"name": "Disease.rate", "type": "float"},
      {"name": "Wounds.rate", "type": "float"},
      {"name": "Other.rate", "type": "float"}
    ]
  }
  ```

---

### 4. `GET /get_range_spec`

* **Description:**
  Returns the minimum and maximum values for a column in a table.
* **Methods:** `GET`
* **Parameters:**

  * `table` (string): Table name.
  * `column` (string): Column name.
* **Body:** None
* **Headers:** None
* **Returns:** A two-valued list  of the form `[min_val, max_val]`
* **Errors:** 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server`. 400: `Missing parameter column` if the column is missing, or 400: `No column column on table table` if the column isn't found.
* **Example Request:**
  `/get_range_spec?table=nightingale&column=Disease`
* **Response Example:**

  ```json
  [1, 2761]
  
  ```

---

### 5. `GET /get_all_values`

* **Description:**
  Returns all distinct values for a column in a table.
* **Methods:** `GET`
* **Parameters:**

  * `table` (string): Table name.
  * `column` (string): Column name.
* **Body:** None
* **Headers:** None
* **Returns:** A list of all of the distinct values in the column
* **Errors:** 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server`. 400: `Missing parameter column` if the column is missing, or 400: `No column column on table table` if the column isn't found.
* **Example Request:**
  `/get_all_values?table=nightingale&column=Month`
* **Response Example:**

  ```json
  [
    "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"
  ]
  ```

---

### 6. `GET /get_column`

* **Description:**
  Returns all values (including duplicates) in a column, as a JSON list.
* **Methods:** `GET`
* **Parameters:**

  * `table` (string): Table name.
  * `column` (string): Column name.
* **Body:** None
* **Headers:** None
* **Returns:** A list of all of the  values in the column
* **Errors:** 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server`. 400: `Missing parameter column` if the column is missing, or 400: `No column column on table table` if the column isn't found.
* **Example Request:**
  `/get_column?table=nightingale&column=Disease`
* **Response Example:**

  ```json
  [1, 12, 11, 359, 828, 788, 503, 844, 1725, 2761, 2120, 1205, 477, ...]
  ```

---

### 7. `POST /get_filtered_rows`

* **Description:**
  Returns rows matching an optional filter and/or column projection.
* **Methods:** `POST`
* **Parameters:** None
* **Body:** A JSON structure of the form:
  * `table`: (string, required): Table name.
  * `columns`: (list, optional): List of columns to return.  Default is all columns.
  * `filter_spec`: (object, optional): SDQL filter object.
  * `result_format`: one of `"list", "dict", "sdml"`.  Default is `"list"`.  Specify the format of the return.  If `"list"`, the result is a list of lists of values.  If `"dict"`, the result is a list of dictionaries `{<column>: <value>}`.  If `"sdml"`, the result is an SDML RowTable.
* **Headers**: None
* **Returns:** A list of lists of the rows of the table which match the `filter_spec`.  If the `columns` list is specified, only entries for those columns are sent.  If `filter_spec` is absent, all rows of the table are returned.
* **Errors:** 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server`. 400: `column not found` if the columns are specified and a column
is not present.  400: `Bad filter spec` if the filter spec is not formed
* **Request Example:**
Dict format:
  ```json
  {
    "table": "nightingale",
    "columns": ["Month", "Disease"],
    "filter_spec": {
      "column": "Year",
      "operator": "IN_LIST",
      "values": [1855]
    },
    "result_format": "dict"
  }
  ```
* **Response Example:**

  ```json
  [
    {"Month": "Jan", "Disease": 2761},
    {"Month": "Feb", "Disease": 2120},
    {"Month": "Mar", "Disease": 1205},
    {"Month": "Apr", "Disease": 477},
    {"Month": "May", "Disease": 508},
    {"Month": "Jun", "Disease": 802},
    {"Month": "Jul", "Disease": 382},
    {"Month": "Aug", "Disease": 483},
    {"Month": "Sep", "Disease": 189},
    {"Month": "Oct", "Disease": 128},
    {"Month": "Nov", "Disease": 178},
    {"Month": "Dec", "Disease": 91}
  ]
  ```
  List format (default):
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
* **Response Example:**

  ```json
  [
    ["Jan", 2761],
    ["Feb", 2120],
    ["Mar", 1205],
    ["Apr", 477],
    ["May", 508],
    ["Jun", 802],
    ["Jul", 382],
    ["Aug", 483],
    ["Sep", 189],
    ["Oct", 128],
    ["Nov", 178],
    ["Dec", 91]
  ]
  ```
  SDML Format:
    ```json
  {
    "table": "nightingale",
    "columns": ["Month", "Disease"],
    "filter_spec": {
      "column": "Year",
      "operator": "IN_LIST",
      "values": [1855],
      "result_format": "sdml"
    }
  }
  ```
* **Response Example:**

  ```json
  {
    "type": "RowTable",
    "schema": [
      {"name": "Month", "type": "string"},
      {"name": "Disease", "type": "number"}
    ],
    "rows": [
      ["Jan", 2761],
      ["Feb", 2120],
      ["Mar", 1205],
      ["Apr", 477],
      ["May", 508],
      ["Jun", 802],
      ["Jul", 382],
      ["Aug", 483],
      ["Sep", 189],
      ["Oct", 128],
      ["Nov", 178],
      ["Dec", 91]
    ]
  }
  ```

---

## Error Handling

All endpoints return HTTP 4xx or 5xx on error. Error responses are JSON objects with a `"message"` key.

**Example error response:**

```json
{
  "message": "Table 'nightingale' not found"
}
```

---
---

## Protocol Conventions: Server-to-Server Queries and Result Format

When one SDTP server acts as a client to another SDTP server (for example, when fulfilling queries for a `RemoteSDMLTable`), the response format for row queries must be robust to schema differences between the two servers.

**Format Requirement for Remote Queries:**
- All inter-server `/get_filtered_rows` requests **must** specify `"result_format": "sdml"` in the request body.
- The remote SDTP server will return an SDML `RowTable` object, which includes both a schema (column names and types) and the matching rows.

**Rationale:**
- Column order, names, and types may differ between the requesting and serving servers.
- The `RowTable` format is self-describing and ensures that the client can accurately reconstruct results based on column names and types, regardless of the order or underlying implementation.
- This format avoids subtle errors that can arise when using the `"list"` format, which assumes identical schema and column order between both parties.
- The `"dict"` format (list of dictionaries) is also self-describing but is less efficient for large row sets.

**Client Guidance:**
- Upon receiving a RowTable response, the client (remote SDTP server) should extract the schema and rows, and align or reorder columns by name to match the user’s request.
- Any requested column that is missing or has a type mismatch should be treated as an error.
- Clients should never assume the column order in the response matches their local schema unless explicitly verified.

**Example inter-server row query request:**
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
**Example response:**
{
  "type": "RowTable",
  "schema": [
    {"name": "Month", "type": "string"},
    {"name": "Disease", "type": "number"}
  ],
  "rows": [
    ["Jan", 2761],
    ["Feb", 2120],
    ["Mar", 1205]
    // ...
  ]
}
```
**Best Practices:**

- All SDTP server implementations should use this convention for any protocol-level communication between SDTP servers or automated clients.

- Only end-user clients (such as data scientists or application frontends) should use other formats, and only if they are certain of the column order.

## See Also

* [Overview](overview.md)
* [SDML Reference](sdml_reference.md)
* [SDQL Reference](sdql_reference.md)
* [Architecture](architecture.md)
* [Manifesto](manifesto.md)

---
