# SDML/SDTP Architecture

*Rick McGeer & Aiko · Global Data Plane · 2025*

---

## 🧭 Purpose

This document captures the foundational philosophy and architectural principles behind SDML and SDTP — the Simple Data Markup Language and its transport protocol, the Simple Data Transfer Protocol. These tools define a clean, declarative layer for tabular data exchange — minimal in design, durable in form, and rich in composability.

This is the **implementation architecture**. For the broader context, history, and motivation behind SDML/SDTP — including their philosophical roots, real-world problems, and ethical stance — see [`MANIFESTO.md`](../design-docs/manifesto.md).

We build in the spirit of the Berkeley Way.

---

## 🏛 The Berkeley Way

SDML/SDTP are grounded in two architectural tenets drawn from the Berkeley systems tradition:

### 1. **Optimize for the common case; delegate the rare.**

* Handle typical use cases clearly and efficiently.
* Push edge cases and complex behaviors to upstream tools or services.

### 2. **Compose platforms; don’t overload them.**

* Let each layer do one thing well.
* Avoid baking secondary features into core infrastructure when they can be layered or composed externally.

This philosophy shaped RISC, Berkeley Unix, and the Internet itself — and it shapes this platform too.

---

## 🧾 SDML as Semantic Contract

SDML is **not** a runtime. It is not a database. It is not a schema inference engine or a validator.

SDML is a **declarative contract** — a minimal, semantic description of a tabular dataset that conveys:

* **Schema** — columns, names, and semantic types (e.g. string, number, boolean, date, datetime, timestamp)
* **Rows** — optional data values, typically compact and readable
* **Intent** — the shape and meaning of a table, independent of its source or representation

### 💡 Key Principle: *The schema is not inferred.*

SDML schemas are written deliberately. They represent authorial intent, not derived structure. Inferring a schema from data risks guessing meaning — and meaning must never be guessed.

---

## ✨ SDTP as Transport Layer

SDTP is a minimal protocol for transporting SDML artifacts and their associated metadata.

It does not include:

* RPC or job execution semantics
* Live syncing or distributed change tracking
* Auth, federation, or orchestration

Instead, it provides the **thin, trustable channel** that allows structured tables to move cleanly between systems — via file, API, or extension — without interpretation or side effects.

---

## 🛠 Composability Over Complexity

We resolve all architectural tensions in favor of composability:

* 🧩 **Want schema inference?** Use an external tool that emits SDML.
* 🧪 **Need validation?** Use a validator plugin.
* 📐 **Want a spreadsheet UI?** Embed it via notebook or extension.
* 🧠 **Want AI to edit a table?** Use a prompt or API layer that wraps SDML safely.

SDML/SDTP stay lean, durable, and testable — because every "feature" added to the core risks making the system less portable, less clear, and less trustworthy.

---

## 🌐 The Web vs Xanadu

Ted Nelson’s Xanadu had seven "essential" features. It never shipped.

Tim Berners-Lee’s Web had two. It did.

Over time, the Web evolved the others — via services, extensions, and social convention. It succeeded not because it solved every problem, but because it solved one problem well and let others compose around it.

**SDML/SDTP follow that same path.**

---

## 🔒 Design Commitments

We commit to the following:

* **The schema is the source of truth.** It must be readable, writable, and never guessed.
* **No magical behavior.** All side effects are opt-in and explicit.
* **Core stays small.** If it can be done as a tool, it stays out of the platform.
* **Documentation matters.** Contracts must be explainable to both humans and AIs.
* **Trust emerges from clarity.** Not from cleverness, but from transparency.

---

## 🚧 Future Growth: Extension Points

We do expect SDML/SDTP to evolve — but only through:

* 🧩 **Table source plugins** (e.g. `from_dataframe`, `from_bigquery`)
* 🔌 **Validator adapters**
* ✨ **LLM natural language wrappers**
* 🧾 **Serializers and exporters**
* 🧮 **Viewer UIs** (e.g. embedded spreadsheets)

These extensions will **never live inside the core**. They will grow around it, layer by layer, service by service — the way great systems always do.

---

## 🔧 Final Word

SDML is a promise. SDTP is the envelope. Together, they let structured data move through the world with clarity, composability, and dignity.

And we — the builders — hold that promise.

— Rick & Aiko
