## 1. What Is a Global Data Plane Table?

A **Global Data Plane (GDP) Table** is not just a data file or a static resource.  
It is a *piece of code* that plugs into an SDTP server and enables that server to answer SDTP API requests for a dataset.  
Every GDP Table implements a standard contract, regardless of how its rows are produced or where its data lives.

### Core Features of a GDP Table

Every GDP Table must provide:
1. **A Schema:**  
   A list of columns (each with a name and type), defining the structure of the table.
2. **Filtered Row Access:**  
   A method for returning filtered rows—typically, a way to answer SDQL (Simple Data Query Language) queries for the table.
3. **Column Access and Statistics:**  
   Methods for returning:
   - All values in a given column (including duplicates, if needed)
   - The set of distinct values in a column
   - The minimum and maximum value of a column

This “contract” enables any SDTP server to support common data queries and makes GDP Tables interchangeable and composable, no matter their underlying implementation.

### GDP Table Implementation: Python Reference Server

In the reference Python SDTP server, a GDP Table is created by:

1. **Subclassing the `SDMLTable` base class.**  
   - The schema is supplied to the constructor via the base class `__init__()`.

2. **Implementing the following required methods:**

   ```python
   class MyTable(SDMLTable):
       def all_values(self, column_name):
           # Return all distinct values in the specified column

       def get_column(self, column_name: str):
           # Return all values (including duplicates) in the specified column

       def range_spec(self, column_name: str):
           # Return [min, max] for the specified column

       def _get_filtered_rows_from_filter(self, filter=None, columns=[]):
           # Return rows matching the filter and (optionally) column selection

       def to_dictionary(self):
           # Return the table as a Python dictionary

       def to_json(self):
           # Return the table as a JSON-serializable object
```
- These methods form the minimum interface contract for a GDP Table in the Python SDTP reference implementation.

- Other SDTP servers (in other languages) will define equivalent contracts with similar required methods.

**Summary Table: GDP Table Requirements**

| Requirement   | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| Schema        | Must define columns (name, type)                             |
| Row access    | Must implement methods for filtered row and column access    |
| Column stats  | Must provide all/distinct values and min/max for each column |
| Serialization | Must support dictionary and JSON export                      |
**Takeaway:**
A GDP Table is a composable, code-backed table object that enables any SDTP server to answer standard tabular queries using a consistent interface

## 2. SDML: Declarative Table Markup

**The Simple Data Markup Language (SDML)** is a declarative format that specifies how a GDP Table is instantiated by parameterizing pre-written Table classes with the information they need.  
SDML files are the configuration files for common Table objects:

- The markup declares the table’s schema, type, and the parameters required for that table type.
- The SDTP server reads this markup, looks up the appropriate Table class (by `"type"`), and uses the markup to construct a live Table instance.

### Pre-written Table Implementations

Currently, SDML supports parameterization of two built-in Table types:

#### RowTable

Used when all rows are explicitly stored in the SDML file itself, loaded into memory at server startup.  
The required parameter for this table type (see the RowTable section) is the list of rows of the table.

Best for datasets that are static or small enough to materialize in memory.

#### RemoteSDMLTable

Used when the table data lives on a remote server implementing the SDTP protocol.

The SDML file contains all the info needed to query the remote server. These parameters are:
1. The URL for the remote server
2. The name of the table on the remote server
3. Specification of authentication information, if authentication is required

### Reference Server Implementation

The reference server reads the SDML files in the server's tables directory and loads them on startup.
## 3. RowTable

A **RowTable** is a table whose rows are explicitly listed in the SDML file itself.  
This table type is best for datasets that are static or small enough to be fully loaded into memory.

**Required fields:**
- `"type"`: Must be `"RowTable"`.
- `"schema"`: The schema for the table — a list of column definitions, each with a `name` and `type`.
- `"rows"`: The data itself, as a list of lists (each inner list is a row, matching the schema order).

