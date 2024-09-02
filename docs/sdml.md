
# The Simple Data Markup Language
The Simple Data Markup Language (SDML) is a language for capturing and linking tabular data.  It is designed to do for tabular data what HTML did for documents.  However, while HTML documents are primarily designed for human consumption, SDML Tables are primarily designed for machine access.

In SDML, the unit is the _table_.  Each SDML document describes a _single_ table. 
A table is a (potentially infinite) list of fixed-length records.  Each record is called a _row_.  An SDML table is equivalent to:
- A PANDAS Dataframe
- A SQL database table
- A specific form of CSV file where
    - The data are in the rows of the CSV file
    - The rows of the CSV file are all the same length
    - The type of the entries in any column of the CSV file are the same as all the other entries
- A single spreadsheet tab with the same restrictions as the CSV file.


## Example

The following example shows the key features of SDML.  This table is taken from Florence' Nightingale's famous 1854-1855 dataset investigating the causes of death in the Crimean War
```
{
  "type": "RowTable",
  "schema": [
    {"name": "Month_number", "type": "number"},
    {"name": "Date", "type": "date"},
    {"name": "Year", "type": "number"},
    {"name": "Month", "type": "string"},
    {"name": "Army", "type": "number"},
    {"name": "Disease", "type": "number"},
    {"name": "Wounds", "type": "number"},
    {"name": "Other", "type": "number"},
    {"name": "Disease.rate", "type": "number"},
    {"name": "Wounds.rate", "type": "number"},
    {"name": "Other.rate", "type": "number"}
  ],
  "rows": [
    [1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7]
    ...
  ]
}
```
This file describes a tablewith 11 columns and one row per month.   Each row in `row` section of the table has exactly 11 entries, and the type of the kth column lines up with the type of the kth row.

## SDML Table Structure
Each SDML table  is a dictionary, with the following fields:
- `schema`: this is a list of objects, each of which _must_ have two fields:
    - `name`: a string with the name of the column
    - `type`: the type of the column, which is one of the supported SDML types (see below)
- `type`: this is a string, which describes the _type_ of the table.  The type is the source of the table rows; see the list of supported table types below.  The type of the table determines the remaining fields in the table dictionary.

Note that the top level, ` `schema` entries all admit the possibility of non-required fields, which are open to convention for specific purposes.  One common purpose is metadata of various sorts: the units for a specific column; column relationships (e.g., one column is an error bar for another); collection method or purpose of a table; etc.  While it is assumed that these additional fields will in general be strings, there is no requirement that they be strings.
 
 ### Table Types
 A table type describes  the source of the rows of the table.  The goal of SDML is to capture the ways that data today is represented.  These include:
 - Direct representation
 - CSV Files
 - xlsx files
 - Google sheets
Further, SDML not only supports local SDML files, but also remote files at the remote end of an HTTP download link or Simple Data Transfer Protocol (SDTP) link.

#### RowTable
A _RowTable_ is the simplest form of SDML Table; it is given by a single dictionary entry `rows`, which gives a list of lists of SDML values (see below).  In a RowTable, the rows of the table are directly represented in the SDML file.

#### RemoteTable
A _RemoteTable_  is an SDML Table hosted on a remote Simple Data Transfer Protocol server and is directly queried from there.  It has three dictionary items beyond the "type" and "schema" fields required of all tables:
- _name_, required: the name of the table on the remote server
- _url_, required: the URL of the remote SDTP server
- _headers_, optional: a dictionary of header variables and values that accompanies an SDTP request on this table.  This is typically used for authentication information.  An example remote table is given here:
```
{
  "type": "RemoteTable",
  "schema": [
    {"name":"Year","type":"number"},
    {"name":"Democratic","type":"number"},
    {"name":"Republican","type":"number"},
    {"name":"Other","type":"number"}
  ],
  "name": "electoral_college"
  "url": "https://sdtp-data-wiki-new-lrbsxicfna-uw.a.run.app"
}

```

A `RemoteCSVTable` type is under consideration.

##### Further Table Types
Further table types are planned, under  conditions:
- There is a large body of uploaded and available data in the desired format
- On-the-fly conversion to SDML format is robust and reliable
- It's easier to convert on the fly rather than generating an SDML table

### A Note on Tables
It's important to note that SDML tables are used as an interchange format, and can be generated on demand in response to queries, much as an HTML document need not be physically resident in a repository, but can and are generated dynamically in response to queries. An SDML Table type is only required to permit a remote client to query the table itself.
It's expected that the only table types in wide usage will be `RowTable` and `RemoteTable`.  The remaining table types are in support of legacy datasets which are not hosted by a Global Data Plane server.  In most cases, however, it's a far better idea to stand up a GDP server, which can be tailored specifically to the hosted datasets.
For example, it's relatively straightforward to stand up a `SQLTable` datatype, which would handle the connectivity to an underlying Postgres, MySQL, or other DB engine and simply reflect the underlying database schema.  However, database schemas reflect both the semantics of the underlying data and storage efficiencies.  The semantic schema is generally far simpler, and offers simpler queries.  Making a GDP server the interface to the database allows implementers to hide the complex layouts that arise from storage efficiencies.

## SDML Value Types
SDML currently supports seven datatypes.  These types, their semantics, and JSON  wire format are given here.  The vital point about each type is that the JSON libraries in JavaScript and Python are easily able to read the values and convert them to the proper types for computation.

| Type | Wire Format | Description |
|------|-------------|-------------|
| number | Integer or floating point decimal number | A number |
| string | UTF String | A string |
| boolean | true or false | A boolean value |
| date | A date in ISO format YYYY-MM-DD, quoted as a string value | A date |
| datetime | A datetime in ISO format YYYY-MM-DD#hh:mm:ss.nnn, quoted as a string value | A date  and time |
| timeofday | A timestamp in ISO format hh:mm:ss.nnn, quoted as a string value | A  time of day|
| point | A list of numbers, of arbitrary length | The intent is to model an n-dimensional vector, for which there is no standard ISO format.  The dimension of the vector for a specific column is left unspecified and not checked |

