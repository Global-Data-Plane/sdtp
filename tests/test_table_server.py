# BSD 3-Clause License

# Copyright (c) 2024, The Regents of the University of California (Regents)
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Run tests on the table server, the middleware that sits between the data plane structures
and the data plane server
'''
import pytest
import sys
import requests

sys.path.append('src')
sys.path.append('tests')

from sdtp import TableServer, TableNotFoundException, ColumnNotFoundException
from sdtp import RowTable, SDMLTableFactory
from sdtp import InvalidDataException, SDML_STRING
import os
from json import load

TEST_URL_DIR = 'https://raw.githubusercontent.com/engageLively/sdtp/main/tests/tables/'

from sdtp.table_server import _check_dict_and_keys, _check_type, _check_table_spec, _check_valid_form

def test_check_type():
    _check_type(3, int, 'Int type check test')
    _check_type('foo', str, 'String type check test')
    _check_type({'foo': 2}, dict, 'Dict  type check test')
    test_table = RowTable([{"name": "a", "type": SDML_STRING}], [['foo']])
    _check_type(test_table, RowTable, 'RowTable type check test')
    with pytest.raises(AssertionError):
        _check_type(None, str, 'foo')
    with pytest.raises(AssertionError):
        _check_type(3, str, 'foo')
    with pytest.raises(AssertionError):
        _check_type('foo', int, 'foo')
    with pytest.raises(AssertionError):
        _check_type(3, RowTable, 'foo')
    with pytest.raises(AssertionError):
        _check_type(test_table, str, 'foo')

def test_check_dict_and_keys():
    test_dict = {'a': '1', 'b': '2'}
    _check_dict_and_keys(test_dict, {'a', 'b'}, ' dictionary test 1', 'test_dict')
    _check_dict_and_keys(test_dict, {'a'}, ' dictionary test 2', 'test_dict')
    _check_dict_and_keys(test_dict, {}, ' dictionary test 3', 'test_dict')
    _check_dict_and_keys(test_dict, None, ' dictionary test 4', 'test_dict')
    with pytest.raises(AssertionError):
        _check_dict_and_keys(None, {'a', 'b'}, ' dictionary test 5', 'test_dict')
    with pytest.raises(AssertionError):
        _check_dict_and_keys('foo', {'a', 'b'}, ' dictionary test 6', 'test_dict')
    with pytest.raises(AssertionError):
        _check_dict_and_keys(test_dict, {'a', 'c'}, ' dictionary test 7', 'test_dict')
    

def test_check_table_spec():
    test_table = RowTable([{"name": "a", "type": SDML_STRING}], [['foo']])
    with pytest.raises(AssertionError):
        _check_table_spec(None)
    with pytest.raises(AssertionError):
        _check_table_spec({'foo': 3})
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 'foo'})
    with pytest.raises(AssertionError):
        _check_table_spec({'table': test_table})
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 2, 'table': test_table})
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 'foo', 'table': 'bar'})
    _check_table_spec({'name': 'foo', 'table': test_table})

def test_check_table_spec():
    test_table = RowTable([{"name": "a", "type": SDML_STRING}], [['foo']])
    # test for None
    with pytest.raises(AssertionError):
        _check_table_spec(None)
    # test for missing keys
    with pytest.raises(AssertionError):
        _check_table_spec({'foo': 3})
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 'foo'})
    with pytest.raises(AssertionError):
        _check_table_spec({'table': test_table})
    # test for bad name
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 2, 'table': test_table})
    # test for None table
    with pytest.raises(AssertionError):
        _check_table_spec({'name': 'foo', 'table': 'bar'})
    # test for a good table
    _check_table_spec({'name': 'foo', 'table': test_table})

def test_check_valid_form():
    schema = [{"name": "a", "type": SDML_STRING}]
    rows = [['Alice']]
    test_table_spec_good = {'type': 'RowTable', 'schema': schema, 'rows': rows}
    test_table_spec_no_type = {'schema': schema, 'rows': rows}
    test_table_spec_no_schema = {'type': 'RowTable',  'rows': rows}
    # test for None
    with pytest.raises(AssertionError):
        _check_valid_form(None)
    # test for missing keys
    with pytest.raises(AssertionError):
        _check_valid_form({'foo': 3})
    with pytest.raises(AssertionError):
         _check_valid_form({'name': 'foo'})
    with pytest.raises(AssertionError):
         _check_valid_form({'table': test_table_spec_good})
    # test for bad name
    with pytest.raises(AssertionError):
         _check_valid_form({'name': 2, 'table': test_table_spec_good})
    # test for None table
    with pytest.raises(AssertionError):
         _check_valid_form({'name': 'foo', 'table': None})
    # test for missing keys in table
    with pytest.raises(AssertionError):
         _check_valid_form({'name': 'foo', 'table': test_table_spec_no_schema})
    with pytest.raises(AssertionError):
         _check_valid_form({'name': 'foo', 'table': test_table_spec_no_type})
    # test for a good table
    _check_valid_form({'name': 'foo', 'table': test_table_spec_good})


def test_table_server_creation():
    server = TableServer()
    # check the factories were initialized
    assert(server.factories.keys() == {'RowTable', 'RemoteSDMLTable'})
    for factory in server.factories.values():
        assert isinstance(factory, SDMLTableFactory)

class TestTableFactory(SDMLTableFactory):
    '''
    A simple SDMLTableFactory to test add_table_factory
    '''
    def __init__(self):
        super(TestTableFactory, self).__init__('TestTable')
    
    def build_table(self, table_spec):
        # Since this is just a test, don't do anything different 
        # than a RowTableFactory and take the same spec
        super(TestTableFactory, self).build_table(table_spec)
        return RowTable(table_spec["schema"], table_spec["rows"])

def test_add_table_factory():
    table_factory = TestTableFactory()
    server = TableServer()
    # test for None
    with pytest.raises(AssertionError):
        server.add_table_factory(None)
    # test for non-factory
    with pytest.raises(AssertionError):
        server.add_table_factory('foo')
    # test that the add was done successfully
    server.add_table_factory(table_factory)
    assert('TestTable' in server.factories.keys())
    assert(server.factories['TestTable'] == table_factory)

def _check_table_key_present(server, key, table):
    assert(key in server.servers.keys())
    assert(server.servers[key] == table)
    
        

def test_add_table():
    test_table = RowTable([{"name": "a", "type": SDML_STRING}], [['foo']])
    server = TableServer()
    # test for a bad spec.  We've already ensured that bad table specs get 
    # caught, so one bad table spec is enough
    with pytest.raises(AssertionError):
        server.add_sdtp_table({'name': 'foo', 'table': 'bar'})
    # add a table and make sure it's in the list
    server.add_sdtp_table({'name': 'foo', 'table': test_table})
    _check_table_key_present(server, 'foo', test_table)
    test_table_1 = RowTable([{"name": "b", "type": SDML_STRING}], [['foo']])
    # check to make sure add_table replaces an existing table if the key is the same
    server.add_sdtp_table({'name': 'foo', 'table': test_table_1})
    _check_table_key_present(server, 'foo', test_table_1)


def test_add_sdtp_table_from_dictionary():
    schema = [{"name": "a", "type": SDML_STRING}]
    rows = [['Alice']]
    test_table_spec_row = {'type': 'RowTable', 'schema': schema, 'rows': rows}
    test_table_spec_test = {'type': 'TestTable', 'schema': schema, 'rows': rows}
    server = TableServer()
    # test for a bad spec
    # as with test_add_sdtp_table, we only need to test one bad case
    with pytest.raises(AssertionError):
        server.add_sdtp_table_from_dictionary({'table': test_table_spec_row}) # missing name
    # test for a non-existent factory.  Haven't added TestTableFactory yet
    with pytest.raises(InvalidDataException):
        server.add_sdtp_table_from_dictionary({'name': 'test_table', 'table': test_table_spec_test})
    # test for a valid factory (make sure it's added)
    server.add_sdtp_table_from_dictionary({'name': 'row_table', 'table': test_table_spec_row})
    assert('row_table' in server.servers.keys())
    # add a new factory, then table, make sure it works
    server.add_table_factory(TestTableFactory())
    server.add_sdtp_table_from_dictionary({'name': 'test_table', 'table': test_table_spec_test})
    assert('row_table' in server.servers.keys())
    assert('test_table' in server.servers.keys())

def test_get_all_tables():
    # check an empty server
    server = TableServer()
    assert(len(server.get_all_tables()) == 0)
    schema = [{"name": "a", "type": SDML_STRING}]
    rows = [['Alice']]
    rows2 = [['Bob']]
    table = RowTable(schema, rows)
    table1 = RowTable(schema, rows2)
    # check getting a table works
    server.add_sdtp_table({'name': 'table1', 'table': table})
    assert(list(server.get_all_tables()) == [table])
    # check making sure adding a table with the same name overwrites, doesn't add
    server.add_sdtp_table({'name': 'table1', 'table': table1})
    assert(list(server.get_all_tables()) == [table1])
    # check adding a table
    server.add_sdtp_table({'name': 'table', 'table': table})
    table_list = server.get_all_tables()
    assert(len(table_list) == 2)
    assert(table in table_list)
    assert(table1 in table_list)

# server_test_tables is in the same directory as the tests

from server_test_tables import test_tables

def test_get_table():
    table_server = TableServer()
    # Test getting tables, including all corner cases
    # Table -- None and bad key
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_table(None)
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_table('foo')
    # For the tables, first, before we add we should get an error,
    # and after we add should get the table back
    for entry in test_tables:
        with pytest.raises(TableNotFoundException) as err:
            table_server.get_table(entry['name'])
        table_server.add_sdtp_table(entry)
        found = table_server.get_table(entry['name'])
        assert(found == entry['table'])
        

def test_get_all_values():
    table_server = TableServer()
    # Test getting tables, including all corner cases
    # Table -- None and bad key
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_all_values(None, 'foo')
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_all_values('foo', 'foo')
    for entry in test_tables:
        with pytest.raises(TableNotFoundException) as err:
            table_server.get_all_values(entry['name'], 'foo')
        table_server.add_sdtp_table(entry)
        # test bad column
        with pytest.raises(AssertionError) as err:
            table_server.get_all_values(entry['name'], None)
            # 'foo' is a name that we never use as a column name
        with pytest.raises(ColumnNotFoundException) as err:
            table_server.get_all_values(entry['name'], 'foo')
        # for each good table, good column pair get_all_values should match table.all_values
        table = entry['table']
        for column in table.schema:
            assert(table_server.get_all_values(entry['name'], column['name']) == table.all_values(column['name']))
        

def test_get_range_spec():
    table_server = TableServer()
    # Test getting tables, including all corner cases
    # Table -- None and bad key
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_range_spec(None, 'foo')
    with pytest.raises(TableNotFoundException) as err:
        table_server.get_range_spec('foo', 'foo')
    for entry in test_tables:
        with pytest.raises(TableNotFoundException) as err:
            table_server.get_range_spec(entry['name'], 'foo')
        table_server.add_sdtp_table(entry)
        # test bad column
        with pytest.raises(AssertionError) as err:
            table_server.get_range_spec(entry['name'], None)
            # 'foo' is a name that we never use as a column name
        with pytest.raises(ColumnNotFoundException) as err:
            table_server.get_range_spec(entry['name'], 'foo')
        # for each good table, good column pair get_range_spec should match table.range_sapec
        table = entry['table']
        for column in table.schema:
            assert(table_server.get_range_spec(entry['name'], column['name']) == table.range_spec(column['name']))
        