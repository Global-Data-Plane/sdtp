## SDTPClient — Python Client for SDTP Table Service

## Introduction

The **SDTPClient** is a robust, extensible Python library for programmatically accessing, querying, and integrating tabular data from SDTP servers using the Global Data Plane architecture. It is designed for simplicity, composability, and seamless integration with modern security and devops workflows.

SDTPClient exposes all core SDTP REST endpoints, handles authentication via web-standard methods, and offers a full suite of helper methods for common tabular data workflows — including DataFrame integration, query/filter builders, and credential management.
It can be used interactively (notebooks, scripts), in production services, or as a backend library for analytics, pipelines, and AI partners.

---

### Authentication Overview

SDTPClient is designed for **maximum flexibility and ease of integration**.

* It builds on standard REST/web authentication: *HTTP Bearer tokens*, which work with OAuth2, API keys, JWTs, and all modern identity providers.
* **No custom auth logic is required**: Any web/REST server running SDTP can use its own existing auth layer — and the client will supply tokens, keys, or headers as needed.

**Reference Implementation**:

* Accepts requests without enforcing authentication by default. The deployer is responsible for adding security in production environments.

**Credential Handling in the Client**:

* SDTPClient can accept tokens or headers directly, via environment variables, from secure files, or via a YAML config file.
* The client never stores, issues, or validates credentials — it simply attaches them to requests as specified.

---

### Supplying Credentials: Methods & Precedence

SDTPClient supports multiple ways to provide authentication tokens/headers:

| Method          | How to Use                                                  | Example Code                                           | Use Case                          |
| --------------- | ----------------------------------------------------------- | ------------------------------------------------------ | --------------------------------- |
| Direct token    | Pass as `credential` or `auth` argument at init or per-call | `client = SDTPClient(url, credential="abc123")`        | Local, secret manager, notebooks  |
| Environment var | Set token in env var; client auto-discovers                 | `os.environ["SDTP_CREDENTIAL_VAR"] = "abc123"`         | Containers, CI/CD, notebooks      |
| File path       | Store token in file; client reads via path/env              | `client = SDTPClient(url, credential_path="~/.token")` | DevOps, servers, K8s secrets      |
| YAML config     | Map server URLs to credential methods via config            | (see below)                                            | Multi-server, ops, complex setups |
| None            | No credential; for public/trusted server or for testing     | `client = SDTPClient(url)`                             | Public/test endpoints             |

**Precedence (highest wins):**

1. Direct/explicit (per-call or client arg)
2. Environment variable (default or custom name)
3. File path
4. YAML config file
5. No credential

If multiple methods are provided, SDTPClient resolves in the above order.
Per-request credentials always override the default for that call only.

---

### YAML Config File: Credential Discovery

For robust, multi-server environments, SDTPClient supports a YAML config file (default: `~/.sdtp_client_config.yaml`). This file can specify, for each server URL (or a default fallback):

* `env`: Name of the environment variable holding the token
* `path`: Path to a file with the token
* `value`: Token value (not recommended for production)

**Example:**

```yaml
credentials:
  "https://sdtp1.example.com": { env: SDTP_API_TOKEN }
  "https://sdtp2.example.com": { path: ~/.secrets/sdtp2_token }
  "default": { env: SDTP_API_TOKEN }
```

* The client uses the credential method for the URL, or `default` if none matches.
* Env/file changes are picked up between calls.
* No secrets are written or updated by the client — only read.

---

### Per-Request Credential Overrides

While SDTPClient supports global (client-level) credentials, credentials can also be overridden for individual requests:

* **Per-call override:**
  Any API method that issues an HTTP request (e.g., `get_filtered_rows`, `get_table_schema`, etc.) accepts an `auth` or `credential` argument to supply a token for that request only.

  ```python
  # Uses global client credential (default)
  client.get_filtered_rows(table="nightingale", filter_spec=fspec)

  # Override credential for this call only
  client.get_filtered_rows(table="nightingale", filter_spec=fspec, credential="special_token")
  ```

