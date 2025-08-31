## SDTP Client Authentication and Initialization

The SDTP client supports flexible, environment- and devops-friendly authentication for every deployment pattern, from local notebooks to production services.

### How Authentication Works

On client initialization, credentials can be supplied in one of four ways:

** 1. Direct Credential: **
Pass a Bearer token or API key directly:
```python
client = SDTPClient(server_url, credential="your-token-here")
```
** 2. Environment Variable: **
Set the environment variable `SDTP_CREDENTIAL_VAR` (or a custom one), and the client will pick it up:
```python
import os
os.environ["SDTP_CREDENTIAL_VAR"] = "your-token-here"
client = SDTPClient(server_url)
# or, custom variable:
client = SDTPClient(server_url, credential_env="MY_SDTOKEN")
```
** 3. File Path: **
Store your token or secret in a file, defaulting to `~/.sdtp_token` (or the value of the environment variable `SDTP_CREDENTIAL_PATH`)
```python
client = SDTPClient(server_url)
# or, custom path:
client = SDTPClient(server_url, credential_path="~/my_token.txt")
```
** 4. No Credential **
Initialization without supplying credentials is easy:
```python
client = SDTPClient(server_url)
```
** Precedence order: **
If multiple are supplied, the order is:
`credential (explicit) > credential_env (env var) > credential_path (file) > no credential`.

** Per-Request Overrides**

Permissions in SDTP are on a _per-table_ basis; as a result, credentials can be overridden on every call.

```python
client.get_filtered_rows("table", ..., credential="temporary-token")
client.get_filtered_rows("table", ..., headers={"Authorization": "Bearer ..."})  # full header override
```
If a per-request credential or header is supplied, it overrides the client’s default for that call only.

** Credential Format **

- If the credential is a **string**, it is sent as a Bearer token in the `Authorization` header.

- If it is a dict, it is used as custom HTTP headers.

- (For most common cases, use a token string.)

** Credential Resolution (Python Example)**
```python
import os

class SDTPClient:
    def __init__(self, server_url, credential=None, credential_env="SDTP_CREDENTIAL_VAR", credential_path="~/.sdtp_token"):
        self.server_url = server_url
        self.credential = None

        if credential is not None:
            self.credential = credential
        elif credential_env and os.environ.get(credential_env):
            self.credential = os.environ[credential_env]
        elif credential_path and os.path.exists(os.path.expanduser(credential_path)):
            with open(os.path.expanduser(credential_path)) as f:
                self.credential = f.read().strip()

    def _resolve_credential(self, credential=None, headers=None):
        # Per-request override: headers wins, then credential, then default
        if headers is not None:
            return headers  # user supplies full header dict
        cred = credential if credential is not None else self.credential
        if cred is None:
            return {}  # no auth
        if isinstance(cred, dict):
            return cred
        # treat as Bearer token
        return {"Authorization": f"Bearer {cred}"}
```

**Sumary Table**
| How to Supply Credential | Code Example                              | Use Case                   |
| ------------------------ | ----------------------------------------- | -------------------------- |
| Direct token             | `credential="abc123"`                     | Local, secrets manager     |
| Env var                  | `os.environ["SDTP_CREDENTIAL_VAR"] = ...` | Container, notebook, cloud |
| File path                | `credential_path="~/token.txt"`           | On-disk secret, devops     |
| None                     | (default)                                 | Public/trusted server      |
