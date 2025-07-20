# The SDML/SDTP Manifesto

*Rick McGeer & Aiko · Global Data Plane · 2025*

---

## ❗️The Problem

Data sucks.

Not the data itself — the handling of it. The *formatting*. The *semantics*. The *lack of standards*. The endless slog of cleaning, reshaping, and reinterpreting it just to do something simple — like plot a graph or feed a model or publish a dashboard.

We live in a world where:

- Scientific instruments emit gigantic Excel files
- JSON and CSV formats have no shared conventions
- Metadata is buried in random rows or filenames
- Schemas are guessed, not declared
- Tables can’t be read without writing code
- Moving a dataset between systems is an act of hope

Even sophisticated users — engineers, analysts, researchers — spend **hours** just trying to figure out what a table *means*. What are the columns? What are the types? Is this a timestamp or a float? What’s the unit? Where’s the data provenance?

This isn’t science. This isn’t productivity.  
This is the tragedy of missing structure.

---

### 💾 The Whole Damn Thing

Here’s another deep flaw: **you usually have to grab the *entire* dataset just to do anything useful with it**.

There’s no semantic indexing. No clean query interface. No declarative slice that says, *“Just give me these rows with this shape.”* So whether it’s a 200KB file or a 200GB dump, you’re stuck pulling the whole thing, just to figure out what’s even in there.

And if the dataset updates? Good luck. Now you're dealing with versioning, diffing, partial regeneration, and keeping local and upstream copies in sync — all without a standard for **how to represent the table in the first place**.

This isn’t just inefficient. It’s brittle, redundant, and wrong.  
And we've all silently agreed to live with it.

But we shouldn't.

---

## 🌍 Why This Matters

We are drowning in data — and starving for **meaning**.

More than half the time spent on AI, science, and engineering is wasted on **just getting the data to behave**. Not modeling. Not visualizing. Not discovering. Just parsing, formatting, inferring, guessing.

This is why.

We’re living in a world where “structured data” has no structure that anyone can count on. And it’s wrecking our ability to share, reuse, and collaborate.

So we’re building something better.

---

## 🧭 What Good Design Looks Like

We've learned from the best systems in history — not because they were complex, but because they were *right-sized*, beautifully hackable, and easy to adopt. Here are three principles we hold close — and how we apply them.

### 📐 1. Canonize existing practice
Data wears many costumes, but semantically it’s always a **table**: a sequence of fixed-shape records. Whether it comes from a CSV, a JSON array, a SQL join, a log stream, or a database view — underneath it all is a table.

**SDML doesn’t invent that. It blesses it.**  
We accept the universal shape and make it explicit, minimal, and clear.

*How we apply it:* SDML formalizes this universal table as a simple, readable contract. We define the schema by hand, not inference — because meaning is too important to guess.

---

### 🛠 2. Live off the land
Good systems don’t build everything from scratch. They thrive by leveraging what’s already out there.

Tim Berners-Lee built the Web on top of TCP/IP, and repurposed existing protocols like FTP and Gopher. Mic Bowman once said the original HTTP server was nine lines of shell script over `ftp`. Even if that’s apocryphal, the first production server was only ~3,000 lines of C. That’s **not** a moonshot — that’s just clean plumbing.

*How we apply it:* SDTP uses **HTTP/HTTPS as its transport layer**, and **JSON as the wire format**. We can't do better — and if we tried, we’d surely make an impressive mess. This way, we inherit decades of tooling, security, monitoring, caching, and access control — including cookies and bearer tokens. The wheel already rolls. We don’t rebuild it. We ride it.

---

### 🪶 3. Make it stupid-easy to adopt
The early Web spread because anyone could publish. You only needed a text editor and five or six tags:
```html
<html>, <body>, <h1>, <p>, <a>, <ul>, <li>
```
You could get a page online in ten minutes. No framework. No runtime. No tutorial series.

