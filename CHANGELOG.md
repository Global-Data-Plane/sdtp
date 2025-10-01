# SDTP 2025.09.17 Release Notes

## 🚀 What’s New

- [x] **Pydantic-based Validation**: Improved filter spec validation with helpful error messages.
- [x] **Expanded Test Coverage**: 180+ tests, with complete coverage of all filter classes and helpers.
- [x] **New Mkdocs-based Documentation**: Full documentation rewrite in mkdocs.
- [x] **Convenience SDTP Client**: New SDTPClient class for simpler queries and returns.
- [x] **Multiple Formats for get_filtered_rows** SDML and dict return types now supported. 
- [x] **Example Jupyter Notebooks** Sample Jupyter Notebooks.
- [x] **New TableBuilder Architecture**.  TableBuilder abstracts table factory classes
- [x] **Auth/env support**.  Support added for file-based and env-based authentication for individsual tables

# SDTP v2025.10.1 Release Notes

**Release Date:** 2025-10-1

## 🚀 What’s New

- [x] **Filter Helpers**: New convenience functions for SDQL filter generation (`EQ`, `NEQ`, `ANY`, etc.) simplify the API and reduce verbosity.
- [x] **Pydantic-based Validation**: Improved filter spec validation with helpful error messages.
- [x] **Expanded Test Coverage**: 190+ tests, with complete coverage of all filter classes and helpers.
- [x] **Cleaner Packaging**: No extraneous files (`app.py` excluded from wheel and sdist!).
- [x] **Documentation Improvements**: Updated SDQL reference and code comments.

## 🐞 Fixes


- [x] Smoke test now covers all filter operators.

## ⚠️ Breaking Changes

- API is now stricter about argument types and missing fields.

---

## **README: Quick Install & Example**

```sh
pip install --index-url https://test.pypi.org/simple/ sdtp
```