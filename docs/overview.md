# Global Data Plane — Overview

The Global Data Plane (GDP) is an open standard for describing, transferring, and querying tabular data using a portable JSON format and a REST API.

GDP makes it easy to share structured data between tools, teams, and environments—locally or in the cloud—without vendor lock-in or custom scripts.

## Components

- **Simple Data Markup Language (SDML):** Standard JSON-based table format.
- **Simple Data Query Language (SDQL):** Lightweight language for filtering/selecting data.
- **Simple Data Transfer Protocol (SDTP):** REST API for remote data access and queries.

## Typical Workflow

1. Describe tables with SDML (JSON).
2. Filter/query data with SDQL.
3. Move/query data via SDTP (REST API).

GDP is intended for data engineers, scientists, and analysts who work across heterogeneous systems.


##  Examples

A set of example SDML files is provided in the examples directory of the SDTP repository
(https://github.com/Global-Data-Plane/sdtp/tree/main/examples).

These examples include:

- UFO Sightings: Aggregated by country, state, year, month, and sighting type.

- US Election Data:

    - Electoral college results (1828–2020)

    - Senate and Presidential voting history, margins, and control

    - Nationwide Presidential vote totals

- Florence Nightingale's Dataset:

    - Original and summarized data tables

These files are useful for trying out SDTP features, running tutorials, and testing dashboard or analytics workflows.
For full file descriptions, see the examples/README.md.

## Example Notebooks

A set of instructional notebooks are in the sdtp repo at (https://github.com/Global-Data-Plane/sdtp/tree/main/notebooks).  
These notebooks demonstrate a varierty of applications  of the Data Plane Table abstraction, including ETL, dynamic computation, and interoperability with  tools such as  PANDAS.

### **quickstart**

- Tutorial: Creating and Saving an SDML Table from a CSV File

- Purpose: Step-by-step introduction to building your first SDML Table from a real CSV file.

- Demonstrates:

    - Loading a CSV into a table

    - Assigning schema and types

    - Saving the table to SDML for future use

    - Intended for: New users and as a reference for other workflows

### **elections_cleanse**

- Tutorial: Generating a Clean, Normalized Elections Results Table

- Purpose: Cleanses the Cook Political Report spreadsheet into a normalized elections results table.

- Demonstrates:

    - Real-world ETL (parse, normalize, fill edge cases)

    - Party name normalization (e.g., "Bull Moose" → "Progressive")

    - Construction of a columnar SDML table ready for downstream analysis

### **nightingale**

- Tutorial: Florence Nightingale’s Data: SDML Table & Summary

- Purpose: Converts Florence Nightingale’s historical dataset into an SDML table and creates a summary view.

- Demonstrates:

    - Data wrangling for historical statistics

    - Using SDML Table tools for grouping and summarizing

    - Example: mortality statistics as both raw and aggregated tables

### **presidential-history**

- Tutorial: Pivot Tables and SDML: A Case Study

Purpose: Reads the presidential elections table, uses Pandas to create a pivot table, then saves the result as an SDML table.

Demonstrates:

    - Interoperability between SDML and Pandas

    - Building pivot tables for exploratory analysis

    - Saving transformed tables back into SDML format for sharing and reuse

### **electoral_college**

- Tutorial: Serving a Table from an API, Not Static Storage

- Purpose: Shows how a Table can be dynamically generated and served from an API, rather than being a fixed list in memory.

- Demonstrates:

    - Implementing the Table interface as an API (not just a data structure)

    - “Live” tables that compute, aggregate, or fetch data on the fly

    - Example: querying, filtering, and aggregation against a dynamic, code-backed Table

Requirements for all notebooks:

- Jupyter Notebook

- sdtp (`pip install sdtp`)

(Some require Pandas or external data files as noted)
CSV Files required by the Notebooks are in notebooks/data
SDML Tables required by the Notebooks are in notebooks/tables