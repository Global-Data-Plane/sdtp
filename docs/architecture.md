# Global Data Plane – Architecture

## Executive Summary

The Global Data Plane (GDP) architecture prioritizes clarity, portability, and simplicity. Tabular data — from small files to real-time streams — is described using SDML (Simple Data Markup Language). Queries use SDQL, an explicit and composable query language. The GDP Server exposes a REST API, designed to avoid embedding business logic or vendor-specific extensions. The architecture is structured so that developers in any language can implement or extend the protocol without hidden requirements or additional complexity.

---

## Purpose

This document describes the core architectural principles and decisions for GDP:

* **SDML** provides a declarative, minimal format for tabular data.
* **GDP Protocol** offers a transport mechanism for SDML data and metadata.

GDP is designed to enable durable, explicit tabular data exchange, emphasizing composability over built-in features or automation.

---

## Design Tenets

GDP is based on the following principles:

1. Optimize for the common case; delegate the rare.

   * Direct support for typical scenarios.
   * Advanced or infrequent use cases are implemented externally.
2. Compose platforms; avoid overloading them.

   * Each architectural layer has a narrow scope.
   * Non-essential features are handled outside the core protocol.

This approach draws on systems design traditions emphasizing separation of concerns and minimal core scope.

---

## SDML: Declarative Contract

SDML provides a contract for describing tabular data. It is not a database, runtime, or inference engine. SDML describes:

* Column names and semantic types (e.g., string, number, boolean, date, timestamp).
* Optional row data (human-readable values).
* The intended shape and semantics of the table, independent of storage or processing layer.

**Note:** Schema inference is not supported. SDML schemas are explicitly authored. Automatic inference is delegated to external tools.

---

## Protocol: Minimal Transport Layer

GDP protocol transmits SDML artifacts and metadata. It does not include:

* Remote procedure calls (RPC) or distributed execution.
* Data syncing or version control.
* Authentication, federation, or workflow orchestration.

The protocol is a minimal channel for structured data movement, not interpretation.

---

## Composability

Design trade-offs always favor composability:

* Schema inference and validation are handled externally.
* User interfaces are implemented via extensions or external applications.
* AI and LLM integrations occur via wrappers, not as part of the schema or protocol itself.

GDP remains minimal, explicit, and testable. New features are added only when they cannot be composed externally.

---

## Design Commitments

* The schema is the authoritative source of truth; it is both human- and machine-readable.
* All behaviors are explicit and documented; there is no implicit state or effect.
* The core protocol is minimal; extended features reside outside the core.
* Documentation is mandatory and should be accessible to both human and programmatic consumers.
* Clarity and transparency are prioritized above performance optimizations or feature additions.

---

## Component Overview

### Scope

The **Global Data Plane** consists of three primary components:

* **SDML**: Simple Data Markup Language (declarative schema and table definition)
* **SDQL**: Simple Data Query Language (explicit, composable query language for tabular data)
* **SDTP**: Simple Data Transfer Protocol (minimal REST protocol for moving SDML artifacts and their metadata between systems)

All three components work together to provide a durable, platform-agnostic layer for tabular data exchange. “Global Data Plane” refers to this unified abstraction. SDTP remains the protocol and API layer. SDML and SDQL are the contract and query layers, respectively.

---

### Component Boundaries

* **SDML** defines data structure, schema, and semantics.
* **SDQL** defines how queries are constructed and expressed; it is limited to explicit, composable operations and does not support procedural logic or side effects.
* **SDTP** specifies how SDML and SDQL documents are transmitted over HTTP; it exposes endpoints for sending, retrieving, and listing tables and queries.

Each component is developed and versioned independently, but all conform to the architectural principles described above.

---

### Integration Points

External features — such as validation, connectors to storage systems, or AI integration — are composed as plugins or wrappers around the core Global Data Plane APIs. No internal logic is assumed; all non-core capabilities are documented as extensions or example integrations.

---

### Summary Table

| Component | Purpose                        | Scope                         | Extensible via |
| --------- | ------------------------------ | ----------------------------- | -------------- |
| SDML      | Schema & Table definition      | Declarative, minimal contract | Plugins, tools |
| SDQL      | Query specification            | Explicit, composable, limited | Adapters       |
| SDTP      | Protocol/API for data movement | RESTful, minimal, stateless   | Extensions     |


