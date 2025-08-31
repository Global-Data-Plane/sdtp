# SDTP Overview

**SDTP is an open standard for describing, transmitting, and querying tabular data using a portable JSON format and a REST API.**

It is designed to make structured data straightforward to share and access, whether working with files, APIs, or cloud storage.

---

## What is SDTP?
A protocol and schema for representing, moving, and querying tabular data in a consistent way.

## Key Parts
- **[SDML](sdml_reference.md):** A markup language for describing tables, expressed in JSON.
- **[SDQL](sdql_reference.md):** A simple query language for filtering and selecting data.
- **[SDTP Server](protocol.md):** A REST server implementing the SDTP API, exposing, loading, and querying tables.

## How Does It Work?
- Define tables using [SDML (JSON)](sdml_reference.md).
- Query and move data via [REST APIs](protocol.md).
- Filter and transform tables with [SDQL](sdql_reference.md).

## Who Is It For?
- Data engineers, scientists, and analysts who work with tabular data across different tools and systems.

## Why Use SDTP?
- To provide a consistent approach to data transfer and access, without requiring custom scripts or vendor-specific solutions.

## Where Can You Use It?
- Locally, in cloud environments, or between organizations—anywhere tabular data needs to be exchanged or queried.

---

## Key Features & Concepts

- **Simplicity:**  
  Formats and protocols are intended to be clear and easy to use, both by hand and in code.

- **Remote Queries:**  
  Supports querying any SDTP-compatible server over HTTP/HTTPS using a REST API. No client library is required.

- **Easy Conversion:**  
  Data can be imported from and exported to existing formats ([JSON, CSV, XLS/XLSX, SQL databases](conversion_guide.md)).

- **Infinite Data Streams:**  
  Can be used for static tables as well as streams or live-updating sources, such as sensor data or logs.

- **Composability:**  
  Tables and queries can be composed, filtered, and combined using a text editor and JSON.

- **Extensibility:**  
  The protocol and its markup/query languages ([SDML](sdml_reference.md), [SDQL](sdql_reference.md)) are designed to support future operators, data types, and backends.

- **Transparency:**  
  All steps in data transfer and query are explicit and inspectable.

---

> **To learn about the philosophy behind SDTP, see the [Manifesto](manifesto.md).**  
> **To get started, see the [Quick Start](quickstart.md).**  
> **For technical details, see the [Protocol Reference](protocol.md).**  
> For architecture and design principles, see the [Architecture doc](architecture.md).
