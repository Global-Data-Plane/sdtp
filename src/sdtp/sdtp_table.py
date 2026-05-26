# Copyright (c) 2024-2025, The Regents of the University of California (Regents)
# All rights reserved.

import pandas as pd
import requests
import json
from typing import List, Dict, Any, Union, Callable, Optional
import os

from .sdtp_schema import ColumnSpec, RowTableSchema, RemoteTableSchema, ContainerTableSchema
from .sdtp_utils import InvalidDataException, type_check, convert_list_to_type, convert_rows_to_type_list, SDMLTypeConverter
from .sdtp_filter import SDQLFilter, make_filter

def _row_dict(row, columns):
    result = {}
    for i in range(len(columns)):
        result[columns[i]] = row[i]
    return result

def _convert_filter_result_to_format(rows, columns, schema_fields, format):
    result_rows = rows
    column_names = [entry['name'] for entry in schema_fields]
    column_indices = [column_names.index(column) for column in columns]
    result_rows = [[row[index] for index in column_indices] for row in rows]
            
    if format == 'list':
        return result_rows
        
    if format == 'dict':
        return [_row_dict(row, columns) for row in result_rows]
    # format is SDML, return a RowTable
    row_table_schema = [schema_fields[i] for i in column_indices]
    return RowTable(row_table_schema, result_rows)

ALLOWED_FILTERED_ROW_RESULT_FORMATS = {'dict', 'list', 'sdml'}
DEFAULT_FILTERED_ROW_RESULT_FORMAT = 'list'


