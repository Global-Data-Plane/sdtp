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

For architecture, protocol details, and usage examples, see:  
- [Quick Start](quickstart.md)
- [Architecture](architecture.md)
- [Protocol Reference](protocol.md)
