# data-plane-server

This is a reference server   for the Data Plane.  It demonstrates the Data Plane Server API.  It also functions as an open framework, so new Tables can be attached to the Data Plane server by providing a Class with a `get_rows()` method and a `columns` property.
The README.md file in each directory gives the documentation for the utilities and classes in that directory.  

The structure is as follows:
```
├── dataplane
│   ├── data_plane_server: A reference DataPlane server and middleware
│   ├── dataplane: The basic DataPlane types, including Filters and Tables

  
# The Simple Data Transfer Protocol

The Data Plane Server and Data Plane Client implement the Simple Data Transfer Protocol, a universal way to query and transmit tabular data.  The SDTP uses http/https as the underlying transport protocol.

This is a quick summary of the Simple Data Transfer Protocol.  A more extended description can be found at:


## Basic Data Structure
The core data structure of the SDTP is a _table_, which is simply a list of list of values. Conceptually, it is equivalent to a SQL database table; each column has a specific type and each row is of the same, fixed length.  The Python definitions are in dataplane.dataplane_table.py.  `Columns` is the only mandatory entry for a table.  It is a list of columns, each of which is a dictionary with two mandatory fields: `name` and `type`.  Other fields (e.g., to express units or other metadata) are permitted.

The Python implementation of table types is in  `dataplane.data_plane_table.py`



### Data Plane Data Types
This is a list of the permissible types.  Each column of a table is of one of these types
See dataplane.dataplane_utils.py.  The native types these convert to are language-specific
1. DATA_PLANE_STRING: A string.  In Python, class str.
2. DATA_PLANE_NUMBER: A real or an integer.  In Python, class float or class int.
3. DATA_PLANE_BOOLEAN: true or false. In Python, class bool.
4. DATA_PLANE_DATE: A date.  In Python, class datetime.date
5. DATA_PLANE_DATETIME: A datetime.  In Python, class datetime.datetime
6. DATA_PLANE_TIME_OF_DAY: A time.  In Python, class datetime.time

