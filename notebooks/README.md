# Example Notebooks


These notebooks demonstrate a variety of applications  of the Data Plane Table abstraction, including ETL, dynamic computation, and interoperability with  tools such as  PANDAS.

## **quickstart**

- Tutorial: Creating and Saving an SDML Table from a CSV File

- Purpose: Step-by-step introduction to building your first SDML Table from a real CSV file.

- Demonstrates:

    - Loading a CSV into a table

    - Assigning schema and types

    - Saving the table to SDML for future use

    - Intended for: New users and as a reference for other workflows

## **elections_cleanse**

- Tutorial: Generating a Clean, Normalized Elections Results Table

- Purpose: Cleanses the Cook Political Report spreadsheet into a normalized elections results table.

- Demonstrates:

    - Real-world ETL (parse, normalize, fill edge cases)

    - Party name normalization (e.g., "Bull Moose" → "Progressive")

    - Construction of a columnar SDML table ready for downstream analysis

## **nightingale**

- Tutorial: Florence Nightingale’s Data: SDML Table & Summary

- Purpose: Converts Florence Nightingale’s historical dataset into an SDML table and creates a summary view.

- Demonstrates:

    - Data wrangling for historical statistics

    - Using SDML Table tools for grouping and summarizing

    - Example: mortality statistics as both raw and aggregated tables

## **presidential-history**

- Tutorial: Pivot Tables and SDML: A Case Study

Purpose: Reads the presidential elections table, uses Pandas to create a pivot table, then saves the result as an SDML table.

Demonstrates:

    - Interoperability between SDML and Pandas

    - Building pivot tables for exploratory analysis

    - Saving transformed tables back into SDML format for sharing and reuse

## **electoral_college**

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
CSV Files required by the Notebooks are in data
SDML Tables required by the Notebooks are in tables