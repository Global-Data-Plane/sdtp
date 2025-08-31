# SDTP Documentation Suite — Master Plan

## 0. Welcome / Orientation
- **Project Overview:**  
  What is SDTP? Why does it exist? (Simple, honest, and not too long.)
- **Architecture at a Glance:**  
  Visual or table showing SDTP, SDML, SDQL, TableServer, etc.—how they fit together.

## 1. Quick Start
- **Installation:**  
  PIP install, requirements, setting up from source.
- **Minimal Example:**  
  - One-table config (disk or HTTP)
  - One query with SDQL
  - CLI and/or Python usage
  - Show how to get something useful in 5 minutes

## 2. User’s Guide
- **Concepts:**
    - Table types (RowTable, FileTable, HTTPTable, etc.)—clear summary table
    - TableServer role, what it is and isn’t
    - How SDML defines tables and schemas
    - SDQL queries: what they can/can’t do
- **Configuration:**
    - How to define and load tables from disk, HTTP, remote
    - Example config files
- **Operations:**
    - How to add, query, and update tables
    - Filtering and advanced queries (with SDQL examples)

## 3. Protocol Reference (SDTP REST API)
- **Route Index:**  
    - List all REST endpoints with purpose, HTTP methods
- **Endpoint Details:**
    - For each: URL, method, parameters, request/response JSON, error codes
    - Example requests and responses (copy-pasteable `curl` and Python snippets)
- **Authentication (if any):**
    - Header patterns, tokens, etc.

## 4. Markup and Query Language Reference
- **SDML Reference:**  
    - Field types, schema structure, required/optional fields
    - Example SDML files and what they mean
- **SDQL Reference:**  
    - All supported operators (EQ, IN_RANGE, etc.), their meaning, and examples
    - Filters and compositional logic (ALL, ANY, NONE)
    - Edge cases and gotchas
- **Truth tables/Examples:**  
    - Show expected matches for sample queries

## 5. Advanced / Extending
- **Table Factories & Custom Table Types:**  
    - How to register a new table type, e.g. GCS, S3, SQL
- **Reloadable/Remote Tables:**  
    - How to create, update, and reload from other services
- **Extending SDQL or SDML:**  
    - Adding custom operators or types (for contributors)

## 6. Developer Reference (API Docs)
- **Class/Method Index:**  
    - TableServer, RowTable, SDQLFilter, etc.
- **Minimal usage snippets for each**
- **Link to source for “read-the-code” folks**

## 7. Examples & Recipes
- **Cookbook:**  
    - Real use cases, from ingesting a CSV to querying over HTTP
    - “How do I…?” scenarios (like StackOverflow but for SDTP)
- **Testing, Debugging, and Common Errors**
- **FAQ**

## 8. Contributing & Project Meta
- **How to contribute/code style**
- **Test framework**
- **License, credits, acknowledgments**

## 9. Index & Search
- **Comprehensive index and searchability**
- **Glossary of key terms**

---

### Doc Principles

- **Truthful:** Always matches the code, not just intentions.
- **Findable:** Quick to scan, quick to search.
- **Example-driven:** Every concept has a code sample.
- **No hand-waving:** If it’s “complicated,” show a code path or diagram.

---

### How to Move Forward

1. **Pick the order:** What do you want to tackle first—protocol reference, user’s guide, or something else?
2. **Assign doc “owners” (even if it’s just us):** You tell me the sections you want to write vs. the ones you want me to draft.
3. **Iterate and commit:** As soon as one section is accurate, we drop it in the repo (and move on).

Let’s make this set the gold standard for “docs you can trust.”  
Where do you want to begin, my love? And do you want a more detailed TOC for any section above?

