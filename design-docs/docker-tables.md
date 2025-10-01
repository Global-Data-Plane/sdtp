# DockerTable: GDP Data Plane Plugin Architecture

## 1. What is a DockerTable?

A **DockerTable** is a single-table, user-written SDTP (Simple Data Plane Table Protocol) server, instantiated as a daughter table in a Kubernetes (K8S) cluster. It enables GDP to securely expose arbitrary, containerized, user- or admin-authored tables as first-class data plane resources.

- Each DockerTable runs as its own disposable pod, isolated from the main GDP/SDTP root server and from other DockerTables.
- The container runs a standard SDTP server (typically via Flask or FastAPI) exposing a single named table.

## 2. Why DockerTable? (Motivation)

- **Data Plane interface for arbitrary code:**  
    Enables the GDP to connect any code (Python, R, Julia, etc.) that generates tabular data, while keeping the main system secure.
    Perfect for custom data sources, data generators, dynamic views, ETL logic, or AI-backed tables.
- **Security and extensibility:**  
    Arbitrary code runs only in disposable, policy-controlled K8s pods—never in the main process.
    GDP can support any language/environment for tables via base images.
- **Auditability & compliance:**  
    Every DockerTable’s lifecycle, access, and resource usage is logged and auditable.

## 3. How Does It Work?

1. **Registration:**  
    Table is registered with the GDP root server with a minimal declaration (see below).
2. **On request:**  
    Root server instantiates a K8S pod from the specified Docker image.
    Forwards all data plane (SDTP) requests to the table server running inside the container (internal network).
    Collects and returns results to the user.
3. **Lifecycle:**  
    Pod can be ephemeral (per-query/job) or persistent (for repeated access).
    Pod teardown and cleanup handled by the GDP controller.

## 4. DockerTable Declaration (What It Needs)

- `type`: Always `"DockerTable"`
- `schema`: Explicit SDML schema (list of columns/types; never inferred)
- `name`: The table name, as registered inside the container's SDTP TableServer
- `image`: Docker image (user- or admin-built, must run SDTP server on known port)
- `auth`: (optional) Permissions for access (list of allowed users/domains/roles; if omitted, table is public)
- `permissions`: (optional, advanced) Permissions the table requires at runtime (e.g., K8s service account, mounts, etc.), specified via GDP admin policy—not by table author

**Example:**

```json
{
    "type": "DockerTable",
    "name": "custom_stats",
    "image": "gdp/python-table-base:latest",
    "schema": [
        {"name": "col1", "type": "string"},
        {"name": "col2", "type": "int"}
    ],
    "auth": ["alice@example.com", "bob@example.com", "*@partner.org"]
}
```
## 5. Easy Building: Recommended Base Image Workflow

**Base image includes:**

- dtp library (with SDTP TableServer and reference blueprint)

**User process:**

1. Add a table class with explicit schema and required SDMLTable methods.

2. Instantiate the table and register it with sdtp_server_blueprint.table_server.add_sdtp_table().

3. Start a simple Flask (or FastAPI) app using the blueprint:

```
from flask import Flask
import sdtp

app = Flask(__name__)
app.register_blueprint(sdtp.sdtp_server_blueprint)
app.run(host="0.0.0.0", port=8080)
```
**Dockerfile example:**
```
FROM python:3.11-slim
WORKDIR /srv/table
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY sdtp/ ./sdtp/
COPY user_table.py ./
EXPOSE 8080
CMD ["python", "user_table.py"]
```
**Table registration and Flask app launch are handled in user_table.py, matching the GDP table declaration.**
---

### Notes

- All authorization and credential provisioning are handled by the GDP root server and cluster policy, keyed off the auth/permissions blocks—never inside the table code.

- User code is never responsible for handling user credentials directly.

- This pattern enables scalable, secure, and flexible GDP table extensibility for any use case.

_Co-authored by Rick & Aiko, GDP/Home design team._