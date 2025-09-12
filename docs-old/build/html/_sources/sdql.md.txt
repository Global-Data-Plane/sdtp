# The Simple Data Query Language
The Simple Data Query Language (SDQL) is the primary interaction between Global Data Plane users and SDML tables.  It is rare that a GDP user will want to download or examine an entire SDML Table.  In fact, in some sense at-source filtering is the entire point of the GDP, and for some tables downloading the entire table is impossible.  SDML Tables are logical, not physical, entities.  For example, a Solar System simulation takes in the initial positions, velocities, and masses of the planets as initial conditions and reports their positions and velocities at arbitrary times in the future.  An SDML Table representing the Solar System has a column for each planet's position, velocity, and mass, and a column for time.  Runs of the simulator are triggered by SDQL queries, which specify the initial conditions and request the values for specific ranges of time.
SDQL is designed to be lightweight and simple.  When the Structured Query Language (SQL) was designed, it was assumed that no computation outside SQL was done, and as a result SQL was designed to be a full-featured compute engine.  SDQL has a different set of design assumptions; it assumes that the query agent is a program, and the results of the SDQL query will be inputs to further computation on the client side.  As a result, SDQL's sole operation is to return the data of interest to the followon computation operation.    Moreover, much of SQL (for example) is devoted to creating conjoined tables on the fly (this is the principal function of the `JOIN` operation).  Since the Global Data Plane's tables are _semantic_, not _physical_, entities, this is done server-side and isn't exposed in the query language. The sole functions of SDQL is to _filter_ and provide summary information on tables.

## SDQL Syntax and Structure
SDQL is an _intermediate_ form for queries, designed to support a wide range of surface syntaxes and encoding in POST http request bodies.  As a result, each SDQL Query is a JSON structure, of the form: `{"table": <table_name>, "query": <query>}`.
## SDQL Query Classes

SDQL has two classes of query: _column_ queries provide summary information about a specific column, and _row_ queries select rows which meet specific criteria.  SDQL column operators are designed to provide information for subsequent row operations -- e.g., what are the possible values entries in this column can take?


### SDQL Column Queries
SDQL currently supports three column queries

- `{"operator": "GET_RANGE", "column": <column_name>}`.  Get the range (maximum and minimum values) over a column.  Since every SDML type is ordered, this is defined for all columns.

- `{"operator": "GET_ALL_VALUES", "column": <column_name>}`.  Get the set of _distinct_ values in a column

- `{"operator": "GET_COLUMN", "column": <column_name>}`.  Get the list  of _all_ values in a column, including duplicates


_Note on infinite tables_.  Since a Global Data Plane table is a logical, not physical object and is of potentially unbounded size, column queries must be implemented carefully on very large or unbounded tables.  `GET_COLUMN` is clearly not well-defined, and should return an error in this case; `GET_RANGE` should return the maximum and minimum _possible_ values in this case, and `GET_ALL_VALUES` should return the set  of possible values.  If this set is infinite, an error should be returned

### SDQL Row Queries
SDQL Row queries are designed to filter rows of the table; the result of an SDQL row query is the set of rows which match the condition.  Effectively, it operates as a _simple_ form of a SQL `WHERE` clause.  There are currently six supported operators:

- `{"operator": "IN_RANGE", "column": <column>, "min_val": <min_val>, "max_val": <max_val>}`.  Returns the list of rows where the entry in column `<column>` is between `<min_val>` and `<max_val>`, inclusive.

- `{"operator": "IN_LIST", "column": <column>, "values": <list of values>}`.  Returns the list of rows where the entry in column `<column>` is any of the values specified in the list.

- `{"operator": "REGEX_MATCH", "column": <column>, "expression": <re match expression>}`.  _Columns of type *STRING* only_. Returns the list of rows where the entry in column `<column>` matches the REEGEX_MATCH expression `<expression>`.  The syntax of the regular expression `<expression>` is in the standard Python regular expression syntax.

- `{"operator": "ALL", "arguments": <list of SDQL Query Operations>}`.  Returns the list of rows where _every_ query in the list of `arguments` matches.  This is equivalent to a Boolean `AND` on the query list

- `{"operator": "ANY", "arguments": <list of SDQL Query Operations>}`.  Returns the list of rows where _any_ query in the list of `arguments` matches.  This is equivalent to a Boolean `OR` on the query list

