.. include:: ../README.rst
This is a reference server and client  for the Simple Data Transfer Protocol.  It demonstrates the SDTP Server API.  It also functions as an open framework, so new Tables can be attached to the Data Plane server by providing a Class with a `get_rows()` method and a `columns` property.
The README.md file in each directory gives the documentation for the utilities and classes in that directory.  

The structure is as follows:
```
├── sdtp
│   ├── sdtp_server: A reference SDTP server and middleware
│   ├── sdtp: The basic SDTP types, including Filters and Tables
