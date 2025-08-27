# Simple Data Query Language (SDQL)

SDQL is a JSON-based, intermediate query language for expressing row filters on a single table.
It is designed to be composable, backend-agnostic, and compatible with both local and remote SDTP servers.
Surface-language “sugar” (e.g., user-friendly query builders or SQL/NL translators) should target SDQL as the protocol’s canonical query representation.

---

## Operators

| Operator      | Arguments                                                                                                  | Matches                                               |
| ------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `IN_LIST`     | `column` (name), `values` (list)                                                                           | Rows where the column value is in the list of values  |
| `IN_RANGE`    | `column` (name),<br> `min_val` (optional),<br> `max_val` (optional),<br> `inclusive` (optional; see below) | Rows where the column value is in the specified range |
| `REGEX_MATCH` | `column` (name),<br> `expression` (Python regex)                                                           | Rows where the column value matches the expression    |
| `ANY`         | `arguments` (list of filters)                                                                              | Rows where *any* of the argument filters match        |
| `ALL`         | `arguments` (list of filters)                                                                              | Rows where *all* of the argument filters match        |
| `NONE`        | `arguments` (list of filters)                                                                              | Rows where *none* of the argument filters match       |

---

## Notes

* All filters except `REGEX_MATCH` are valid on all column types.
  `REGEX_MATCH` is only valid on string columns.
* `min_val` and `max_val` are both optional on `IN_RANGE` queries:

  * If `max_val` is omitted, all values ≥ `min_val` are found (subject to inclusivity).
  * If `min_val` is omitted, all values ≤ `max_val` are found (subject to inclusivity).

---

## `IN_RANGE`: Inclusivity Semantics

SDQL adopts the [Pandas](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html) convention for range endpoints.

* The `inclusive` field is **optional**.
* Allowed values:

  * `"both"` (default):    `min_val <= x <= max_val`
  * `"left"`:               `min_val <= x < max_val`
  * `"right"`:              `min_val < x <= max_val`
  * `"neither"`:            `min_val < x < max_val`
* If `inclusive` is omitted, `"both"` is assumed.

**Example:**

```json
{
  "operator": "IN_RANGE",
  "column": "score",
  "min_val": 60,
  "max_val": 80,
  "inclusive": "right"
}
```

*Matches rows where* `60 < score <= 80`.

---

## Logical Composition

You can build complex queries using `ANY`, `ALL`, and `NONE`:

**Example:**

```json
{
  "operator": "ALL",
  "arguments": [
    {
      "operator": "IN_LIST",
      "column": "state",
      "values": ["CA", "WA", "OR"]
    },
    {
      "operator": "IN_RANGE",
      "column": "sales",
      "min_val": 1000
    }
  ]
}
```

This filter matches rows where `state` is one of `["CA", "WA", "OR"]` **and** `sales >= 1000` (with both endpoints inclusive by default).

---

## Extensibility and Surface Sugar

* SDQL is intentionally minimal and explicit.
* Surface syntaxes (e.g., UI builders, NL-to-query, etc.) are expected to provide shortcuts and user-friendly features, mapping to SDQL as the canonical form.
* New operators (e.g., `EQUALS`, `IS_NULL`) can be added as needed, but should be mapped to the core primitives for consistency.

---

## Implementation & Validation

* Each operator requires specific fields.
  Implementations should validate filter specs before executing.
* For best compatibility, strictly follow the required and optional field names and types as described above.

---

## Summary Table

| Operator     | Arguments                             | Purpose                                       |
| ------------ | ------------------------------------- | --------------------------------------------- |
| IN\_LIST     | column, values                        | Membership in a value list                    |
| IN\_RANGE    | column, min\_val, max\_val, inclusive | Bounded value range with optional inclusivity |
| REGEX\_MATCH | column, expression                    | Regex match for string columns                |
| ANY          | arguments                             | Logical OR (any sub-filter matches)           |
| ALL          | arguments                             | Logical AND (all sub-filters match)           |
| NONE         | arguments                             | Logical NOR (none of the sub-filters match)   |

---

*SDQL is designed to be portable, safe, and robust—an explicit, extensible foundation for table query logic in SDTP systems.*

---