- `{"operator": "NONE", "arguments": <list of SDQL Query Operations>}`.  Returns the list of rows where _no_ query in the list of `arguments` matches.  This is equivalent to a Boolean `NOT` on the query list

It's important to note that the `ALL`, `ANY`, `NONE` queries are just standard SDQL queries, so that they can be nested and form an arbitrary logic circuit on the rows of the table.

# Examples

We show a number of examples of SDQL Queries, using the Florence Nightingale dataset from the Crimean War.  Its SDML file is shown here:
```
{
  "name": "nightingale",
  "table": {
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
      [1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7],
      [2, "1854-05-01", "May", 1854, 23333, 12, 0, 9, 6.2, 0, 4.6],
      [3,  "1854-06-01", "Jun", 1854, 28333, 11, 0, 6, 4.7, 0, 2.5],
      [4,  "1854-07-01", "Jul", 1854, 28722, 359, 0, 23, 150, 0, 9.6],
      [5,  "1854-08-01", "Aug", 1854, 30246, 828, 1, 30, 328.5, 0.4, 11.9],
      [6,  "1854-09-01", "Sep", 1854, 30290, 788, 81, 70, 312.2, 32.1, 27.7],
      [7,  "1854-10-01", "Oct", 1854, 30643, 503, 132, 128, 197, 51.7, 50.1],
      [8,  "1854-11-01", "Nov", 1854, 29736, 844, 287, 106, 340.6, 115.8, 42.8],
      [9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48],
      [10,  "1855-01-01", "Jan", 1855, 32393, 2761, 83, 324, 1022.8, 30.7, 120],
      [11,  "1855-02-01", "Feb", 1855, 30919, 2120, 42, 361, 822.8, 16.3, 140.1],
      [12,  "1855-03-01", "Mar", 1855, 30107, 1205, 32, 172, 480.3, 12.8, 68.6],
      [13,  "1855-04-01", "Apr", 1855, 32252, 477, 48, 57, 177.5, 17.9, 21.2],
      [14,  "1855-05-01", "May", 1855, 35473, 508, 49, 37, 171.8, 16.6, 12.5],
      [15,  "1855-06-01", "Jun", 1855, 38863, 802, 209, 31, 247.6, 64.5, 9.6],
      [16,  "1855-07-01", "Jul", 1855, 42647, 382, 134, 33, 107.5, 37.7, 9.3],
      [17,  "1855-08-01", "Aug", 1855, 44614, 483, 164, 25, 129.9, 44.1, 6.7],
      [18,  "1855-09-01", "Sep", 1855, 47751, 189, 276, 20, 47.5, 69.4, 5],
      [19,  "1855-10-01", "Oct", 1855, 46852, 128, 53, 18, 32.8, 13.6, 4.6],
      [20,  "1855-11-01", "Nov", 1855, 37853, 178, 33, 32, 56.4, 10.5, 10.1],
      [21,  "1855-12-01", "Dec", 1855, 43217, 91, 18, 28, 25.3, 5, 7.8],
      [22,  "1856-01-01", "Jan", 1856, 44212, 42, 2, 48, 11.4, 0.5, 13],
      [23,  "1856-02-01", "Feb", 1856, 43485, 24, 0, 19, 6.6, 0, 5.2],
      [24,  "1856-03-01", "Mar", 1856, 46140, 15, 0, 35, 3.9, 0, 9.1]
    ]
  }
}
```