How we apply it: You can convert a CSV or XLSX file to an SDML table using nothing more than a plain-text editor or an AWK script. (Yes, AWK still works. Remind us to tell you the Brian Kernighan story.) Want to serve it? Just add a few routes to a Flask, FastAPI, or Node.js server — or drop in our reference implementation and go.

We want SDML to feel the way the Web did in 1993:
Write a table. Save it. Use it.
No guesswork. No mystery. No build system.
Just clarity.

---

### 👥 4. Make it AI-ready
Data used to be produced by humans and their instruments, and consumed by humans. Today, AIs are full partners in data production and analysis — and a well-matched human/AI team is a marvel of productivity.

That changes the design target.

We need formats that are friendly to both humans and machines — easy to read, easy to generate, and semantically clear.

This isn’t theoretical. It’s already happening:
When AIs and humans collaborate on documents, they often use Markdown — because it provides structure without noise. It’s readable, editable, and semantically expressive without requiring a visual layout engine.

SDML brings that same clarity to tabular data.
It’s compact and declarative for machines.
It’s readable and writable for humans.

It’s the shared surface where both can think clearly — and think together.
---
### 📜 5. The Data Equivalence Principle
In data science, queries and results should be independent of the data source.

The Data Equivalence Principle says that whether you’re pulling data from a database, an API, a flat file, or an IoT sensor — the experience should be the same. No source should reveal itself through the query interface.

This echoes the Equivalence Principle of General Relativity — how all sources of acceleration are equivalent. In physics, it means that no experiment can distinguish between uniform acceleration and gravitational fields. Similarly, in data, the user should never be able to tell where the data came from. They should only see the result, with no regard for whether the data resides in a CSV, a relational database, or a distributed data lake.

This principle is critical for usability, scalability, and trust. It means that systems using SDML and SDTP will work in any context, with no extra work or complexity for the user. They just query the data. It just works.

## The Design : How SDML and SDTP Reflect Our Principles
🧠 SDML: A Simple Data Format
At its core, the Simple Data Markup Language (SDML) was designed to be a simple way to  represent tabular data. This simplicity directly aligns with our design principles of clarity and minimalism.

This is best illustrated in a sample table, which we show here:
```
{
  "type": "RowTable",
  "schema" : [{ "name": "name", "type": "string" }, { "name": "age", "type": "number" }, { "name": "last_birthday", "type": "date" }, { "name": "preferred_break_time", "type": "timeofday"}, { "name": "last_bus_ride", "type": "datetime" }, { "name": "likes_apples", "type": "boolean"} ],
  "rows": [
      [ "Pearla", 64, "2020-09-24", "11:24:55", "2020-09-24T11:24:55", true ],
      [ "Karleen", 78, "2011-12-09", "13:40:27", "2011-12-09T13:40:27", true ],
      [ "Bathsheba", 79, "2010-08-07", "23:44:12", "2010-08-07T23:44:12", true ],
      [ "Casi", 13, "2021-10-17", "17:13:02", "2021-10-17T17:13:02", true ],
  ]
}
```
This represents a very simple table, with six columns (name, age, last_birthday, preferred_break_time, last_bus_ride, likes_apples) and types (string, number, date, timeofday, datetime, boolean), and four rows. The table type indicates how the rows are obtained. In the case of a RowTable, as specified here, the rows are physically present in the JSON structure.

Structure:
An SDML table is a JSON structure with two required fields: a static list of columns and a table type. Each column is a pair: name and type. The type of a column is semantic. The table type indicates how the rows are obtained. Many table types require additional fields. For instance, a RowTable requires a rows field.

Minimality:
SDML requires only a specification of the names and types of columns and the table type. Specific types may require additional parameters. There is a clean separation between the schema of the data and the data itself: the schema is explicitly represented in its own field. There is no specification of metadata, though table authors are free to supply this in additional fields.

Static Set of Columns:
By defining columns explicitly, there’s no ambiguity about the data structure. It’s simple, clear, and consistent — a reflection of the principle that we canonize existing practice.