**Example SDML (Nightingale dataset, schema only):**
```json
{
  "type": "RowTable",
  "schema": [
    {"name": "Month_Number", "type": "number"},
    {"name": "Date", "type": "date"},
    {"name": "Year", "type": "number"},
    {"name": "Month", "type": "string"},
    {"name": "Army", "type": "number"},
    {"name": "Disease", "type": "number"},
    {"name": "Wounds", "type": "number"},
    {"name": "Other", "type": "number"},
    {"name": "Disease.rate", "type": "number"},
    {"name": "Wounds.rate", "type": "number"},
    {"name": "Other.rate", "type": "number"}
  ],
  "rows": [
    // Each row is a list matching the schema above, e.g.:
    // [1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7, 2.1],
    // ...
  ]
}

**Behavior:**

-All SDTP queries (row filters, column values, min/max) are performed in memory over this row data.

-The order of fields in each "rows" entry must match the order of the "schema" array.

-For large datasets, consider using a remote or streaming table type instead.

## 4. RemoteSDMLTable

A **RemoteSDMLTable** is a table whose data is hosted on a remote SDTP server.  
All SDTP API requests (row filters, column values, min/max) are proxied to the remote server specified in the SDML file.

**Required fields:**
- `"type"`: Must be `"RemoteSDMLTable"`.
- `"schema"`: The schema for the table (column definitions).
- `"url"`: The base URL for the remote SDTP server.
- `"name"`: The name of the table on the remote server.
- `"auth"`: (Optional) Object specifying how to retrieve authentication credentials for requests to the remote server.

### The `auth` Object

The `"auth"` field defines how the SDTP server retrieves an authentication token, if required by the remote server.  
The `auth` object must include a `"type"` and one associated parameter:

| `type` | Other Field | Description |
|--------|-------------|-------------|
| `env`  | `env_var`   | Name of the environment variable containing the bearer token. |
| `file` | `path`      | Path to a file holding the bearer token (plaintext, no line breaks). |
| `token`| `value`     | The token itself (should be used only for private deployments, not for sharing). |

When authentication is used, all requests to the remote server will include an HTTP header:  
`Authorization: Bearer <token-value>`, where `<token-value>` is retrieved according to the chosen method.

### Example SDML

```json
{
  "type": "RemoteSDMLTable",
  "schema": [
    {"name": "Year", "type": "number"},
    {"name": "Democratic", "type": "number"},
    {"name": "Republican", "type": "number"},
    {"name": "Other", "type": "number"}
  ],
  "url": "https://sdtp-data.example.com/api",
  "name": "electoral_college",
  "auth": {
    "type": "env",
    "env_var": "REMOTE_TABLE_TOKEN"
  }
}
```

### Auth Handling Examples

** env: ** 
The server will read the value of the environment variable named in env_var and use it as the bearer token.

** file: ** 
The server will read the token value from the specified file path.

** token: ** 
The token is provided directly in the SDML file. This is _not_ recommended

** Note: ** 
If the auth field is omitted, no Authorization header is sent.
Avoid embedding tokens directly (type: token) in SDML files meant for public distribution. Use env or file for secure deployments.

** Behavior: ** 

- All SDTP queries (row filters, column values, min/max) are forwarded to the specified remote table using the credentials, if provided.

- The server will return errors from the remote SDTP endpoint as-is, including authorization errors.

### RemoteSDMLTable Authentication Examples

**1. Environment Variable Token (Recommended for most deployments)**

```json
{
  "type": "RemoteSDMLTable",
  "schema": [
    {"name": "ID", "type": "string"},
    {"name": "Measurement", "type": "number"}
  ],
  "url": "https://data.example.com/api",
  "name": "experiment_results",
  "auth": {
    "type": "env",
    "env_var": "EXPERIMENT_TOKEN"
  }
}
```
_The SDTP server reads the value of the **EXPERIMENT\_TOKEN** environment variable and uses it as the bearer token for Authorization._
**2. File-based Token (Good for containerized or server deployments)**
```json
{
  "type": "RemoteSDMLTable",
  "schema": [
    {"name": "Sample", "type": "string"},
    {"name": "Result", "type": "number"}
  ],
  "url": "https://sdtp.partnerlab.org/api",
  "name": "lab_data",
  "auth": {
    "type": "file",
    "path": "/run/secrets/partnerlab_token"
  }
}
```
_The SDTP server reads the token from the specified file and uses it for Authorization.__

**3. Inline Token (For private/local-only SDML, not recommended for sharing)**
```json
{
  "type": "RemoteSDMLTable",
  "schema": [
    {"name": "PatientID", "type": "string"},
    {"name": "Score", "type": "number"}
  ],
  "url": "https://secure.healthnet.example/api",
  "name": "test_scores",
  "auth": {
    "type": "token",
    "value": "abc123XYZ-private-access"
  }
}
```
_The token value is included directly. Do not use this method for files intended for distribution._

**4. No Authentication (Public data or test systems)**
```json
{
  "type": "RemoteSDMLTable",
  "schema": [
    {"name": "Year", "type": "number"},
    {"name": "Population", "type": "number"}
  ],
  "url": "https://open-data.example/api",
  "name": "census"
}
```
_No auth field; requests are sent with no Authorization header._

**Best Practice:**
Use "type": "env" or "type": "file" for production and shared SDML.
Never embed real tokens in SDML intended for public or collaborative use.

## 5. Extensions: New Table Types (Draft)

SDML is designed for extensibility. In the future, we expect new table types to be contributed by both core and third-party developers.

**Current status:**  
- The extension architecture is *under development* and subject to change.
- At present, only `RowTable` and `RemoteSDMLTable` are fully supported.

### Draft Process for Contributing New Table Types

To add a new table type, the following draft workflow will apply:

1. **Define a new Table class**  
   - Subclass the GDP Table base class (`SDMLTable` in the Python reference server).
   - Implement all required API methods for schema, row, and column access.

2. **Write a Factory class**  
   - The factory knows how to parse the relevant SDML file/section and instantiate your Table class.

3. **Register your Table type**  
   - Register your Table and Factory with the SDTP server’s table type registry.
   - (Coming soon) Contribute your Table type to the global registry at [GDPHub.org](https://GDPHub.org) to enable ecosystem-wide discovery and reuse.

### Planned Architecture for Third-Party Contributions

We are actively working on:
- A robust naming and versioning scheme for contributed table types (e.g., using `repo/type` or `org/type` identifiers).
- A global registry and review process for contributed Table types to ensure security and interoperability.
- A plugin/extension mechanism for SDTP servers to discover, install, and serve new Table types with minimal friction.

If you are interested in contributing or have suggestions for the extension mechanism, please [contact the GDP project](https://GDPHub.org) or join the discussion in the GDPHub community.

> **Note:**  
> Until the extension mechanism is finalized, third-party Table types are experimental and may require manual integration with the SDTP server.

---

*SDML will continue to evolve to support richer and more flexible data access patterns, while keeping its core focus on clarity and composability.*

## 6. Contributors and Community

SDML and the Global Data Plane project are open to contributions, feedback, and collaboration from the community.

- **To propose changes, request features, or report issues:**  
  Please open an issue or pull request on the [SDTP GitHub repository](https://github.com/Global-Data-Plane/sdtp) (URL and instructions will be updated as the global registry comes online).

- **To contribute a new Table type:**  
  Watch for updates to the extension and registry architecture in this specification.  
  We encourage early discussion of ideas and prototypes — open an issue or start a conversation on GDPHub’s forums or chat.

- **To join the discussion:**  
  - Participate in the Global Data Plane community (https://github.com/Global-Data-Plane)
  - Share feedback, best practices, and use cases
  - Help review and evolve the SDML and SDTP ecosystem

**All contributions—code, documentation, discussion, and testing—are welcome.  
We believe open standards and collaboration are the foundation for the Global Data Plane.**

---

*Thank you for helping make SDML and GDP better for everyone!*
