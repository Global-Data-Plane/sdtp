# SDQL Reference (Simple Data Query Language)

SDQL (Simple Data Query Language) is a minimal, portable query language for filtering and selecting rows and columns from tabular datasets. SDQL is designed for composability, explicitness, and ease of use with the SDTP protocol and SDML table format. It is not intended as a replacement for SQL; instead, it provides a straightforward and interoperable way to express data filters in JSON.

It is rare that a user will want to download or examine an entire SDML Table.  In fact, in some sense, at-source filtering is the entire point of SDTP, and for some tables, downloading the entire table is impossible.  SDML Tables are logical, not physical, entities.  For example, a Solar System simulation takes in the initial positions, velocities, and masses of the planets as initial conditions and reports their positions and velocities at arbitrary times in the future.  An SDML Table representing the Solar System has a column for each planet's position, velocity, and mass, and a column for time.  Runs of the simulator are triggered by SDQL queries, which specify the initial conditions and request the values for specific ranges of time.  But the "table" itself is infinite, or large enough that it can be treated as such; only finding rows that match specific time periods makes sense.

SDQL is designed to be lightweight and simple.  When the Structured Query Language (SQL) was designed, it was assumed that no computation outside SQL was done, and as a result, SQL was designed to be a full-featured compute engine.  SDQL has a different set of design assumptions; it assumes that the query agent is a program, and the results of the SDQL query will be inputs to further computation on the client side.  As a result, SDQL's sole operation is to return the data of interest to the follow-on computation operation.  Moreover, much of SQL (for example) is devoted to creating conjoined tables on the fly (this is the principal function of the `JOIN` operation).  Since the Global Data Plane's tables are *semantic*, not *physical*, entities, this is done server-side and isn't exposed in the query language. The sole function of SDQL is to *filter* and provide summary information on tables.

---

## Design Principles

* **Explicitness:** No implicit conversions or behaviors; filters are explicit and fully described in the query object.
* **Portability:** All SDQL filters are described using plain JSON; no language-specific syntax or vendor extensions.
* **Composability:** Filters may be nested using logical operators (ALL, ANY, NONE) for complex queries.
* **Minimalism:** SDQL exposes only a small set of operators, enabling straightforward implementation and static validation.

---

## SDQL and SQL

SDQL can be intuitively thought of as the `WHERE` clause of a SQL select statement; and, indeed, any SQL clause can be realized as a specialization of a SDQL operator or by a combination of SDQL operators.  For example, the SQL `=` operator is the SDQL operator `IN_LIST` where the `values` list argument is a single list; e.g. `Category = 'Electronics'` is realized in SDQL as `{"operator": "IN_LIST", "column": "Category", "values":["Electronics"]}`.

## SDQL Filter Object Structure

SDQL is an *intermediate* form for queries, designed to support a wide range of surface syntaxes and encoding in POST http request bodies. Each SDQL filter is a JSON object with an `operator` key and operator-specific arguments.

### Example: Membership in a value list

```json
{
  "operator": "IN_LIST",
  "column": "Month",
  "values": ["Jan", "Feb", "Mar"]
}
```

### Example: Value >= a minimum

```json
{
  "operator": "GE",
  "column": "Disease",
  "value": 1000
}
```

---

## Supported Operators

SDQL Row queries are designed to filter rows of the table; the result of an SDQL row query is the set of rows which match the condition.  Effectively, it operates as a *simple* form of a SQL `WHERE` clause.  There are currently **nine** supported operators:

| Operator     | Arguments                    | Purpose                                     | SQL Analog                                                                                                  |
| ------------ | ---------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| IN\_LIST     | column, values               | Membership in a value list                  | `<column> = values[0] OR <column> = values[1]...`                                                           |
| GE           | column, value                | column value >= value                       | `<column> >= value`                                                                                         |
| LE           | column, value                | column value <= value                       | `<column> <= value`                                                                                         |
| GT           | column, value                | column value > value                        | `<column> > value`                                                                                          |
| LT           | column, value                | column value < value                        | `<column> < value`                                                                                          |
| REGEX\_MATCH | column, expression           | Regex match for string columns              | `LIKE`                                                                                                      |
| ANY          | arguments (array of filters) | Logical OR (any sub-filter matches)         | `OR`                                                                                                        |
| ALL          | arguments (array of filters) | Logical AND (all sub-filters match)         | `AND`                                                                                                       |
| NONE         | arguments (array of filters) | Logical NOR (none of the sub-filters match) | `NOT( OR )` (`NOT` if the `arguments` parameter is a list of length 1) — e.g. `NOT A` or `NOT (A OR B ...)` |

---

## Logical Composition

SDQL supports composition using the following logical operators:

* `ALL`: All sub-filters must match (logical AND)
* `ANY`: At least one sub-filter must match (logical OR)
* `NONE`: No sub-filters must match (logical NOR)

### Example: Months in 1855 with less than 200 deaths by wounds

```json
{
  "operator": "ALL",
  "arguments": [
    { "operator": "IN_LIST", "column": "Year", "values": [1855] },
    { "operator": "LE", "column": "Wounds", "value": 200 }
  ]
}
```

---

## Result Format

* **Row queries** (e.g., `/get_filtered_rows`): Returns a JSON list of dicts (one per row), or list of lists if columns are not named. Actual return format may depend on the SDTP endpoint implementation and query parameters.

---

## Example Filters (Nightingale Dataset)

### Get all months where deaths by disease exceeded 2000

