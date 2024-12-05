# The Simple Data Transfer Protocol
The third component of the Global Data Plane is the Simple Data Transfer Protocol (SDTP) which permits the execution of Simple Data Query Languaage (SDQL) queries on Simple Data Markup Language (SDML) queries over the network.  It is the simplest of the three components of the Global Data Plane; it is simply a mechanism for sending SDQL queries and receiving the results over an HTTP/S connection.  It is a set of three routes which can be implemented by any HTTP/S server; a reference implementation on a Flask server is available.  

The primary design goal of SDTP is _ease of adoption_.  It should be easy to implement SDTP in any existing web server.  SDTP is designed to require _no_ specialized software on either the client or the server side.  STDP queries are standard HTTP/S POST/GET, and the return values are JSON dictionaries and lists.

This design goal led to a very spare, simple protocol.  The design mantra was "When in doubt, leave it out".  Useful protocols and standards add required features in response to user needs over time; simplicity in initial design permits the maximum flexibility in adding these features when and as they are needed, with specific use cases in mind.   It also permits the use of generic HTTP/S features for features and use cases. Finally, it permits implementers maximum freedom in enhancing the protocol for specific situations.

SDTP is not designed or intended to be a complete data hosting solution.  A number of features that are desirable or required in a hosting solution are absent from the basic SDTP protocol.  Search is one example.  It can be anticipated that a single SDTP server can host a large number of SDML tables, either physically or, through the SDML RemoteTable mechanism, virtually, or both.  data.gov, for example, has about 300,000 datasets, and almost all of these are easily convertible to SDML.  _Finding_ the right datasets for a problem is desirable; it's also a feature with a large number of existing implementations, and SDTP sites are free to implement the search mechanism appropriate for their domain -- or none at all.

Similar reasoning applies to a lack of security in the protocol.  Early versions of the SDTP anticipated per-table access control based on header variables.  This was dropped, because there are a plethora of HTTP/S access control mechanisms that are adapted for specific purposes.  At the end of the day, access to tabular data is no different from API access to document or image data, and access issues are well solved in HTTP/S.

In sum, SDTP is not designed as a standalone protocol.  It is a set of standard routes that must be implemented by a general HTTP/S server.

## SDTP Routes
There are three classes of route in the SDTP protocol: one for getting the names and schemas of the tables the server hosts, another for executing column queries on a specific table, and a third for executing row queries.  The first and third are single-route classes; the second is essentially a single-route class, but has additional routes for convenience of the user.

A major design goal of the Global Data Plane is that no specific client libraries or software beyond a standard HTTP/S request library (`fetch` in JavaScript, `requests` or the various `urrlib`s in Python, `curl` or `wget` from the command line) are required.  Requests are standard HTTP/S `GET` requests with parameters or `POST` requests with a JSON body.  Returns are _always_ JSON objects or lists, and, when there is a tradeoff between contextual information and ease of parsing, the latter consideration dominates.  For example, in early versions of the protocol, a `get_range` request returned a JSON dictionary with two fields, `max_val` and `min_val`.  This was dropped in favor of returning a two-element ordered list: `{"min_val: <v1>, "max_val": <v2>}` became `[v1, v2]`, because every client has the ability to parse a JSON list in a single API call.  This is a very simple and trivial example, but it illustrates the design philosophy.

Similarly, SDTP uses standard HTTP/S error codes.

### Get Tables
This class consists of three  routes, `get_table_names`, `get_table_schema?table=<table_name>`, `get_tables`.

#### `get_table_names`
*Description:* Returns the list of names of tables hosted by this server, as a simple list of strings.
*Methods:* `GET`
*Parameters: None
*Body:* None
*Headers:* None
*Returns:* A JSON list of the names of the tables hosted by this server
*Errors:* None
*Example:* `/get_table_names`
*Example Return:* `["ec_table", "electoral_college", "nationwide_vote", "presidential_margins", "presidential_vote", "presidential_vote_history"]`

