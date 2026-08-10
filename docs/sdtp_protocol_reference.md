# SDTP Protocol Reference

**Version:** 0.3 (Draft)  
**Date:** May 30, 2026  
**Authors:** Rick McGeer & Aiko  

The **Simple Data Transfer Protocol (SDTP)** is a minimal, clean REST API for exposing, querying, and retrieving tabular data described using SDML.

SDTP is intentionally **narrow**: it defines how clients discover tables, retrieve metadata, and query data. It does **not** handle authentication, complex orchestration, natural language parsing, or data movement policy — those belong in higher layers.

---

## Design Principles

- Simplicity and predictability
- Self-describing tables
- Service discovery by name
- SDQL as the intermediate query language (not user-facing)
- Agnostic to data movement, replication, and state
- Strong emphasis on backward compatibility

---

## Core Endpoints

### Discovery Endpoints

| Endpoint                    | Method | Description                                      | Status      |
|-----------------------------|--------|--------------------------------------------------|-------------|
| `GET /tables`               | GET    | Lightweight list of all tables + basic metadata  | **New**     |
| `GET /tables/{table_name}`  | GET    | Rich metadata and description of one table       | **New**     |
| `GET /get_table_names`      | GET    | Simple list of table names (legacy)              | Existing    |
| `GET /get_tables`           | GET    | All tables with full schemas                     | Existing    |

### Schema & Metadata

| Endpoint                    | Method | Description                                      | Status      |
|-----------------------------|--------|--------------------------------------------------|-------------|
| `GET /get_table_schema`     | GET    | Schema for a single table                        | Existing    |

### Column Operations

| Endpoint                    | Method | Description                                      | Status      |
|-----------------------------|--------|--------------------------------------------------|-------------|
| `GET /get_range_spec`       | GET    | Min/max values for a column                      | Existing    |
| `GET /get_all_values`       | GET    | All distinct values for a column                 | Existing    |
| `GET /get_column`           | GET    | Full column (including duplicates)               | Existing    |

### Main Query Endpoint

| Endpoint                    | Method | Description                                      | Status      |
|-----------------------------|--------|--------------------------------------------------|-------------|
| `POST /get_filtered_rows`   | POST   | Core filtered query endpoint                     | Existing    |

---

## Discovery Endpoints (New)

### `GET /tables`

Returns a lightweight directory of all available tables.

**Response:**
```json
[
  {
    "name": "monthly-revenue",
    "description": "Monthly revenue by region and product line",
    "row_count": 12480,
    "last_updated": "2026-05-01"
  }
]
```

### `GET /tables/{table_name}`

Returns rich metadata about a specific table.

**Response:**
```json
{
  "name": "monthly-revenue",
  "description": "...",
  "schema": [ ... ],
  "capabilities": ["pagination", "streaming"],
  "example_queries": [ ... ],
  "last_updated": "2026-05-01"
}
```

---

## Query Endpoints

### `POST /get_filtered_rows`

The main query endpoint.

**Request body:**
```json
{
  "table": "monthly-revenue",
  "columns": ["region", "revenue"],
  "filter": { ... },
  "result_format": "list"          // "list", "dict", or "sdml"
}
```

---

## Error Handling (New Standard)

All error responses must follow this format:

```json
{
  "error": {
    "code": "TABLE_NOT_FOUND",
    "message": "Table 'monthly-revenue-q2' was not found",
    "details": "...",
    "trace_id": "req_7f8a9b2c",
    "suggestion": "Call GET /tables to see available tables"
  }
}
```

---

## Pagination (Proposed)

Future support for continuation tokens and limit/offset will be added.

---

## See Also

* [SDML Reference](sdml_reference.md)
* [SDQL Reference](sdql_reference.md)
* [Architecture](architecture.md)