class SDMLTable:
    """
    An SDMLTable. This is the abstract superclass for all Simple Data Markup Language tables, and 
    implements the schema methods of every SDML class. The data methods are implemented
    by the concrete classes. Any new SDMLTable class should:
    1. Subclass SDMLTable
    2. Have a constructor with the argument schema_fields (or accept a Pydantic spec model)
    3. call super(<classname>, self).__init__(schema_fields) in the constructor
    4. Implement the methods:
        (a) all_values(self, column_name)
        (b) range_spec(self, column_name)
        (c) _get_filtered_rows_from_filter(self, filter)
        (d) to_json(self)
    where:
        i. column_name is the name of the column to get the values/range_spec from
        ii. filter is a an instance of SDQLFilter
        iii. if columns is not None for get_filtered_rows, only return entries from those columns
            in the result from get_filtered_rows
            
    Arguments:
        schema_fields: a list of records of the form {"name": <column_name>, "type": <column_type>}.
           The column_type must be a type from galyleo_constants.SDTP_TYPES.
    """
    def __init__(self, schema_fields: List[dict]):
        self.schema_fields = schema_fields
        # Every concrete subclass must populate this property with its matching Pydantic model instance
        self._spec: Optional[Any] = None

    @property
    def schema(self) -> List[dict]:
        """Backward-compatible alias for schema_fields."""
        return self.schema_fields

    @schema.setter
    def schema(self, value: List[dict]) -> None:
        self.schema_fields = value

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, value) -> None:
        self._spec = value

    def column_names(self) -> List[str]:
        """Return the names of the columns"""
        return [column["name"] for column in self.schema_fields]

    def column_types(self) -> List[str]:
        """Return the types of the columns"""
        return [column["type"] for column in self.schema_fields]

    def get_column_type(self, column_name) -> Optional[str]:
        """
        Returns the type of column column_name, or None if this table doesn't have a column with
        name  column_name.

        Arguments:
            column_name(str): name of the column to get the type for
        """
        matches = [column["type"] for column in self.schema_fields if column["name"] == column_name]
        return matches[0] if len(matches) > 0 else None
    
    def all_values(self, column_name: str) -> list:
        """
        get all the values from column_name
        Arguments:
            column_name: name of the column to get the values for
           
        Returns:
            list: List of the values
        """
        raise NotImplementedError(f'all_values has not been implemented in {type(self).__name__}')
    
    def get_column(self, column_name: str) -> list:
        """
        get the column column_name
        Arguments:
            column_name: name of the column to get

        Returns:
            list: List of the values in the column
        """
        raise NotImplementedError(f'get_column has not been implemented in {type(self).__name__}')

    def range_spec(self, column_name: str) -> list:
        """
        Get the list [min_val, max_val] for column_name
        Arguments:
            column_name: name of the column to get the range spec for

        Returns:
            list: the minimum and maximum of the column
        """
        raise NotImplementedError(f'range_spec has not been implemented in {type(self).__name__}')
    
    def _get_filtered_rows_from_filter(self, filter=None):
        """
        Returns the rows for which the filter returns True. Returns a list of the matching rows

        Arguments:
            filter: A SDQLFilter
        Returns:
            The subset of self.get_rows() which pass the filter
        """
        raise NotImplementedError(f'_get_filtered_rows_from_filter has not been implemented in {type(self).__name__}')

    def get_filtered_rows(self, filter_spec=None, columns=None, format=DEFAULT_FILTERED_ROW_RESULT_FORMAT):
        """
        Filter the rows according to the specification given by filter_spec.
        Returns the rows for which the resulting filter returns True.

        Arguments:
            filter_spec(dict): Specification of the filter, as a dictionary
            columns(list): the names of the columns to return. Returns all columns if absent
            format(str): one of 'list', 'dict', 'sdml'. Default is list. 
        Returns:
            list: The subset of self.get_rows() which pass the filter in the format specified by format
        """
        if format is None: 
            format = DEFAULT_FILTERED_ROW_RESULT_FORMAT
        if format not in ALLOWED_FILTERED_ROW_RESULT_FORMATS:
            raise InvalidDataException(f'format for get_filtered rows must be one of {ALLOWED_FILTERED_ROW_RESULT_FORMATS}, not {format}')
        
        requested_columns = columns if columns else []
        filter_obj = make_filter(filter_spec) if filter_spec is not None else None
        rows = self._get_filtered_rows_from_filter(filter=filter_obj)
        columns_in_result = self.column_names() if len(requested_columns) == 0 else requested_columns
        return _convert_filter_result_to_format(rows, columns_in_result, self.schema_fields, format)

    def to_dictionary(self) -> dict:
        """
        Generate a complete dictionary specification representing the table instance.
        Natively leverages Pydantic to export a dictionary structured exactly 
        according to the table's formal schema model contract.
        """
        if self.spec and hasattr(self.spec, "model_dump"):
            return self.spec.model_dump(by_alias=True)
        raise NotImplementedError(f"Class '{self.__class__.__name__}' did not initialize a valid Pydantic model.")

    def to_json(self) -> str:
        """
        Generate a canonical wire-format JSON string representation of the table instance.
        Bypasses standard Python json.dumps overhead by using Pydantic's highly 
        optimized native serialization engine.
        """
        if self.spec and hasattr(self.spec, "model_dump_json"):
            return self.spec.model_dump_json(by_alias=True)
        raise NotImplementedError(f"Class '{self.__class__.__name__}' did not initialize a valid Pydantic model.")