* **Custom headers:**
  If an SDTP server expects a custom header (not just a Bearer token), the `headers` argument can be provided as a dictionary to override or supplement the default headers:

  ```python
  client.get_table_schema(table="nightingale", headers={"Authorization": "Bearer abc123"})
  ```

* **Table-level overrides:**
  If multiple tables on the same SDTP server require different credentials, separate SDTPClient instances may be used with different default credentials, or per-call overrides may be provided as shown above.

---

### Credential Resolution & Security Guarantees

SDTPClient resolves and attaches credentials according to the following precedence:

1. Per-call credential/header (explicit `credential` or `headers` argument)
2. Client default (set at initialization)
3. Config file (YAML, for URL or default)
4. Environment variable (as named in config, or `SDTP_API_TOKEN`)
5. File path (as named in config)
6. None (no credential attached)

* **No credential storage or modification:**
  SDTPClient does not write, issue, or modify credentials or config files. All files are read-only; no credential values are persisted or cached in memory.
* **No credential validation:**
  The client only attaches credentials and reports authentication errors as returned by the server. Credential validation is performed server-side.
* **Inspection:**
  For debugging, the `get_credential_method()` helper can be used to check which method would be used for a given server or table. The credential value itself is never exposed.

---

### Security Considerations

* The reference SDTP server implementation does not enforce authentication checks—it accepts all requests. Security is the responsibility of the deployer. SDTP endpoints should not be exposed to untrusted networks without proper gateway or proxy authentication.
* **Best practice:**
  Always use environment variables, secure file paths, or external credential managers for production deployments.
  Credentials should not be stored directly in code, notebooks, or YAML configs intended for distribution.
* **Production environments:**
  Container secret mounts, K8s secrets, Vault, or other system-native credential solutions are recommended.

---

### SDTPClient API Reference

#### Class: SDTPClient

##### Initialization

```python
SDTPClient(
    server_url: str,
    credential: Union[str, dict] = None,
    credential_env: str = "SDTP_CREDENTIAL_VAR",
    credential_path: str = "~/.sdtp_token"
)
```

**Arguments:**

* `server_url` (`str`): The base URL of the SDTP server.
* `credential` (`str` or `dict`, optional):

  * If a `str`, treated as a Bearer token for Authorization header.
  * If a `dict`, supplied as custom HTTP headers.
* `credential_env` (`str`, optional): Name of environment variable holding the token (default: `"SDTP_CREDENTIAL_VAR"`).
* `credential_path` (`str`, optional): Path to a file containing the credential (default: `~/.sdtp_token`).

**Resolution precedence:**
If multiple are supplied, the order is: `credential (explicit) > credential_env (env var) > credential_path (file) > no credential`.

---

##### Credential Resolution

```python
_resolve_credential(
    credential: Union[str, dict, None] = None,
    headers: Optional[dict] = None
) -> dict
```

**Arguments:**

* `credential` (`str`, `dict`, or `None`):

  * Per-request override; if provided, takes precedence over client default.
* `headers` (`dict`, optional):

  * Per-request header dictionary; if provided, is used directly and overrides all other settings.

**Returns:**

* `dict`: HTTP headers for the request.

**Notes:**

* If `headers` is provided, it is used as-is (full override).
* If `credential` is a dict, it is used as custom headers.
* If `credential` is a str, it is sent as a Bearer token.
* If no credential is found, returns `{}` (no Authorization).

---

##### Typical Usage Example

```python
# Using direct token
client = SDTPClient("https://sdtp.example.com", credential="abc123")

# Using environment variable
import os
os.environ["SDTP_CREDENTIAL_VAR"] = "abc123"
client = SDTPClient("https://sdtp.example.com")

# Using credential file
client = SDTPClient("https://sdtp.example.com", credential_path="~/token.txt")

# No credential (for public/trusted endpoints)
client = SDTPClient("https://sdtp.example.com")
```

**Per-request override:**

```python
client.get_filtered_rows("nightingale", filter_spec, credential="temp-token")
client.get_filtered_rows("nightingale", filter_spec, headers={"Authorization": "Bearer alt-token"})
```