```json
{
  "operator": "GT",
  "column": "Disease",
  "value": 2000
}
```

### Get months in 1855 with less than 200 deaths by wounds

```json
{
  "operator": "ALL",
  "arguments": [
    { "operator": "IN_LIST", "column": "Year", "values": [1855] },
    { "operator": "LT", "column": "Wounds", "value": 200 }
  ]
}
```

### Get all rows where Month is "Jan", "Feb", or "Mar"

```json
{
  "operator": "IN_LIST",
  "column": "Month",
  "values": ["Jan", "Feb", "Mar"]
}
```

---

## Extensibility and Implementation

* SDQL is designed for extension; new operators may be added for project-specific or backend-specific purposes.
* Unknown or invalid operators should result in a validation error.
* All SDQL objects are intended to be static and inspectable; dynamic or computed operators are discouraged in the base protocol.

---

## Operator Summary Table

| Operator     | Arguments                    | Purpose                                     |
| ------------ | ---------------------------- | ------------------------------------------- |
| IN\_LIST     | column, values               | Membership in a value list                  |
| GE           | column, value                | Column value >= value                       |
| LE           | column, value                | Column value <= value                       |
| GT           | column, value                | Column value > value                        |
| LT           | column, value                | Column value < value                        |
| REGEX\_MATCH | column, expression           | Regex match for string columns              |
| ANY          | arguments (array of filters) | Logical OR (any sub-filter matches)         |
| ALL          | arguments (array of filters) | Logical AND (all sub-filters match)         |
| NONE         | arguments (array of filters) | Logical NOR (none of the sub-filters match) |

---
## SDQL Filter Construction in Python

To make SDQL filters easy to build in code (and avoid manual JSON/dict construction), use the provided high-level helper functions. These generate SDQL-compliant filter dicts for all standard operators, including value normalization (e.g., dates to ISO strings).

```
from sdtp_filter import IN_LIST, EQ, GE, REGEX, ANY

# IN_LIST (membership in a value list)
spec1 = IN_LIST("status", ["active", "pending"])
# result: {"operator": "IN_LIST", "column": "status", "values": ["active", "pending"]}

# EQ (single-value equality)
spec2 = EQ("user_id", 42)
# result: {"operator": "IN_LIST", "column": "user_id", "values": [42]}

# GE (greater than or equal) supports date/datetime/time and will normalize to ISO string
from datetime import date
spec3 = GE("created", date(2024, 4, 10))
# result: {"operator": "GE", "column": "created", "value": "2024-04-10"}

# REGEX (pattern match)
spec4 = REGEX("email", r".+@example.com")
# result: {"operator": "REGEX_MATCH", "column": "email", "expression": r".+@example.com"}

# Logical composition (ANY): pass a list or multiple filters as varargs
spec5 = ANY([spec2, spec4])   # as a list
spec6 = ANY(spec2, spec4)     # as varargs
# result: {"operator": "ANY", "arguments": [{"operator": "IN_LIST", "column": "user_id", "values": [42]}, {"operator": "REGEX_MATCH", "column": "email", "expression": r".+@example.com"} ]}

# Logical composition (ANY): pass a list or multiple filters as varargs
spec7 = ALL([spec2, spec4])   # as a list
spec8 = ALL(spec2, spec4)     # as varargs
# result: {"operator": "ALL", "arguments": [{"operator": "IN_LIST", "column": "user_id", "values": [42]}, {"operator": "REGEX_MATCH", "column": "email", "expression": r".+@example.com"} ]}

# Logical composition (ANY): pass a list or multiple filters as varargs
spec9 = NONE([spec2, spec4])   # as a list
spec10 = NONE(spec2, spec4)     # as varargs
# result: {"operator": "NONE", "arguments": [{"operator": "IN_LIST", "column": "user_id", "values": [42]}, {"operator": "REGEX_MATCH", "column": "email", "expression": r".+@example.com"} ]}

# Not Equal
spec11 = NEQ('name', 'Mike')
# result {"operator": "NONE", "arguments": [{"operator": "IN_LIST", "column": "name", "values": ["Mike"]}]}

# All helpers return plain dicts ready for SDTP/SDML or JSON serialization
print(spec1)
# {'operator': 'IN_LIST', 'column': 'status', 'values': ['active', 'pending']}

print(spec3)
# {'operator': 'GE', 'column': 'created', 'value': '2024-04-10'}
```

### Automatic Date/Datetime Normalization

When you use these helpers, all `date`, `datetime`, or `time` values are automatically converted to ISO-format strings before inclusion in the filter dict. This ensures filters are always compatible with SDTP servers and JSON APIs.

### Best Practices & Gotchas

Always use helpers. Do not manually construct SDQL filter dicts—helpers handle normalization, argument naming, and future-proofing.

Composite filters (`ANY`, `ALL`, `NONE`) accept either a list of filters or multiple filters as arguments, e.g., `ANY(EQ('y', 3), LT('z', 5))` returns the same result as `ANY([EQ('y', 3), LT('z', 5)])`.

Mixing models and dicts: Helpers always output dicts; never mix Pydantic models or non-serializable objects in composite arguments.

Helpers are guaranteed to match the SDQL spec as documented above. If you ever need to implement a custom filter, use the same field names and normalization rules as the helpers.

Validation: All helpers return filter dicts that can be validated or passed directly to SDMLTable, SDTP, or related APIs.

## See Also

* [SDTP Protocol Reference](sdtp_protocol_reference.md)
* [SDML Reference](sdml_reference.md)
* [Architecture](architecture.md)