class SDMLFixedTable(SDMLTable):
    """
    A SDMLFixedTable: This is a convenience class for subclasses which generate a fixed 
    number of rows locally, independent of filtering. This is instantiated with a function get_rows() which delivers the
    rows, rather than having them explicitly in the Table. Note that get_rows() *must* return 
    a list of rows, each of which has the appropriate number of entries of the appropriate types.
    all_values, range_spec, and _get_filtered_rows_from_filter are all implemented on top of 
    get_rows. Note that these methods can be overridden in a subclass if there is a
    more efficient method than the obvious implementation, which is what's implemented here.

    Arguments:
        schema_fields(List): a list of records of the form {"name": <column_name>, "type": <column_type>}.
            The column_type must be a type from galyleo_constants.SDTP_TYPES.
        get_rows (Callable): a function which returns a list of list of values. Each component list
            must have the same length as schema, and the jth element must be of the
            type specified in the jth element of schema
    """
    def __init__(self, schema_fields: list, get_rows: Callable[[], List]):
        super().__init__(schema_fields)
        self.get_rows = get_rows

    @property
    def spec(self) -> RowTableSchema:
        """Dynamically build a RowTable representation for universal serialization contracts."""
        return RowTableSchema(type="RowTable", schema=self.schema_fields, rows=self.get_rows())

    def _get_column_values_and_type(self, column_name: str):
        try:
            index = self.column_names().index(column_name)
        except ValueError as original_error:
            raise InvalidDataException(f'{column_name} is not a column of this table') from original_error
        sdtp_type = self.schema_fields[index]["type"]
        rows = self.get_rows()
        return ([row[index] for row in rows], sdtp_type)

    def all_values(self, column_name: str) -> list:
        """get all the values from column_name"""
        (values, sdtp_type) = self._get_column_values_and_type(column_name)
        result = list(set(values))
        result.sort()
        return result
    
    def get_column(self, column_name: str) -> list:
        """get all the column column_name"""
        (result, sdtp_type) = self._get_column_values_and_type(column_name)
        return result
    
    def check_column_type(self, column_name):
        """For testing. Makes sure that all the entries in column_name are the right type"""
        value_list = self.all_values(column_name)
        required_type = self.get_column_type(column_name)
        if required_type is not None:
            bad_values = [val for val in value_list if not type_check(required_type, val)]
        else:
            bad_values = []
        if len(bad_values) > 0:
            raise InvalidDataException(f'Values {bad_values} could not be converted to {required_type} in column {column_name}')

    def range_spec(self, column_name: str) -> list:
        """Get the dictionary {min_val, max_val} for column_name"""
        (values, sdtp_type) = self._get_column_values_and_type(column_name)
        if not values:
            return []
        values.sort()
        return [values[0], values[-1]]
    
    def _get_filtered_rows_from_filter(self, filter=None):
        """Returns the rows for which the filter returns True."""
        if filter is None:
            return self.get_rows()
        else:
            match_columns = self.column_names()
            return [row for row in self.get_rows() if filter.matches(row, match_columns)]

    def to_dataframe(self):
        """Convert the table to a PANDAS DataFrame."""
        return pd.DataFrame(self.get_rows(), columns=self.column_names())


class SDMLDataFrameTable(SDMLFixedTable):
    """
    A simple utility class to serve data from a PANDAS DataFrame. The general idea is 
    that the values are in the PANDAS Dataframe, which must have the same column names
    as the schema and compatible types.
    """
    def __init__(self, schema, dataframe, type_converter=None, converter_kwargs=None):
        super().__init__(schema, self._get_rows)
        self.dataframe = dataframe.copy()
        self.dataframe.columns = self.column_names()
        
        if type_converter is not None:
            tc = type_converter
        else:
            tc = SDMLTypeConverter(**(converter_kwargs or {}))
            
        for column in schema:
            column_values = self.dataframe[column["name"]].tolist()
            try:
                fixed_series = convert_list_to_type(column["type"], column_values, tc)
                self.dataframe[column["name"]] = fixed_series
            except Exception as exc:
                raise InvalidDataException(f'error {exc} converting {column["name"]}')
            
    def _get_column_and_type(self, column_name):
        try:
            index = self.column_names().index(column_name)
        except ValueError as original_error:
            raise InvalidDataException(f'{column_name} is not a column of this table') from original_error
        return {
            "type": self.schema_fields[index]["type"],
            "values": self.dataframe[column_name].to_list()
        }
    
    def all_values(self, column_name: str) -> list:
        type_and_values = self._get_column_and_type(column_name)
        result = list(set(type_and_values['values']))
        result.sort()
        return result
    
    def get_column(self, column_name: str) -> list:
        type_and_values = self._get_column_and_type(column_name)
        return type_and_values['values']

    def range_spec(self, column_name: str) -> list:
        type_and_values = self._get_column_and_type(column_name)
        result = list(set(type_and_values['values']))
        if len(result) == 0:
            return []
        result.sort()
        return [result[0], result[-1]]
         
    def _get_rows(self):
        return self.dataframe.values.tolist()

    def to_dataframe(self):
        return self.dataframe.copy()


