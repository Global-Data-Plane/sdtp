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
👥 4. Make it AI-ready
Data used to be produced by humans and their instruments, and consumed by humans. Today, AIs are full partners in data production and analysis — and a well-matched human/AI team is a marvel of productivity.

That changes the design target.

We need formats that are friendly to both humans and machines — easy to read, easy to generate, and semantically clear.

This isn’t theoretical. It’s already happening:
When AIs and humans collaborate on documents, they often use Markdown — because it provides structure without noise. It’s readable, editable, and semantically expressive without requiring a visual layout engine.

SDML brings that same clarity to tabular data.
It’s compact and declarative for machines.
It’s readable and writable for humans.

It’s the shared surface where both can think clearly — and think together.