Which renders as this table:
| Month_Number | Date | Month | Year | Army | Disease | Wounds | Other | Disease.rate | Wounds.rate | Other.rate | 
|--------------|------|-------|------|------|---------|--------|-------|--------------|-------------|------------| 
| 1 | 1854-04-01 | Apr | 1854 | 8571 | 1 | 0 | 5 | 1.4 | 0 | 7 | 
| 2 | 1854-05-01 | May | 1854 | 23333 | 12 | 0 | 9 | 6.2 | 0 | 4.6 | 
| 3 | 1854-06-01 | Jun | 1854 | 28333 | 11 | 0 | 6 | 4.7 | 0 | 2.5 | 
| 4 | 1854-07-01 | Jul | 1854 | 28722 | 359 | 0 | 23 | 150 | 0 | 9.6 | 
| 5 | 1854-08-01 | Aug | 1854 | 30246 | 828 | 1 | 30 | 328.5 | 0.4 | 11.9 | 
| 6 | 1854-09-01 | Sep | 1854 | 30290 | 788 | 81 | 70 | 312.2 | 32.1 | 27.7 | 
| 7 | 1854-10-01 | Oct | 1854 | 30643 | 503 | 132 | 128 | 197 | 51.7 | 50.1 | 
| 8 | 1854-11-01 | Nov | 1854 | 29736 | 844 | 287 | 106 | 340.6 | 115.8 | 42.8 | 
| 9 | 1854-12-01 | Dec | 1854 | 32779 | 1725 | 114 | 131 | 631.5 | 41.7 | 48 | 
| 10 | 1855-01-01 | Jan | 1855 | 32393 | 2761 | 83 | 324 | 1022.8 | 30.7 | 120 | 
| 11 | 1855-02-01 | Feb | 1855 | 30919 | 2120 | 42 | 361 | 822.8 | 16.3 | 140.1 | 
| 12 | 1855-03-01 | Mar | 1855 | 30107 | 1205 | 32 | 172 | 480.3 | 12.8 | 68.6 | 
| 13 | 1855-04-01 | Apr | 1855 | 32252 | 477 | 48 | 57 | 177.5 | 17.9 | 21.2 | 
| 14 | 1855-05-01 | May | 1855 | 35473 | 508 | 49 | 37 | 171.8 | 16.6 | 12.5 | 
| 15 | 1855-06-01 | Jun | 1855 | 38863 | 802 | 209 | 31 | 247.6 | 64.5 | 9.6 | 
| 16 | 1855-07-01 | Jul | 1855 | 42647 | 382 | 134 | 33 | 107.5 | 37.7 | 9.3 | 
| 17 | 1855-08-01 | Aug | 1855 | 44614 | 483 | 164 | 25 | 129.9 | 44.1 | 6.7 | 
| 18 | 1855-09-01 | Sep | 1855 | 47751 | 189 | 276 | 20 | 47.5 | 69.4 | 5 | 
| 19 | 1855-10-01 | Oct | 1855 | 46852 | 128 | 53 | 18 | 32.8 | 13.6 | 4.6 | 
| 20 | 1855-11-01 | Nov | 1855 | 37853 | 178 | 33 | 32 | 56.4 | 10.5 | 10.1 | 
| 21 | 1855-12-01 | Dec | 1855 | 43217 | 91 | 18 | 28 | 25.3 | 5 | 7.8 | 
| 22 | 1856-01-01 | Jan | 1856 | 44212 | 42 | 2 | 48 | 11.4 | 0.5 | 13 | 
| 23 | 1856-02-01 | Feb | 1856 | 43485 | 24 | 0 | 19 | 6.6 | 0 | 5.2 | 
| 24 | 1856-03-01 | Mar | 1856 | 46140 | 15 | 0 | 35 | 3.9 | 0 | 9.1 |
|--------------|------|-------|------|------|---------|--------|-------|--------------|-------------|------------|

## Column Operation Examples

Here we show examples of each column operation, with comments on operation and semantics.  Note that column operations cannot be composed; each a simple operation with a simple result, and the results of a column operation aren't 

| Description | SDQL Operation | Result | Comment |
|-------------|----------------|--------|---------|
| Find the maximum and minimum month | `{"operator": "GET_RANGE", "column": "Month"}` | `["Apr", "Sep"]` | Ordering is type-specific; for string, it's alphabetic |
| Find the distinct values in the months column | `{"operator": "GET_ALL_VALUES", "column": "Month"}` | `["Apr", "Aug", "Dec", "Feb", "Jan", "Jul", "Jun", "Mar", "May", "Nove", "Oct", "Sep"]` | It isn't required that the results be ordered, but they often  are |
| Get the "Wounds" column | `{"operator": "GET_COLUMN", "column": "Army"}` | [0, 0, 0, 0, 1, 81, 132, 287, 114, 83, 42, 32, 48, 49, 209, 134, 164, 276, 53, 33, 18, 2, 0, 0]  | The table is by definition unordered, and the results of this query are unordered.  There is one entry per row in the table|

## Row Operation Examples

Here we show examples of row operations, with comments on operation and semantics.  Unlike column operations, row operations compose using the `ANY`, `ALL`, and `None` operations

