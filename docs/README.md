# Global Data Plane

The **Global Data Plane** is a set of open standards for representing, querying, and transferring tabular data between systems.

It consists of three main components:

- **Simple Data Markup Language (SDML):** A standard, JSON-based, human-readable format for describing tabular data and schemas.
- **Simple Data Query Language (SDQL):** A JSON-based minimal query language for filtering and selecting data from tables.
- **Simple Data Transfer Protocol (SDTP):** An HTTP-based protocol for querying SDML tables over the network using SDQL.

Together, these standards provide a transparent, consistent way to move and work with tabular data—across tools, teams, and environments.

This repository contains implementations and tools for all three components.

---

## Design Goals

The GDP is intended to make data publishing and access simple and transparent.

- **Simplicity:** Clarity and ease of use—edit by hand, read by eye.
- **Remote Queries:** Query any SDTP server over HTTP with plain REST calls.
- **Easy Conversion:** Move data to and from JSON, CSV, pandas, XLS/XLSX, and SQL databases.
- **Streaming Support:** Static and streaming/tabular data.
- **Composability:** Build, filter, and combine data and queries with a text editor.
- **Extensibility:** Add new operators, types, or backends as your needs grow.
- **Transparency:** Inspect and understand every data flow—no hidden magic.


---

## Contributing

Contributions are welcome!
- Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on code, documentation, and issues.
- All code and documentation changes should include clear explanations and, where possible, test coverage.
- Bug reports and feature requests are welcome via GitHub Issues.

---

## FAQ

**Q: Who is this for?**  
A: Developers, data engineers, and anyone who needs to move tabular data simply and reliably between tools or teams.

**Q: Can I use this with my existing tools and workflows?**  
A: Yes. GDP tools are designed for interoperability. You can convert to/from pandas, SQL, CSV, and other formats.


**Q: Where Can You Use It?**
- Locally, in cloud environments, or between organizations—anywhere tabular data needs to be exchanged or queried.

**Q: What software do I need to run to create an SDML Table?**
- SDML tables can be created in any text editor

**Q: What software do I need to run to create an SDQL Filter?**
- SDQL filters can be created in any text editor

**Q: What client software do I need to run to query a remote SDTP server?**
- SDTP doesn't require any client software: any HTTP/HTTPS requests library (e.g., Python `requests`, the utility `curl`) can be used.  The package provides a convenience client, but this isn't required.

**Q: Can SDTP be implemented on a standard HTTP Server?**
- SDTP is a set of routes that can be implemented by any HTTP Server

**Q: Where and how are SDML Tables stored?**
- SDML and SDQL _do not imply any implementation_.  An SDML Table is an abstract, not concrete, artifact; it is the data equivalent of a software API.  It simply declares that each record is of the lengths and types of the schema, and that it will deliver matching rows in response to an SDQL Query.  In the package, we offer two standard SDML Tables -- a RowTable, where the rows are physically present in the table structure, and a RemoteSDMLTable, where the table is hosted at a remote SDTP Server.