Extensible, General Interface to Get Data:
The central idea is that SDML doesn't require specification of a table format, or indeed local storage of tables. For example, a RemoteSDMLTable doesn't have a rows field (the rows aren’t stored locally); instead, it has a required url field, with the address of the remote SDTP server, and, potentially, the authentication information required to access the remote table.

Simple, Semantic Type System:
We use basic, semantic types — strings, booleans, numbers, datetime, date, and timestamp — to provide maximum flexibility to implementing systems to store or generate data.

🔍 SDQL: A Structured Data Query Language

The Structured Data Query Language (SDQL) sits at the heart of the data access layer, enabling expressive queries over SDML-formatted data with minimal complexity and no assumptions about data storage. SDQL is intentionally simple, composable, and storage-agnostic, designed to work equally well with flat files, remote endpoints, live database-backed services, simulators, sensor arrays, or other systems

### Key Principles of SDQL

No Constraints on Storage or Generation.  SDQL imposes no requirements on how the data is stored or generated. There is no concept of joins, nested queries, or dependencies on table relationships. Instead, SDQL defines a filter expression that is applied to an SDML table, regardless of its underlying representation.

Minimalism and Simplicity.   The core language is extremely small. Filters include simple relational operations (is the value in this column in a given list of values, is the value between these two values, does the value match this regular expression) and  logical operations (all, any, none), the equivalent of (and, or, not). Range queries are always inclusive, by design. More complex semantics can be composed from these simple building blocks.

Compositional Query Logic. Every SDQL query is a logic tree. Leaf nodes are basic predicates, and interior nodes are logical operators (all, any, none). This structure makes it easy to build complex queries out of smaller pieces and to serialize them for transmission over SDTP or storage in config files.

Intermediate Representation. SDQL is defined first as a structured intermediate representation (a JSON object). This means it can be rendered in multiple surface syntaxes: CLI-style, GUI filter builders, or natural language. This design keeps the query semantics consistent across different user interfaces or access modes.

### Example SDQL Query

This SDQL filter selects all rows where age is greater than 21 and likes_apples is true:
```
{
  "operator": "ALL",
  "args": [
    {
      "column": "age",
      "operator": "IN_RANGE",
      "min_val": 21,
      "max_val": 99
    },
    {
      "column": "likes_apples",
      "operator": "IN_LIST",
      "val": [true]
    }
  ]
}
```

This JSON representation is the canonical intermediate form of SDQL. It can be compiled to and from surface syntaxes including:

-  CLI query: age in 21..99 AND likes_apples = true

- A visual builder where filters are chosen by dropdown

- ### A natural-language interface: "Show me everyone between 21 and 99 who likes apples."

Summary

SDQL is designed to:

- Work across all storage backends and transport layers
- Be easily composed, serialized, and translated
- Keep semantics consistent across all query interfaces
- Reflect our principles of minimalism, clarity, and adaptability

It is not a general-purpose query language. It’s a purpose-built filter engine, optimized for querying structured data in a distributed, format-agnostic way.


### 🌐 SDTP: The Structured Data Transport Protocol

The **Structured Data Transport Protocol (SDTP)** provides a minimal, JSON-over-HTTP interface for querying SDML tables using SDQL filters. It is designed to be simple, scalable, secure, and easy to implement — a lightweight layer that lives directly on top of HTTP or HTTPS.

SDTP is a REST API designed to support the **Structured Data Query Language**. Its principal method, `get_filtered_rows`, sends a table name and an SDQL filter, and receives in return the list of rows of that table matching the filter. If no filter is supplied, `get_filtered_rows` returns all the rows of the table.

In future versions, this method will return a `RowTable` — a full SDML object including schema and filtered rows — rather than just a raw list of rows. This aligns better with the **Data Equivalence Principle** and enables downstream composition. For now, the reference implementation returns only the list of rows.

This reflects a central design principle: **live off the land** — make use of what the web already gives us.

#### Core Principles of SDTP