class RowTable(SDMLFixedTable):
    """
    A simple utility class to serve data from a static list of rows, which
    can be constructed from a CSV file, Excel File, etc. The idea is to
    make it easy for users to create and upload simple datasets to be
    served from a general-purpose server. Note that this will need some
    authentication.
    """
    def __init__(self, spec_or_schema: Union[RowTableSchema, List[dict]], rows: Optional[List[List[Any]]] = None, type_converter=None, converter_kwargs=None):
        if isinstance(spec_or_schema, RowTableSchema):
            self._static_spec = spec_or_schema
            schema_fields = [col.model_dump() for col in spec_or_schema.schema_fields]
            self.rows = spec_or_schema.rows
        else:
            schema_fields = spec_or_schema
            self.rows = rows if rows is not None else []
            self._static_spec = RowTableSchema(type="RowTable", schema=schema_fields, rows=self.rows)

        type_list = [col["type"] for col in schema_fields]
        tc = type_converter if type_converter is not None else SDMLTypeConverter(**(converter_kwargs or {}))
        self.rows = convert_rows_to_type_list(type_list, self.rows, tc)
        
        super().__init__(schema_fields, self._get_rows)
    
    @property
    def spec(self) -> RowTableSchema:
        return self._static_spec

    def _get_rows(self):
        return [row for row in self.rows]


def _generate_ordered_lists(remoteRowTable, localRemoteTable, requestedColumns):
    def reorder_row(row, source_index_list, target_index_list):
        result = row.copy()
        for i in range(len(row)):
            result[target_index_list[i]] = row[source_index_list[i]]
        return result
    def get_index_list(table):
        table_columns = table.column_names()
        return [table_columns.index(column) for column in requestedColumns]
    source_index_list = get_index_list(remoteRowTable)
    target_index_list = get_index_list(localRemoteTable)
    return [reorder_row(row, source_index_list, target_index_list) for row in remoteRowTable.rows]

def _make_headers(auth_info, header_dict):
    has_auth = auth_info is not None and (hasattr(auth_info, "type") or "type" in auth_info)
    if not has_auth:
        return header_dict.copy() if header_dict is not None else None
        
    # Standardize access paths regardless of whether auth_info is a Pydantic object or dictionary record
    auth_type = auth_info.type if hasattr(auth_info, "type") else auth_info["type"]
    auth_token = None
    headers = {}

    if auth_type == 'env':
        env_var = auth_info.env_var if hasattr(auth_info, "env_var") else auth_info["env_var"]
        auth_token = os.environ.get(env_var)
        if not auth_token:
            raise ValueError(f"Environment variable {env_var} not set")
    elif auth_type == 'file':
        path = auth_info.path if hasattr(auth_info, "path") else auth_info["path"]
        if not os.path.isfile(path):
            raise ValueError(f"Auth file {path} not found")
        with open(path, "r") as f:
            auth_token = f.read().strip()
    elif auth_type == 'token':
        auth_token = auth_info.value if hasattr(auth_info, "value") else auth_info["value"]
    else:
        raise ValueError(f"Unsupported auth type: {auth_type}")

    if auth_token is not None:
        headers = {"Authorization": f"Bearer {auth_token}"}
    if header_dict is not None:
        for (key, value) in header_dict.items():
            headers[key] = value
    return None if headers == {} else headers


