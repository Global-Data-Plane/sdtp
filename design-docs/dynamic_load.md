# Future Directions: Dynamic Table Management

As SDTP deployments grow, memory usage and operational flexibility become increasingly important. While the current TableServer loads all tables at startup, the system is designed to support **dynamic loading, unloading, and reloading of tables** as a future enhancement.

## Motivation

* **Scalability:**
  For environments with hundreds or thousands of potential tables, loading all into memory may be inefficient or infeasible.
* **Operational Flexibility:**
  Ability to add or remove tables on the fly without restarting the service.
* **Resource Management:**
  Dynamically unload rarely-used tables to reduce memory footprint, or refresh tables from updated specs.

## Proposed API Extensions

* **add\_table\_from\_spec(name, load\_spec):**
  Load a table dynamically and add it to the registry.
* **unload\_table(name):**
  Remove a table from memory, optionally closing resources.
* **reload\_table(name, load\_spec):**
  Replace an existing table with a fresh version, or reload after updates.
* **refresh\_all():**
  Reconcile the current set of loaded tables with the configuration file, adding/removing as needed.

## Implementation Notes

* All load/unload logic will be encapsulated in TableServer methods;
  *external code must not touch the table registry directly*.
* Loaders and factories must be stateless and callable multiple times.
* Resource cleanup (e.g., file handles, network connections) should be supported via optional `close()` hooks on table objects.

## Example

```python
server.add_table_from_spec("new_table", load_spec)
server.unload_table("old_table")
server.reload_table("existing_table", updated_load_spec)
```

## Status

* The API structure is in place;
  dynamic table lifecycle management is slated as a near-term optimization.

---

*This design lets SDTP scale to large and dynamic environments, without sacrificing clarity or security. The current skinny, robust system can grow as needs evolve.*

---

## Next: Filters

**With the core loading/registry pattern in place, the next area to address is table filtering and query logic.**

---
