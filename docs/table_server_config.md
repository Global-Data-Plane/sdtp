# Configuration: TableServer

The TableServer requires a configuration file (JSON) describing all tables to be loaded, how to load them, and (if needed) how to supply authorization secrets—never directly in config.

## Table List Structure

Each config file is a list of table entries.
Each entry contains:

- `name`: Unique table identifier.
- `load_spec`: Describes where to load and how to authorize.

Example
```
[
  {
    "name": "local_table",
    "load_spec": {
      "location_type": "file",
      "path": "/data/tables/local_table.json"
    }
  },
  {
    "name": "secure_api_table",
    "load_spec": {
      "location_type": "uri",
      "url": "https://api.example.com/data",
      "auth_info": {
        "headers": {
          "Authorization": { "from_env": "API_AUTH_TOKEN" }
        }
      }
    }
  },
  {
    "name": "external_secrets_table",
    "load_spec": {
      "location_type": "uri",
      "url": "https://api.partner.com/metrics",
      "auth_info": {
        "from_file": "/run/secrets/partner_api_headers.json"
      }
    }
  }
]
```

### Supported Authorization Patterns

- *Headers from environment variables:*
```
"auth_info": {
  "headers": {
    "Authorization": { "from_env": "API_AUTH_TOKEN" }
  }
}
```
  - The environment variable must be set at runtime and contain the entire header value.

  - *Inline values are not allowed.*
- *Headers from a JSON secrets file:*
```
"auth_info": {
  "from_file": "/run/secrets/api_headers.json"
}
```
  - The file must contain a JSON object, e.g. `{ "Authorization": "Bearer abc" }`.

*Any other format or inline secrets will raise an error.*
### Security Requirements

- Never store secrets or tokens directly in config files.

- Use environment variables or restricted files for all authorization.
## Configuration Schema

| Field          | Required? | Description                              | Example                                  |
| -------------- | --------- | ---------------------------------------- | ---------------------------------------- |
| name           | Yes       | Unique table name                        | `"metrics_table"`                        |
| load\_spec     | Yes       | Where/how to load the table              | See above                                |
| location\_type | Yes       | `"file"` or `"uri"`                      | `"file"`                                 |
| path           | If file   | Path to local table spec                 | `"/data/foo.json"`                       |
| url            | If uri    | URL to remote table spec or endpoint     | `"https://api.site/data"`                |
| auth\_info     | Optional  | Authorization info for protected sources | `{ "from_file": "/run/secrets/a.json" }` |

## Example: Secrets Fiel Format
A referenced secrets file must contain a JSON dict

```
{
  "Authorization": "Bearer abc123",
  "X-Project": "demo"
}
```
