# SDTPClient — Python Client for SDTP API

A simple, robust Python client for the SDTP Table Service — with a built-in, minimal password manager for credential management.

---

## Credential Management: How SDTPClient Handles Auth

### Credential Discovery Contract

1. **YAML Config File**
    - Default: `~/.sdtp_client_config.yaml`
    - May be overridden by the `SDTP_CLIENT_CONFIG` env var or `config_path` argument at init.
    - *Only YAML is supported.*

2. **Config Format**
    - Flat mapping of server URL → credential method.
    - Credential method is a mapping with exactly one of:
        - `env`: Name of an environment variable holding the token
        - `path`: Path to a file containing the token
        - `value`: The token value itself (not recommended except for dev/test)
    - A special `"default"` key may be included as a fallback for URLs not matched exactly.

    **Example:**
    ```yaml
    credentials:
      "https://sdtp1.example.com": { env: SDTP_API_TOKEN }
      "https://sdtp2.example.com": { path: ~/.secrets/sdtp2_token }
      "https://sdtp3.example.com": { value: "abcdefg-12345-ephemeral-token" }
      "default": { env: SDTP_API_TOKEN }
    ```

3. **Credential Lookup**
    - For each API call, the client:
        - Looks up the URL in the config.
        - Follows the method for that URL: reads from env, reads from file, or uses the value.
        - If no URL match, uses `"default"` if present.
    - *If the env var or file changes between calls, the new credential is picked up automatically.*

4. **No Writing or Updating of Credentials**
    - The client only reads credentials. It never writes or updates the config or any token source.

5. **`query_credential_method(url)`**
    - Returns the credential method (e.g., `{env: SDTP_API_TOKEN}`) for the specified URL.
    - **Never returns the secret itself — only the retrieval method.**

---

## API Methods

### Initialization

```python
client = SDTPClient(
    url: str,
    config_path: Optional[str] = None,
    auth: AuthMethod = None
)
```
- `url`: Base URL of the SDTP server.
- `config_path`: Optional path to the YAML config file (default: `~/.sdtp_client_config.yaml`).
- `auth`: Optional explicit credential for this client only (overrides config for all calls).  `

---

### Credential Management

```python
client.clear()
```
- Clears the stored credential method (reverts to config/default).

```python
method = client.query_credential_method(url: str)
```
- Returns the credential *method* (not the secret) used for the specified URL, or `None` if not configured.

---

### API Endpoints

Each endpoint mirrors the SDTP REST API. All methods accept `auth` (optional, per-call override).

**If `auth` is `None`, the client uses the config file/default logic.**  
**If `auth` is supplied, it overrides config just for that call.**

---

#### list_tables

```python
tables = client.list_tables(auth=None)
```
- Returns a list of available table names.

#### get_tables

```python
tables_with_schema = client.get_tables(auth=None)
```
- Returns all tables with their schemas.

#### get_table_schema

```python
schema = client.get_table_schema(table_name, auth=None)
```
- Returns the schema for a specific table.

#### get_range_spec

```python
range_spec = client.get_range_spec(table_name, column_name, auth=None)
```
- Returns `[min, max]` for a column.

#### get_all_values

```python
values = client.get_all_values(table_name, column_name, auth=None)
```
- Returns all distinct values in a column.

#### get_column

```python
column = client.get_column(table_name, column_name, auth=None)
```
- Returns the entire column as a list.

#### get_filtered_rows

```python
rows = client.get_filtered_rows(
    table,
    columns=None,
    filter=None,
    result_format=None,
    auth=None
)
```
- Returns filtered rows (or all, if no filter).

#### echo_json_post (debug only)

```python
echo = client.echo_json_post(payload, auth=None)
```
- Echoes back the JSON payload.

---


### Error Handling

- If a credential is required and not found, error messages will:
    - List the sources checked (URL, config, env vars, files).
    - Suggest how to fix the problem, with a sample config.

---

### Best Practices

- Store credentials in password managers or OS secret stores, not in code.
- Use the config file for per-server credential management.
- Never check credentials into version control.
- Use per-call `auth` only for temporary or one-off overrides.

---

### Example: Minimal Config File

```yaml
credentials:
  "https://sdtp1.example.com": { env: SDTP_API_TOKEN }
  "https://sdtp2.example.com": { path: ~/.secrets/sdtp2_token }
  "default": { env: SDTP_API_TOKEN }
