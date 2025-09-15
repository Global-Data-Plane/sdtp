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
.

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

Sample Notebooks demonstrating how to load and analyze these files will be added to the repository soon.