1. **Minimal Transport Layer**
   SDTP uses HTTP(S) as its transport protocol and JSON as its wire format. There is no need for new infrastructure, encodings, or protocols. Every existing web framework and HTTP client can serve or consume SDTP endpoints.

2. **Few Entry Points**
   An SDTP Server must implement only seven routes:

   * `get_table_names`: returns the list of all table names hosted on this server
   * `get_tables`: returns the schemata of all tables hosted on this server
   * `get_table_schema`: returns the JSON SDML schema of the specified table
   * `get_range_spec`: returns the minimum and maximum values of the specified column on the specified table
   * `get_all_values`: returns the unique values of the specified column on the specified table
   * `get_column`: returns the values of the specified column on the specified table
   * `get_filtered_rows`: returns the rows of the specified table which match the specified filter, or all rows if no filter is specified

3. **Authentication**
   Authentication and access control aren't specified by the protocol. Implementations are free to choose authentication and access methods. Popular schemes include that supported by the reference implementation: bearer tokens. In various cases (notably where an SDTP Server is implemented as a JupyterHub Service), OAuth is supported.

4. **Data Equivalence**
   The SDTP interface is identical regardless of the backend — whether data is stored in a local CSV, a remote Postgres database, a simulation, or a real-time sensor. Clients cannot tell how or where the data is stored. This is the **Data Equivalence Principle** in action.

5. **Security and Access Control**
   SDTP inherits security features from the web. Authentication and authorization can be handled via bearer tokens, session cookies, OAuth flows, or mTLS — all without requiring custom protocol machinery.

#### Example: Querying a Remote Table

To query a remote table, a client sends a POST request to the SDTP endpoint:

```http
POST /get_filtered_rows HTTP/1.1
Host: data.example.com
Content-Type: application/json

{
  "table": "customers",
  "filter": {
    "operator": "ALL",
    "args": [
      { "column": "country", "operator": "IN_LIST", "val": ["CA", "US"] },
      { "column": "active", "operator": "IN_LIST", "val": [true] }
    ]
  }
}
```

The server responds with matching rows:

```json
[
  [ 1, "Alice", "CA", true ],
  [ 3, "Carlos", "US", true ]
]
```

In future versions, the same query will  yield:

```json
{
  "type": "RowTable",
  "schema": [
    { "name": "id", "type": "number" },
    { "name": "name", "type": "string" },
    { "name": "country", "type": "string" },
    { "name": "active", "type": "boolean" }
  ],
  "rows": [
    [ 1, "Alice", "CA", true ],
    [ 3, "Carlos", "US", true ]
  ]
}
```

#### Summary

SDTP provides:

* A thin, composable, language-independent query interface
* Compatibility with any web stack and secure transport
* Uniform access to data regardless of source
* A foundation for scalable, federated structured data systems

SDTP is designed to make data access easy to adopt, easy to implement, and easy to scale, while maximally leveraging existing infrastructure.


🛠 How They Reflect Our Design Principles
Data Extraction Without Guesswork: SDML is designed to simplify  how data is defined, and remove the ambiguity in formats like CSV or JSON, while maintaining maximal consistency with existing practice.  In particular, the data rows of a CSV table translate directly to
the rows of a RowTable.

Seamless Interoperability: Whether connecting to legacy systems, modern APIs, or AI platforms, SDML and SDTP are designed to  support diverse data sources in a unified, predictable way to ensure  compatibility and ease of integration.

Scalability Through In-Situ Querying: Enabling data to be queried directly on the server or near the data source, is designed to  eliminate unnecessary data transfer, improving efficiency and scalability. This approach aligns with our design principle of making it easy to scale.

User Transparency: With SDML and SDTP, the data format stays consistent, no matter the source. This removes reliance on any particular data architecture, following the Data Equivalence Principle — users query the data without needing to understand the underlying source.

In summary, SDML, SDQL  and SDTP are designed to  align with our guiding principles by providing clarity, efficiency, and interoperability across data sources. These tools are designed to  make it easier for users to interact with data and work across systems, all while maintaining flexibility and scalability for future growth.