```

---
---

## Helper (Convenience) Methods

Below are high-level helper methods designed to make the SDTP client friendlier and more powerful for real-world data workflows. These methods minimize boilerplate and help users interact with SDML tables, schemas, and SDQL filters with minimal effort.

---

### Table and Schema Helpers

**1. `make_table_schema(columns: List[Tuple[str, str]]) -> List[dict]`**  
Quickly build a table schema as a list of column/type dicts for use with the SDTP API or your own data pipelines.

```python
schema = client.make_table_schema([
    ("name", "STRING"),
    ("age", "INTEGER"),
    ("created", "DATETIME")
])
# Returns: [ {'name': 'name', 'type': 'STRING'}, ... ]
```

**2. `table_exists(table_name: str) -> bool`**  
Check if a table exists on the server (avoids errors before upload/query).

```python
if client.table_exists("employees"):
    print("Table exists!")
```

---

### Filter and Query Helpers

**3. `make_filter(operator: str, column: str, value: Any, **kwargs) -> dict`**  
Build a filter object for use in SDQL/SDTP requests.

- `operator` (str): SDQL operator, e.g. 'EQUAL', 'IN', 'IN_RANGE', etc.
- `column` (str): Column to filter
- `value` (Any): Main value (for EQUAL/IN, etc.)
- `**kwargs`: Operator-specific extras (`min_val`, `max_val`, `inclusive`, etc.)

```python
# EQUAL
filt = client.make_filter("EQUAL", column="name", value="Aiko")
# IN_RANGE
filt = client.make_filter("IN_RANGE", column="age", min_val=18, max_val=65, inclusive="both")
```

**4. `make_in_range_filter(column: str, min_val: Any, max_val: Any, inclusive: str = "both") -> dict`**  
Shortcut for the common IN_RANGE filter operator.

```python
filt = client.make_in_range_filter("score", 0, 100, inclusive="left")
```

---

### Query Body Helpers

**5. `build_filtered_rows_request(table: str, columns: List[str] = None, filter: dict = None, result_format: str = None) -> dict`**  
Construct the JSON request body for `get_filtered_rows`.

```python
body = client.build_filtered_rows_request(
    "employees", columns=["name", "age"], filter=filt, result_format="records"
)
rows = client.get_filtered_rows(**body)
```

---

### Pandas/DataFrame Helpers

**6. `get_dataframe(table: str, columns: List[str] = None, filter: dict = None, result_format: str = None) -> pd.DataFrame`**  
Query an SDTP table and return a pandas DataFrame (requires pandas installed).

```python
df = client.get_dataframe("employees", columns=["name", "age"])
```

**7. `table_to_dataframe(table_name: str) -> pd.DataFrame`**  
Download an entire table into a DataFrame.

```python
df = client.table_to_dataframe("departments")
```

---

### Credential and Config Helpers

**8. `query_credential_method(url: Optional[str] = None) -> dict`**  
Return the credential retrieval method (env/path/value) for a given URL.  
If `url` is omitted, uses this client's current URL.

```python
method = client.query_credential_method()         # for current client
method_other = client.query_credential_method("https://other.example.com")
```

**9. `reload_config()`**  
Reload the YAML config file from disk. Useful if secrets or config are changed externally while the client is running.

```python
client.reload_config()
```

---

## Contact and Support

For bugs, feature requests, or help, open an issue on the project repository.