#### `get_table_schema?table=<table_name>`
*Description:* Gets the schema of table `<table_name>` as a list of JSON objects.  Each object contains the fields `name`, the name of the column, and `type`, which is a  Global Data Plane data type.  See [SDML](sdml.md) for the list of types.  Note that a schema object _may_ contain other fields, e.g., `units` for numeric data or, more generally, strings or JSON objects used for metadata purposes.
*Methods:* `GET`
*Parameters: `<table_name>`, a string, required. name of the table
*Body:* None
*Headers:* None
*Returns:* The schema of the table as a list of  JSON objects
*Errors:* 400: `Missing parameter table` if the table is missing, or 400: `Table <table_name> not found if the table is not present on this server.
*Example:* `/get_table_schema?table=nationwide_vote`
*Example Return:* 
```
[
  {
    "name": "Year",
    "type": "number"
  },
  {
    "name": "Party",
    "type": "string"
  },
  {
    "name": "Percentage",
    "type": "number"
  }
]
```

#### `get_tables`
*Description:* Returns the schema of _all_ of the tables as a JSON list of obj, indexed by table name.  Note that each element of the list is identical to the response to the appropriate `get_table_schema` request.  Also note that, if the server hosts many tables, that this can be a very large response. 
*Methods:* `GET`
*Parameters: None
*Body:* None
*Headers:* None
*Returns:* A JSON list of the names of the tables hosted by this server
*Errors:* None
*Example:* `/get_tables`
*Example Return:*
```
{
  "ec_table": [
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "Democratic",
      "type": "number"
    },
    {
      "name": "Republican",
      "type": "number"
    },
    {
      "name": "Other",
      "type": "number"
    }
  ],
  "electoral_college": [
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "Democratic",
      "type": "number"
    },
    {
      "name": "Republican",
      "type": "number"
    },
    {
      "name": "Other",
      "type": "number"
    }
  ],
  "nationwide_vote": [
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "Party",
      "type": "string"
    },
    {
      "name": "Percentage",
      "type": "number"
    }
  ],
  "presidential_margins": [
    {
      "name": "State",
      "type": "string"
    },
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "Margin",
      "type": "number"
    }
  ],
  "presidential_vote": [
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "State",
      "type": "string"
    },
    {
      "name": "Name",
      "type": "string"
    },
    {
      "name": "Party",
      "type": "string"
    },
    {
      "name": "Votes",
      "type": "number"
    },
    {
      "name": "Percentage",
      "type": "number"
    }
  ],
  "presidential_vote_history": [
    {
      "name": "State",
      "type": "string"
    },
    {
      "name": "Year",
      "type": "number"
    },
    {
      "name": "Democratic",
      "type": "number"
    },
    {
      "name": "Republican",
      "type": "number"
    },
    {
      "name": "Progressive",
      "type": "number"
    },
    {
      "name": "Socialist",
      "type": "number"
    },
    {
      "name": "Reform",
      "type": "number"
    },
    {
      "name": "Other",
      "type": "number"
    }
  ]
}
```
### Column Operations
The column operations of SDTP mirror the column queries of [SDQL](sdql.md).  There is one essential column operation: `/execute_column_query`, which is a `POST` request with an SDQL query body.  There are also convenience methods for the existing three SDQL column queries.
#### `/execute_column_query`
*Description:* Returns the result of executing the SDQL column query in the request body, which will always be a JSON list of values.
*Methods:* `POST`
*Parameters: None
*Body:* A JSON SDQL Column query.  See [SDQL](sdql.md)
*Headers:* 'Content-type: application/json'
*Returns:* A JSON list of the result of the SDQL request
*Errors:* 400 if either the table or column is missing, or if the operation is malformed
*Example:* `/execute/column/query` with body `{"table": "nightingale", "query": {"column": "Month_number", "operator": "GET_RANGE"}}`
*Example Return:* `[1, 24]`

#### `/get_range?table=<table_name>&column=<column_name>`
*Description:* A convenience `GET` method equivalent to the `/execute_column_query` request with body `{"table": <table_name>, "query": {"column": <column_name>, "operator": "GET_RANGE"}}`
*Methods:* `GET`
*Parameters: `table`, the name of the table to check, and `column`, the name of the column to get the range for.
*Body:* None
*Headers:* None
*Returns:* A JSON list of the result of the SDQL request
*Errors:*  400 if either the table or column is missing
*Example:* `/get_range?table=nightingale&column=Month_number` 
*Example Return:* `[1, 24]`

#### `/get_all_values?table=<table_name>&column=<column_name>`
*Description:* A convenience `GET` method equivalent to the `/execute_column_query` request with body `{"table": <table_name>, "query": {"column": <column_name>, "operator": "GET_ALL_VALUES"}}`
*Methods:* `GET`
*Parameters: `table`, the name of the table to check, and `column`, the name of the column to get the distinct values for.
*Body:* None
*Headers:* None
*Returns:* A JSON list of the result of the SDQL request
*Errors:*  400 if either the table or column is missing
*Example:* `/get_all_values?table=nightingale&column=Month` 
*Example Return:* `["Apr", "Aug", "Dec", "Feb", "Jan", "Jul", "Jun", "Mar", "May", "Nov", "Oct", "Sep"]`


#### `/get_column?table=<table_name>&column=<column_name>`
*Description:* A convenience `GET` method equivalent to the `/execute_column_query` request with body `{"table": <table_name>, "query": {"column": <column_name>, "operator": "GET_COLUMN"}}`
*Methods:* `GET`
*Parameters: `table`, the name of the table to check, and `column`, the name of the column to get the distinct values for.
*Body:* None
*Headers:* None
*Returns:* A JSON list of the result of the SDQL request
*Errors:*  400 if either the table or column is missing
*Example:* `/get_column?table=nightingale&column=Month_Number` 
*Example Return:* `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]`

#### Note on Unbounded Columns
As noted in [SDQL](sdql.md) columns are potentially of unbounded size.  The results of column queries on columns of unbounded size are the choice of the implementing server, and unspecified by the protocol

### SDTP Row Operations
There is only a single row route in the Simple Data Transfer Protocol, and it is a thin overlay on [SDQL](sdql.md) row queries.  The single route is `get_filtered_rows`, a `POST` method whose JSON body is an SDQL row query.

#### `/get_filtered_rows`
*Description:* Returns the result of executing the SDQL row query in the request body, which will always be a JSON list of JSON lists of values.  See the return values of row operations in [SDQL](sdql.md) for details and examples
*Methods:* `POST`
*Parameters: None
*Body:* A JSON SDQL Row query.  See [SDQL](sdql.md)
*Headers:* 'Content-type: application/json'
*Returns:* The result of the SDQL request, which will be a list of lists in JSON form
*Errors:* 400 if either the table  is missing, or if the operation is malformed
*Example:* `/get_filtered_rows`.  The bodies are the SDQL queries in [SDQL](sdql.md).  One example body is `{"table": "nightingale",  "query": {"operator": "IN_RANGE", "column": "Date", "min_val": "1854-3-1", "max_val": "1854-6-30"}}`
*Example Return:* `[[1, "1854-04-01", 1854, "Apr", 8571, 1, 0, 5, 1.4, 7],[2, "1854-05-01", "May", 1854, 23333, 12, 0, 9, 6.2, 0, 4.6],[3,  "1854-06-01", "Jun", 1854, 28333, 11, 0, 6, 4.7, 0, 2.5]]`
