# SDML/SDTP Architecture

*See also: [Manifesto](manifesto.md) | [Overview](overview.md)*

---

> **Executive Summary:**  
> SDTP’s architecture is intended to support clarity, portability, and simplicity.  
> Tables, from small CSVs to real-time streams, are described using SDML.  
> Queries (SDQL) are explicit and composable.  
> The SDTP Server exposes a REST API without embedding additional logic or vendor-specific constraints.  
> The architecture is designed to allow developers in any language to implement or extend the protocol without hidden requirements or complexity.

---

## Purpose

This document outlines the core principles and architectural choices behind SDML and SDTP:  
- **SDML** (Simple Data Markup Language)  
- **SDTP** (Simple Data Transfer Protocol)  
These tools are meant to provide a declarative, minimal layer for tabular data exchange—favoring composability and durability over features and automatic behaviors.

For a broader context, including motivations and use cases, see the [Manifesto](manifesto.md).

---

## The Berkeley Way

SDML and SDTP are influenced by the following design tenets:

1. **Optimize for the common case; delegate the rare.**
   - Address typical use cases directly.
   - Leave edge cases and advanced features to external tools or layers.

2. **Compose platforms; avoid overloading them.**
   - Each layer should have a narrow, focused responsibility.
   - Secondary features are implemented outside the core.

This approach draws on design traditions from Berkeley systems research, such as RISC and the early Internet.

---

## SDML as Semantic Contract

SDML is not a runtime, database, or inference engine.  
It provides a declarative contract for describing a tabular dataset, including:

- **Schema:** Column names and semantic types (e.g., string, number, boolean, date, timestamp)
- **Rows:** Optional, human-readable data values
- **Intent:** The intended shape and meaning of a table, decoupled from its storage or processing

> **Principle:** The schema is not inferred.  
> Schemas in SDML are always explicitly authored, not derived from data. Inferring meaning is not supported in the core.

---

## SDTP as Transport Layer

SDTP provides a protocol for transferring SDML artifacts and their metadata.

It does not implement:
- RPC or distributed execution
- Syncing or change tracking
- Authentication, federation, or orchestration

SDTP is intended as a minimal, explicit channel for moving structured tables between systems (via file, API, or extension) without interpretation or implicit behavior.

---

## Composability Over Complexity

Design trade-offs are resolved in favor of composability:

- **Schema inference** and similar features are delegated to external tools that emit SDML.
- **Validation** is handled by separate plugins or services.
- **User interfaces** (e.g., spreadsheet viewers) are composed via external applications or extensions.
- **AI integration** is expected to occur through wrappers, not the core schema or protocol.

SDML and SDTP remain minimal and testable, with features added only when they cannot be composed externally.

---

## The Web vs. Xanadu

Projects with broad ambitions (like Xanadu) often do not ship because of overextension.  
The Web succeeded by limiting scope—solving one problem well and allowing other features to grow around it over time.

SDML and SDTP aim to follow this pattern: minimal initial scope, extensible by composition rather than expansion of the core.

---

## Design Commitments

- The schema is the source of truth. It should be both human- and machine-readable.
- There is no implicit or hidden behavior; all effects are explicit.
- The core remains minimal; additional capabilities are external.
- Documentation is a primary concern; contracts should be explainable to both humans and machines.
- Clarity and transparency are prioritized over optimization or feature count.

---

## Future Growth: Extension Points

SDML and SDTP are designed to evolve through external extensions, not changes to the core, including:

- Table source plugins (e.g., `from_dataframe`, `from_bigquery`)
- Validator adapters
- Natural language and LLM wrappers
- Serializers and exporters
- Viewer/user interfaces

Extensions are maintained outside the main protocol and schema definitions.

---

*Back to [Overview](overview.md) or see the [Manifesto](manifesto.md).*
