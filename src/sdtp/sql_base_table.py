

from .sdtp_table import SDMLTable, RowTable, ALLOWED_FILTERED_ROW_RESULT_FORMATS, DEFAULT_FILTERED_ROW_RESULT_FORMAT
from .sdtp_utils import InvalidDataException
from .sdtp_filter import SDQLFilter

class BaseSQLTable(SDMLTable):
    """
    An abstract intermediate superclass for all relational SQL-backed SDML tables.
    
    This class handles universal query compilation by automatically translating SDQL 
    filter specifications into parameterized SQL syntax. It overrides the high-level 
    query pipeline to enforce full projection pushdown and predicate pushdown natively, 
    completely eliminating the need to parse raw records in Python memory state.
    
    Any new database extension using a relational SQL engine should:
    1. Subclass BaseSQLTable.
    2. Have a constructor accepting at least the arguments 'schema' and 'table_name'.
    3. Call super(<classname>, self).__init__(schema, table_name) in the constructor.
    4. Implement the following data execution methods:
        (a) _execute_sql(self, query: str, params: list = None) -> list
        (b) all_values(self, column_name: str) -> list
        (c) range_spec(self, column_name: str) -> list
    5. Optionally implement the following dialect customization hook:
        (a) _compile_dialect_operator(self, operator: str, column: str, spec: dict) -> tuple[str, list]
        
    where:
        i. query is a fully assembled SQL string containing standard placeholder tokens ('?') for variables.
        ii. params is a list of Python primitive values bound to match the query placeholder tokens in order.
        iii. column_name is the validated identifier string of a target column.
        iv. operator is an unrecognized atomic SDQL filter string token (e.g., 'REGEX_MATCH').
        v. spec is the raw dictionary segment representing an atomic filter condition.

    Arguments:
        schema (list): A list of dictionary records of the exact structural form 
            {"name": <column_name>, "type": <column_type>}, where column_type matches 
            a type string registered in sdtp_schema.SDML_SCHEMA_TYPES.
        table_name (str): The physical table identifier string representing the target 
            dataset layer located inside the underlying relational database instance.
    """
    
    def __init__(self, schema: list, table_name: str):
        super().__init__(schema)
        self.table_name = table_name

    def _validate_column(self, column_name: str):
        if column_name not in self.column_names():
            raise InvalidDataException(f"'{column_name}' is not a valid column of table '{self.table_name}'")

    def _execute_sql(self, query: str, params: list|None = None) -> list:
        """
        Execute a compiled, parameterized SQL query string against the underlying 
        database engine driver and return the raw relational rows.

        This is an abstract backend hook that MUST be overridden by concrete 
        subclasses (e.g., DuckDBTable, SQLiteTable). It serves as the terminal 
        bridge between the abstract SDQL query translation layer and the physical 
        database connection instance. 

        Implementations must use the underlying database driver's native execution 
        mechanisms to safely bind positional parameter variables to '?' placeholders. 
        This prevents malicious SQL injection attacks and enables the database engine 
        to cache compiled query execution plans.

        Arguments:
            query (str): A valid, fully composed SQL statement string (typically a 
                SELECT statement) utilizing standard '?' placeholder tokens for 
                variable insertion.
            params (list, optional): An ordered sequence of Python primitive data 
                values (strings, numbers, booleans, dates, etc.) that correspond 
                exactly to the positional placeholder tokens located inside the 
                query string. Defaults to None if the query contains no variables.

        Returns:
            list: A list of rows representing the database query results, where 
                each individual row is formatted strictly as a list of Python 
                primitive values (i.e., a matrix pattern: list[list[Any]]). 
                The order of elements within each nested row list must exactly mirror 
                the vertical column projection sequence defined in the SELECT clause 
                of the query. If no records match the criteria, 
                this method must return an empty list ([]).

        Raises:
            InvalidDataException: If a low-level driver connectivity error occurs, 
                the SQL engine throws a syntax compilation failure, or internal 
                data-type conversions fail.
            NotImplementedError: If a child database extension fails to override 
                this execution handler.
        """
        raise NotImplementedError("_execute_sql must be implemented by the database subclass")

    def _compile_dialect_operator(self, operator: str, column: str, spec: dict) -> tuple[str, list]:
        """
        An optional polymorphic hook to compile vendor-specific or dialect-dependent 
        SDQL filter operations into a localized SQL predicate fragment.

        This method is designed to be overridden by concrete database subclasses 
        (such as DuckDBTable or SQLiteTable) to isolate database engine quirks—like 
        regular expression matching syntax, full-text search operators, or specialized 
        string pattern expressions. 

        The parent `BaseSQLTable._compile_filter_spec` method handles all standard, 
        universal operations (like 'IN_LIST', 'GE', 'LE', etc.) automatically. 
        If an atomic operator is not universally supported, it is passed down to this 
        method to allow the child extension to emit custom SQL string fragments.

        Arguments:
            operator (str): The unique string identifier token representing the unhandled 
                atomic filter condition (for example, 'REGEX_MATCH').
            column (str): The pre-validated string identifier of the target column 
                being evaluated by the filter query.
            spec (dict): The complete raw dictionary segment representing the atomic 
                filter condition block, containing all metadata properties required 
                to generate the segment (such as 'expression' or 'value').

        Returns:
            tuple[str, list]: A two-element tuple containing the SQL string expression 
                and its corresponding list of bind values:
                - The first element must be a valid SQL clause fragment utilizing standard 
                  '?' positional parameters for variable values (e.g., "column REGEXP ?").
                - The second element must be a list containing the matching Python primitive 
                  bind variables to be packed into the master driver execution sequence.
                If the child extension does not recognize or support the requested 
                operator, it must return an empty query statement and empty bind array: ("", []).

        Examples:
            ### Concrete Implementation Example for a DuckDB Extension:
            def _compile_dialect_operator(self, operator: str, column: str, spec: dict) -> tuple[str, list]:
                if operator == "REGEX_MATCH":
                    # DuckDB utilizes the standard functional POSIX wrapper: REGEXP_MATCHES(col, pattern)
                    return f"REGEXP_MATCHES({column}, ?)", [spec.get("expression")]
                return "", []

            ### Concrete Implementation Example for a SQLite Extension:
            def _compile_dialect_operator(self, operator: str, column: str, spec: dict) -> tuple[str, list]:
                if operator == "REGEX_MATCH":
                    # SQLite utilizes an infix custom registered function notation: col REGEXP pattern
                    return f"{column} REGEXP ?", [spec.get("expression")]
                return "", []
        """
        return "", []

    def _handle_nulls(self, sdql_operator: str) -> tuple[str, list]:
        """
            Handle the fallback case where no sub-arguments were provided to a compound SDQL operator.

            This method is called exclusively from `self._compile_filter_spec` when a logical 
            quantifier block contains an empty arguments array. It isolates the 
            parameterized SQL return structure for empty sets, allowing concrete database 
            extensions to easily customize or override default evaluation behavior.

            Empty/Null Parameter Alignment Rules:
            To guarantee identical row-evaluation parity between the SQL execution engine 
            and the framework's in-memory Python fallback routines (`sdtp_filter.py`), 
            empty structural argument arrays are translated into absolute SQL boolean constants:
            - An empty 'ALL' constraint yields "1=1" (Vacuous Truth).
            - An empty 'ANY' constraint yields "1=0" (Absolute Falsehood).
            - An empty 'NONE' constraint yields "1=1" (Absolute Truth).

            Subclasses overriding this method must handle all three valid operator states 
            and preserve the identical two-element tuple return signature.

            Arguments:
                sdql_operator (str): The logical quantifier string token being evaluated. 
                    Must be one of 'ALL', 'ANY', or 'NONE'.

            Returns:
                tuple[str, list]: A two-element tuple managing query parameters safely:
                    - The first element is a valid, isolated SQL boolean expression string 
                    (e.g., "1=1" or "1=0").
                    - The second element is an empty list ([]) representing the absent 
                    positional bind parameters.

            Raises:
                InvalidDataException: If an unrecognized or invalid compound operator string 
                token is passed into the handler.
        """
        null_argument_result = {"ALL": "1=1", "ANY": "1=0", "NONE": "1=1"}
        
        if sdql_operator not in null_argument_result:
            raise InvalidDataException(
                f"Invalid compound operator '{sdql_operator}' passed to _handle_nulls. "
                f"Expected one of {set(null_argument_result.keys())}."
            )
            
        return null_argument_result[sdql_operator], []
                

    def _compile_filter_spec(self, spec: dict) -> tuple[str, list]:
        """
        Recursively compile an abstract SDQL filter specification dictionary into 
        a parameterized SQL condition string and a matching list of bind variables.

        This method serves as the core, deterministic translation engine of 
        `BaseSQLTable`. It automatically traverses the nested structural tree of 
        an SDQL filter AST, unrolling high-level logical quantifiers and mapping 
        atomic conditions to standard relational SQL syntax.

        CRITICAL ARCHITECTURAL NOTE: 
        This method is universally optimized and SHOULD NOT be overridden by concrete 
        subclasses. Subclasses that require support for vendor-specific SQL operators 
        (such as regular expressions or custom full-text search macros) must instead 
        implement the polymorphic hook method `_compile_dialect_operator`.

        Logical Quantifier Compilation Rules:
        - 'ALL' maps directly to a sequence of predicates joined by 'AND' tokens.
        - 'ANY' maps directly to a sequence of predicates joined by 'OR' tokens.
        - 'NONE' unrolls a collection of conditions into a unified 'NOT ((f1) OR (f2))' block.

        
        Arguments:
            spec (dict): A standardized dictionary representing either a compound 
                logical filter node or an atomic column comparison condition. 
                Typically obtained via a client-side filter object invocation 
                of `SDQLFilter.to_filter_spec()`.

        Returns:
            tuple[str, list]: A two-element tuple managing query parameters safely:
                - The first element is a valid SQL fragment string representing an evaluation 
                  predicate or a collection of grouped sub-clauses utilizing standard 
                  '?' positional bind placeholders.
                - The second element is a flat list containing the matching ordered group 
                  of Python primitive data variables corresponding to the placeholders.
                Returns ("", []) if the input specification is structural noise, invalid, 
                or empty.

        Raises:
            InvalidDataException: If an atomic clause refers to an identifier that 
                fails validation against the master table column registry.
        """
        if not isinstance(spec, dict) or "operator" not in spec:
            return "", []

        operator = spec["operator"]

        # 1. Handle Set-Quantifier Compound Operators (ALL, ANY, NONE)
        # The basic idea is that ALL means all arguments are satified (SQL AND)

        if operator in ("ALL", "ANY", "NONE"):
            arguments = spec.get("arguments", [])
            if not arguments:
                return self._handle_nulls(operator)

            sub_clauses, params = [], []
            for sub_spec in arguments:
                clause, sub_params = self._compile_filter_spec(sub_spec)
                if clause:
                    sub_clauses.append(f"({clause})")
                    params.extend(sub_params)

            if not sub_clauses:
                return self._handle_nulls(operator)

            if operator == "ALL":
                return " AND ".join(sub_clauses), params
            elif operator == "ANY":
                return " OR ".join(sub_clauses), params
            elif operator == "NONE":
                return f"NOT ({" OR ".join(sub_clauses)})", params

        # 2. Extract Atomic Column Constraints
        column = spec.get("column")
        if not column:
            return "", []
        self._validate_column(column)

        # Handle universal IN_LIST syntax
        if operator == "IN_LIST":
            values = spec.get("values", [])
            if not values:
                return "1=0", []
            if len(values) == 1:
                return f"{column} = ?", [values[0]]
            placeholders = ", ".join(["?"] * len(values))
            return f"{column} IN ({placeholders})", list(values)

        # Handle universal Comparison Operators
        if operator in ("GE", "GT", "LE", "LT"):
            sql_ops = {"GE": ">=", "GT": ">", "LE": "<=", "LT": "<"}
            return f"{column} {sql_ops[operator]} ?", [spec.get("value")]

        # 3. Delegate Dialect Customizations (e.g., Regex) to the Child Extension
        return self._compile_dialect_operator(operator, column, spec)

    def get_filtered_rows(self, filter_spec=None, columns=None, format=DEFAULT_FILTERED_ROW_RESULT_FORMAT):
        """
        Intercept the query pipeline to execute high-performance projection and 
        predicate pushdowns directly inside the relational database engine.

        Instead of pulling a full dataset into Python memory state and filtering row-by-row, 
        this method overrides the abstract `SDMLTable` routine. It compiles the query 
        constraints into an optimized SQL command, delegates execution to the child driver, 
        and bypasses unnecessary processing loops entirely.

        Execution Pipeline:
        1. **Format Validation**: Ensures the requested return structure is supported.
        2. **Projection Pushdown**: Slices the SQL query vertically, selecting only the column 
           identifiers explicitly requested by the caller. If no columns are provided, it 
           defaults to a full projection of the schema.
        3. **Predicate Pushdown**: Recursively unrolls the incoming `filter_spec` tree structure 
           into an isolated, parameterized SQL WHERE clause via `_compile_filter_spec`.
        4. **Engine Query Execution**: Dispatches the assembled SQL string and bound primitive 
           parameters down to the database-specific driver hook via `_execute_sql`.
        5. **Transposition & Wrap**: Packages the raw relational row matrices into the final 
           requested serialization state (`list`, `dict`, or an isolated `RowTable` instance).

        Arguments:
            filter_spec (dict or SDQLFilter, optional): An abstract query condition tree defining 
                how records should be filtered. Accepts either a raw specification dictionary 
                or a fully instantiated `SDQLFilter` subclass object. Defaults to None, 
                which triggers an unconditional full table scan.
            columns (list of str, optional): An ordered sequence of column name strings to restrict 
                the projection results to. Defaults to None, which extracts every column registered 
                in the table schema.
            format (str, optional): The target data layout format requested for transmission or consumption. 
                Must match one of the string tokens registered in `ALLOWED_FILTERED_ROW_RESULT_FORMATS`. 
                Defaults to `DEFAULT_FILTERED_ROW_RESULT_FORMAT`.

        Returns:
            Union[list[list], list[dict], RowTable]: The query results mapped to the requested format:
                - If format is `'list'`: Returns a matrix array of values (`list[list[PrimitiveType]]`).
                - If format is `'dict'`: Returns an array of flat column-to-value dictionaries (`list[dict[str, PrimitiveType]]`).
                - If format is `'sdml'`: Returns a new, independent `RowTable` instance instantiated using 
                  the vertically projected column schema slice and the matching records list.

        Raises:
            InvalidDataException: Occurs if an unsupported format string token is supplied, a requested column 
                identifier fails internal registry schema validation, or the underlying database driver 
                encounters a low-level query execution or connectivity fault.
        """
        if format is None:
            format = DEFAULT_FILTERED_ROW_RESULT_FORMAT
        if format not in ALLOWED_FILTERED_ROW_RESULT_FORMATS:
            raise InvalidDataException(
                f"Invalid format specification: '{format}'. "
                f"Expected one of {ALLOWED_FILTERED_ROW_RESULT_FORMATS}."
            )

        # Step 1: Execute Projection Pushdown
        requested_columns = columns if columns else self.column_names()
        select_clause = ", ".join(requested_columns)

        # Step 2: Unpack and Compile Predicate Pushdown Tree
        where_clause, params = "", []
        if filter_spec:
            # Safely extract specs from either raw dicts or live Pydantic filter objects
            normalized_spec = filter_spec.to_filter_spec() if isinstance(filter_spec, SDQLFilter) else filter_spec
            
            # Intercept and unroll any shorthand IN_RANGE filters before parsing
            if normalized_spec.get("operator") == "IN_RANGE":
                from sdtp.sdtp_filter import expand_in_range_spec
                normalized_spec = expand_in_range_spec(normalized_spec)
                
            where_clause, params = self._compile_filter_spec(normalized_spec)

        # Step 3: Assemble Master SQL Query
        query = f"SELECT {select_clause} FROM {self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        # Step 4: Dispatch Query to the Database Engine via Subclass Driver Hook
        raw_rows = self._execute_sql(query, params)

        # Step 5: Convert Matrix Array to the Targeted Transport Layout Output
        if format == 'list':
            return raw_rows
            
        if format == 'dict':
            return [{requested_columns[i]: row[i] for i in range(len(requested_columns))} for row in raw_rows]

        # Format is 'sdml': generate a targeted RowTable on the dynamically sliced schema
        column_indices = [self.column_names().index(col) for col in requested_columns]
        projected_schema = [self.schema[i] for i in column_indices]
        return RowTable(projected_schema, raw_rows)