---

##### Summary of Core Methods

| Method                                                                                                   | Purpose/Description                                     |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `get_table_names()`                                                                                      | Returns a list of available table names                 |
| `get_tables()`                                                                                           | Returns a list of all tables (as dicts)                 |
| `get_table_schema(table)`                                                                                | Returns schema for the specified table                  |
| `get_range_spec(table, column)`                                                                          | Returns min/max for the specified column                |
| `get_all_values(table, column)`                                                                          | Returns all distinct values in the column               |
| `get_column(table, column)`                                                                              | Returns all values (with duplicates) in the column      |
| `get_filtered_rows(table, filter_spec, columns=None, result_format=None, credential=None, headers=None)` | Returns filtered rows matching the query (list or SDML) |

* All methods accept optional `credential` and `headers` arguments for per-call overrides.
* Methods return native Python objects corresponding to the REST API response.
* Errors are raised as exceptions with descriptive messages.

---

#### Minimal Working Example

```python
from sdtp_client import SDTPClient

client = SDTPClient(url="https://sdtp.example.com")
tables = client.get_table_names()
schema = client.get_table_schema(tables[0])
rows = client.get_filtered_rows(table=tables[0], filter_spec={"operator": "GT", "column": "Year", "value": 2020})
```

---

### Best Practices

* **Credential management:**
  Use environment variables, container secret mounts, or secure file paths for all production secrets. Do not hardcode tokens or store them directly in code, notebooks, or YAML configuration intended for sharing.
* **Authentication enforcement:**
  The reference SDTP server does not require authentication by default; the deployer must ensure that all public or semi-public deployments are protected by an authentication gateway or proxy.
* **Separation of concerns:**
  The SDTPClient is responsible for credential discovery and transport only; all validation, rotation, and issuance of credentials is performed by the deployer’s infrastructure.
* **YAML configuration:**
  For complex deployments, a single YAML config file may define credential sources for multiple servers, with a default fallback. No secrets are written or updated by SDTPClient.
* **Audit and rotate:**
  Periodically audit credential methods and rotate tokens or keys according to organizational security policies.

---

### Error Handling and Troubleshooting

* **Missing or invalid credentials:**
  If a credential is not found or is rejected by the server, SDTPClient raises a descriptive exception. The error message will specify which credential resolution steps were attempted.
* **HTTP errors:**
  All HTTP 4xx/5xx responses are raised as exceptions with the server’s error message attached.
* **Resolution order debugging:**
  The `get_credential_method()` helper can be used to confirm which method (env, file, direct) was used for a given request.
* **Configuration issues:**
  Failure to read or parse the YAML config, or missing/invalid file paths, will result in an immediate exception with diagnostic details.
* **Recommended response:**
  The user should confirm that all required environment variables, files, and YAML entries are present and correctly formatted.

---

### YAML Configuration Example

A typical YAML config (`~/.sdtp_client_config.yaml`) might look like:

```yaml
credentials:
  "https://sdtp1.example.com": { env: SDTP1_TOKEN }
  "https://sdtp2.example.com": { path: ~/.secrets/sdtp2_token }
  "default": { env: SDTP_TOKEN }
```

* For each server URL, a credential source is specified (`env`, `path`, or `value`).
* A `"default"` entry acts as a fallback.
* Credentials are only read, never written, by the client.

---

### Contact and Support

* **Repository:** [Global Data Plane on GitHub](https://github.com/Global-Data-Plane/sdtp)
* **Documentation:** [global-data-plane.github.io](https://global-data-plane.github.io/)
* **Issue tracking:** Submit bug reports, feature requests, or questions via GitHub Issues.

---

### Summary

SDTPClient is a minimal, robust, and production-ready Python library for interacting with SDTP servers as part of the Global Data Plane ecosystem.
Credential management is flexible, secure, and web-standard; the client is designed to integrate with diverse authentication workflows and is safe for use in interactive, batch, and deployed environments.

For more details, see the full GDP documentation set and protocol references.