| Description | SDQL Operation | Result | Comment |
|-------------|----------------|--------|---------|
| Find all the months when the number of  wounds was less than or equal to 20 | `{"operator": "IN_RANGE", "column": "Wounds", "min_val": 0, "max_val": 20}` | `[[1, "1854-04-01", "Apr", 1854, 8571, 1, 0, 5, 1.4, 0, 7], [2, "1854-05-01", "May", 1854, 23333, 12, 0, 9, 6.2, 0, 4.6], [3, "1854-06-01", "Jun", 1854, 28333, 11, 0, 6, 4.7, 0, 2.5], [4, "1854-07-01", "Jul", 1854, 28722, 359, 0, 23, 150, 0, 9.6], [5, "1854-08-01", "Aug", 1854, 30246, 828, 1, 30, 328.5, 0.4, 11.9], [21, "1855-12-01", "Dec", 1855, 43217, 91, 18, 28, 25.3, 5, 7.8], [22, "1856-01-01", "Jan", 1856, 44212, 42, 2, 48, 11.4, 0.5, 13], [23, "1856-02-01", "Feb", 1856, 43485, 24, 0, 19, 6.6, 0, 5.2], [24, "1856-03-01", "Mar", 1856, 46140, 15, 0, 35, 3.9, 0, 9.1]]` | `IN_RANGE` is inclusive |
| Find all the months with an 'e' as the middle letter | `{"operator": "REGEX_MATCH", "column": "Month", "expression": ".e."}` | `[[6,  "1854-09-01", "Sep", 1854, 30290, 788, 81, 70, 312.2, 32.1, 27.7], [9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48], [11,  "1855-02-01", "Feb", 1855, 30919, 2120, 42, 361, 822.8, 16.3, 140.1], [18,  "1855-09-01", "Sep", 1855, 47751, 189, 276, 20, 47.5, 69.4, 5], [21,  "1855-12-01", "Dec", 1855, 43217, 91, 18, 28, 25.3, 5, 7.8], [23,  "1856-02-01", "Feb", 1856, 43485, 24, 0, 19, 6.6, 0, 5.2]]` | |
| Find the records for March and April | `{"operator": "IN_LIST", "column": "Month", "values": ["Mar", "Apr"]}` | `[[1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7], [12,  "1855-03-01", "Mar", 1855, 30107, 1205, 32, 172, 480.3, 12.8, 68.6], [13,  "1855-04-01", "Apr", 1855, 32252, 477, 48, 57, 177.5, 17.9, 21.2], [24,  "1856-03-01", "Mar", 1856, 46140, 15, 0, 35, 3.9, 0, 9.1]]` | |
| Find the records for months between April and February | `{"operator": "IN_RANGE", "column": "Month", "min_val": "Apr", "max_val": "Feb"}` | `[[1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7], [5,  "1854-08-01", "Aug", 1854, 30246, 828, 1, 30, 328.5, 0.4, 11.9], [9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48], [11,  "1855-02-01", "Feb", 1855, 30919, 2120, 42, 361, 822.8, 16.3, 140.1], [13,  "1855-04-01", "Apr", 1855, 32252, 477, 48, 57, 177.5, 17.9, 21.2], [17,  "1855-08-01", "Aug", 1855, 44614, 483, 164, 25, 129.9, 44.1, 6.7], [21,  "1855-12-01", "Dec", 1855, 43217, 91, 18, 28, 25.3, 5, 7.8], [23,  "1856-02-01", "Feb", 1856, 43485, 24, 0, 19, 6.6, 0, 5.2]]` | Comparisons on strings are alphabetical |
| Find the records for dates  between April and February | `{"operator": "NONE", "arguments": [{"operator": "IN_LIST", "column": "Month", "values": ["Mar"]}]}` | `[[1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7], [2, "1854-05-01", "May", 1854, 23333, 12, 0, 9, 6.2, 0, 4.6], [3,  "1854-06-01", "Jun", 1854, 28333, 11, 0, 6, 4.7, 0, 2.5], [4,  "1854-07-01", "Jul", 1854, 28722, 359, 0, 23, 150, 0, 9.6], [5,  "1854-08-01", "Aug", 1854, 30246, 828, 1, 30, 328.5, 0.4, 11.9], [6,  "1854-09-01", "Sep", 1854, 30290, 788, 81, 70, 312.2, 32.1, 27.7], [7,  "1854-10-01", "Oct", 1854, 30643, 503, 132, 128, 197, 51.7, 50.1], [8,  "1854-11-01", "Nov", 1854, 29736, 844, 287, 106, 340.6, 115.8, 42.8], [9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48], [10,  "1855-01-01", "Jan", 1855, 32393, 2761, 83, 324, 1022.8, 30.7, 120], [11,  "1855-02-01", "Feb", 1855, 30919, 2120, 42, 361, 822.8, 16.3, 140.1], [13,  "1855-04-01", "Apr", 1855, 32252, 477, 48, 57, 177.5, 17.9, 21.2], [14,  "1855-05-01", "May", 1855, 35473, 508, 49, 37, 171.8, 16.6, 12.5], [15,  "1855-06-01", "Jun", 1855, 38863, 802, 209, 31, 247.6, 64.5, 9.6], [16,  "1855-07-01", "Jul", 1855, 42647, 382, 134, 33, 107.5, 37.7, 9.3], [17,  "1855-08-01", "Aug", 1855, 44614, 483, 164, 25, 129.9, 44.1, 6.7], [18,  "1855-09-01", "Sep", 1855, 47751, 189, 276, 20, 47.5, 69.4, 5], [19,  "1855-10-01", "Oct", 1855, 46852, 128, 53, 18, 32.8, 13.6, 4.6], [20,  "1855-11-01", "Nov", 1855, 37853, 178, 33, 32, 56.4, 10.5, 10.1], [21,  "1855-12-01", "Dec", 1855, 43217, 91, 18, 28, 25.3, 5, 7.8], [22,  "1856-01-01", "Jan", 1856, 44212, 42, 2, 48, 11.4, 0.5, 13], [23,  "1856-02-01", "Feb", 1856, 43485, 24, 0, 19, 6.6, 0, 5.2]]` |  Just choose not "march"|
| Find the records for dates  between March 1 1854 and June 30 1854  | `{"operator": "IN_RANGE", "column": "Date", "min_val": "1854-3-1", "max_val": "1854-6-30"}` | `[[1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7],[2, "1854-05-01", "May", 1854, 23333, 12, 0, 9, 6.2, 0, 4.6],[3,  "1854-06-01", "Jun", 1854, 28333, 11, 0, 6, 4.7, 0, 2.5]]` |  Though the wire format for date is an ISO string, comparisons are numeric by date|
| Find the records for the disease rate > 500 or the wound rate > 100 | `{"operator": "ANY", "arguments": [{"operator": "IN_RANGE", "column": "Wounds.rate", "min_val": 100, "max_val": 10000}, "operator": "IN_RANGE", "column": "Disease.rate", "min_val": 500, "max_val": 10000}]}` | `[[8,  "1854-11-01", "Nov", 1854, 29736, 844, 287, 106, 340.6, 115.8, 42.8],[9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48],[10,  "1855-01-01", "Jan", 1855, 32393, 2761, 83, 324, 1022.8, 30.7, 120], [11,  "1855-02-01", "Feb", 1855, 30919, 2120, 42, 361, 822.8, 16.3, 140.1], [12,  "1855-03-01", "Mar", 1855, 30107, 1205, 32, 172, 480.3, 12.8, 68.6]]` |  `ANY` is semantically `OR` |
| Find the records for (the disease rate > 500 or the wound rate > 100) AND Year = 1854 | `{"operator": "ALL", "arguments"[ {"operator": "IN_LIST", "column": "Year", "values": [1854]}, {"operator": "ANY", "arguments": [{"operator": "IN_RANGE", "column": "Wounds.rate", "min_val": 100, "max_val": 10000}, "operator": "IN_RANGE", "column": "Disease.rate", "min_val": 500, "max_val": 10000}]}]}` | `[[8,  "1854-11-01", "Nov", 1854, 29736, 844, 287, 106, 340.6, 115.8, 42.8],[9,  "1854-12-01", "Dec", 1854, 32779, 1725, 114, 131, 631.5, 41.7, 48]]` |  `ALL` is semantically `AND`, and composite operators can be arguments of other composite operators |
|-------------|----------------|--------|---------|

## A Note on Result Format
Since the results of SDQL queries are expected to be used in programs, ease of parsing results is prioritized over making the structures self-documenting.  All results of column queries are JSON lists of values, in ISO format.  All results of row queries are lists of lists of JSON values,  without ornamentation.  This choice was made to give the querying software maximum flexibility in using the results of SDQL queries, with a minimum of parsing and without 