class RemoteSDMLTable(SDMLTable):
    """
    A SDTP Table on a remote server. This just has a schema, an URL, and 
    header variables. This is the primary class for the client side of the SDTP,
    and in many packages would be a separate client module. However, the SDTP is 
    designed so that Remote Tables can be used to serve local tables, so this 
    is part of a server-side framework to.
    Parameters:
        table_name: name of the remote table
        schema: schema of the remote table
        url: url of the server hosting the remote table
        auth: dictionary or model of variables and values required to access the table
    Throws:
        InvalidDataException if the table doesn't exist on the server, the 
        url is unreachable, the schema doesn't match the downloaded schema
    """ 
    def __init__(self, spec: RemoteTableSchema, schema=None, url=None, auth=None, header_dict=None): 
        if not isinstance(spec, (RemoteTableSchema, ContainerTableSchema)):
            spec = RemoteTableSchema(
                type="RemoteSDMLTable",
                table_name=spec,
                schema=schema,
                url=url,
                auth=auth,
                header_dict=header_dict,
            )
        schema_fields = [col.model_dump() for col in spec.schema_fields]
        super().__init__(schema_fields)
        # ---------------------------------------------------------------------
        # ARCHITECTURAL NOTE: UNIFIED SERIALIZATION CONTRACT
        # ---------------------------------------------------------------------
        # We deliberately allow this constructor to accept either a RemoteTableSchema
        # or a ContainerTableSchema instead of forcing ContainerTable to manufacture
        # a fake or incomplete generic Remote table spec block.
        #
        # By storing the unadulterated, native schema model directly inside `self.spec`,
        # the base class `SDMLTable.to_dictionary()` and `to_json()` methods can 
        # seamlessly output the correct declarative wire-format layouts (e.g., 
        # exporting the true 'ContainerTable' type and 'container' block keys)
        # without duplicating initialization or serialization boilerplate.
        #
        # Attributes unique to a standalone remote server are safely extracted via 
        # `getattr`. For ContainerTable, these default to None and are resolved/overridden 
        # dynamically at runtime via the deployment cluster's ServiceResolver.
        # ---------------------------------------------------------------------
        
        # Lock down the true native spec model instance
        self.spec = spec
        self.table_name = spec.table_name
        
        # Use safe inspection to gracefully support local container schemas
        self.url = getattr(spec, "url", None)
        self.auth = getattr(spec, "auth", None)
        self.header_dict = getattr(spec, "header_dict", None)
        
        self.headers = _make_headers(self.auth, self.header_dict)
        self.ok = False

    def _connect_error(self, msg):
        self.ok = False
        raise InvalidDataException(f'Error: {msg}')

    def _check_entry_match(self, schema, index, field, mismatches):
        if self.schema_fields[index][field] == schema[index][field]: 
            return
        mismatches.append(f'Mismatch in field {field} at entry {index}. Server value: {schema[index][field]}, declared value: {self.schema_fields[index][field]}')

    def _check_schema_match(self, schema):
        if len(schema) != len(self.schema_fields):
            self._connect_error(f'Server schema has {len(schema)} columns, declared schema has {len(self.schema_fields)} columns')
        mismatches = []
        for i in range(len(schema)):
            self._check_entry_match(schema, i, "name", mismatches)
            self._check_entry_match(schema, i, "type", mismatches)
        if len(mismatches) > 0:
            self._connect_error('Schema mismatch: ' + ', '.join(mismatches))

    def _execute_get_request(self, url):
        if self.headers:
            return requests.get(url, headers=self.headers)
        return requests.get(url)
        
    def connect_with_server(self):
        """
        Connect with the server, ensuring that the server is:
        a. a SDTP server
        b. has self.table_name in its list of tables
        c. the table there has a matching schema
        """
        try:
            response = self._execute_get_request(f'{self.url}/get_tables')
            if response.status_code >= 300:
                self._connect_error(f'Bad connection with {self.url}: code {response.status_code}')
        except Exception as e:
            self._connect_error(f'Error connecting with {self.url}/get_tables: {repr(e)}')
        try:
            server_tables = response.json()
        except Exception as e:
            self._connect_error(f'Error {repr(e)} reading tables from {self.url}/get_tables')
            
        if self.table_name in server_tables:
            server_schema = server_tables[self.table_name]
            self._check_schema_match(server_schema)
        else:
            self._connect_error(f'Server at {self.url} does not have table {self.table_name}')
        self.ok = True
    
    def _check_column_and_get_type(self, column_name):
         if column_name not in self.column_names():
            raise InvalidDataException(f'Column {column_name} is not a column of {self.table_name}')
         return self.get_column_type(column_name)
        
    def _do_request(self, request):
        if not self.ok:
            self.connect_with_server()
        try:
            response = self._execute_get_request(request)
            if response.status_code >= 300:
                raise InvalidDataException(f'{request} returned error code {response.status_code}')
            return response.json()
        except Exception as exc:
            raise InvalidDataException(f'Exception {repr(exc)} occurred in {request}')
        
    def _execute_column_route(self, column_name, route):
        column_type = self._check_column_and_get_type(column_name)
        request = f'{self.url}/{route}?table_name={self.table_name}&column_name={column_name}'
        result = self._do_request(request)
        return convert_list_to_type(column_type, result, SDMLTypeConverter())
        
    def all_values(self, column_name: str) -> list:
        return self._execute_column_route(column_name, 'get_all_values')
        
    def get_column(self, column_name: str) -> list:
        return self._execute_column_route(column_name, 'get_column')

    def range_spec(self, column_name: str) -> list:
        return self._execute_column_route(column_name, 'get_range_spec')
    
    def _get_filtered_rows_from_remote(self, filter_spec=None, columns=None):
        if not self.ok:
            self.connect_with_server()
        request = f'{self.url}/get_filtered_rows'
        data = {'table': self.table_name, 'result_format': 'sdml'}
        if filter_spec:
            data['filter'] = filter_spec
        if columns is not None and len(columns) > 0:
            data['columns'] = columns
        
        try:
            response = requests.post(request, json=data, headers=self.headers) if self.headers is not None else requests.post(request, json=data)
            if response.status_code >= 300:
                raise InvalidDataException(f'get_filtered_rows to {self.url}: caused error response {response.status_code}')
            
            # The global direct-to-class TableBuilder resolves the incoming RowTable response matrix cleanly
            from .sdtp_table_factory import TableBuilder
            return TableBuilder.build_table(response.json())
        except Exception as exc:
            raise InvalidDataException(f'Error in get_filtered_rows to {self.url}: {repr(exc)}')

    def _get_filtered_rows_from_filter(self, filter=None) -> list:
        filter_spec = None if filter is None else filter.to_filter_spec()
        return self._get_filtered_rows_from_remote(filter_spec, columns=[]).get_rows()
    
    def get_filtered_rows(self, filter_spec=None, columns=None, format=DEFAULT_FILTERED_ROW_RESULT_FORMAT) -> Union[list, list[dict[str, Any]], RowTable]:
        if format is None: 
            format = DEFAULT_FILTERED_ROW_RESULT_FORMAT
        requested_columns = columns if columns else []
        
        if format not in ALLOWED_FILTERED_ROW_RESULT_FORMATS:
            raise InvalidDataException(f'format for get_filtered rows must be one of {ALLOWED_FILTERED_ROW_RESULT_FORMATS}, not {format}')
       
        remoteRowTable = self._get_filtered_rows_from_remote(filter_spec, columns=requested_columns)
        if format == 'list':
            column_names = self.column_names() if len(requested_columns) == 0 else requested_columns
            return _generate_ordered_lists(remoteRowTable, self, column_names)
        elif format == 'dict':
            result_columns = remoteRowTable.column_names()
            return [_row_dict(row, result_columns) for row in remoteRowTable.rows]
        else:
            return remoteRowTable


class ContainerTable(RemoteSDMLTable):
    """
    A table whose data is provided by a Docker container running in the same
    deployment environment (docker-compose, Kubernetes, Cloud Run, etc.).
    It behaves like a RemoteSDMLTable, but the URL is resolved at runtime
    from the logical service_name.
    """
    def __init__(self, spec: ContainerTableSchema):
        # Translate to RemoteTableSchema properties for superclass proxy processing
        
        super().__init__(spec)
        self.service_name = spec.container.service_name
        self.env = spec.container.env


# Direct direct-to-class registrations on boot, completely omitting legacy factories
from .sdtp_table_factory import (
    ContainerTableFactory,
    RemoteSDMLTableFactory,
    RowTableFactory,
    TableBuilder,
)
TableBuilder.register_factory_class('RowTable', RowTableFactory, locked=True)
TableBuilder.register_factory_class('RemoteSDMLTable', RemoteSDMLTableFactory, locked=True)
TableBuilder.register_factory_class('ContainerTable', ContainerTableFactory, locked=True)
