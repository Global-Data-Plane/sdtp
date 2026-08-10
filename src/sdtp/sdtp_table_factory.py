# BSD 3-Clause License
# Copyright (c) 2024-2025, The Regents of the University of California (Regents)
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

import inspect
from .sdtp_schema import parse_table_spec
from .sdtp_utils import InvalidDataException

class TableBuilder:
    """
    A global table builder registry. This validates incoming specification 
    payloads using Pydantic schemas and instantiates concrete SDMLTable execution 
    classes directly, completely bypassing the need for intermediate factory classes.
    """
    table_registry = {}

    @classmethod
    def build_table(cls, spec, *args, **kwargs):
        """
        Build a table from a specification dictionary.
        
        Arguments:
          spec (dict): An SDML table specification payload containing a 'type' and 'schema'.
          *args: Additional positional arguments forwarded to the table constructor.
          **kwargs: Additional keyword arguments forwarded to the table constructor.
          
        Returns:
          SDMLTable: An active instance of the requested table executor class.
          
        Raises:
          InvalidDataException: If the specification is structurally invalid or type verification fails.
        """
        if not isinstance(spec, dict):
            raise InvalidDataException(f"Table specification must be a dictionary, got {type(spec)}")
            
        if 'type' not in spec:
            raise InvalidDataException("Specification dictionary does not have a table type ('type' field missing)")

        # 1. Coordinate comprehensive structural validation using the Pydantic Master Union
        try:
            validated_spec = parse_table_spec(spec)
        except Exception as e:
            raise InvalidDataException(f"Table configuration validation failed: {str(e)}") from e

        # 2. Extract the target registration profile from the global mapping table
        table_type = validated_spec.type
        if table_type not in cls.table_registry:
            raise InvalidDataException(
                f"'{table_type}' is not a valid or registered table type. "
                f"Valid choices are: {list(cls.table_registry.keys())}"
            )

        target_record = cls.table_registry[table_type]
        executor_class = target_record['class']

        # 3. Instantiate either a legacy factory or a direct execution runner.
        if hasattr(executor_class, "build_table"):
            return executor_class.build_table(spec, *args, **kwargs)
        return executor_class(validated_spec, *args, **kwargs)

    @classmethod
    def register_table_class(cls, table_type: str, table_class, locked: bool = False):
        """
        Register a concrete SDMLTable execution class to handle a given table type token.
        Replaces the old legacy 'register_factory_class' routine.
        
        Arguments:
          table_type (str): The unique type identifier string (e.g., 'RowTable').
          table_class (Type): The concrete class definition implementing the driver.
          locked (bool): If True, prevents subsequent registrations from overwriting this class.
          
        Raises:
          InvalidDataException: If the type is already locked or the input is not a class.
        """
        if not inspect.isclass(table_class):
            raise InvalidDataException(f"Provided handler '{table_class}' is not a valid Python class definition.")
   
        if table_type in cls.table_registry:
            record = cls.table_registry[table_type]
            if record['class'] == table_class:
                return
            elif record['locked']:
                raise InvalidDataException(f"The executor class registry for '{table_type}' is locked and cannot be modified.")
                
        cls.table_registry[table_type] = {'class': table_class, 'locked': locked}

    @classmethod
    def register_factory_class(cls, table_type: str, factory_class=None, locked: bool = False):
        """
        Backward-compatible alias for older extension code that registered factory classes.
        """
        if table_type is None:
            raise TypeError("table_type must not be None")
        if not inspect.isclass(factory_class):
            raise InvalidDataException(f"Provided handler '{factory_class}' is not a valid Python class definition.")

        if table_type in cls.table_registry:
            record = cls.table_registry[table_type]
            if record["class"] == factory_class:
                return
            if record["locked"]:
                raise InvalidDataException(f"The executor class registry for '{table_type}' is locked and cannot be modified.")

        cls.table_registry[table_type] = {"class": factory_class, "locked": locked}

    @classmethod
    def get_factory(cls, table_type: str):
        """
        Backward-compatible accessor for the registered executor/factory class.
        """
        if table_type not in cls.table_registry:
            raise InvalidDataException(f"'{table_type}' is not a valid or registered table type.")
        return cls.table_registry[table_type]["class"]

    @classmethod
    def factory_class_registry(cls):
        """
        Return a copy of the current table registry mapping layout.
        """
        return cls.table_registry.copy()


class SDMLTableFactory:
    """
    Compatibility shim for the pre-Pydantic factory API.
    """

    @classmethod
    def build_table(cls, table_spec, *args, **kwargs):
        if not isinstance(table_spec, dict):
            raise InvalidDataException(f"Table specification must be a dictionary, got {type(table_spec)}")
        return parse_table_spec(table_spec)


class RowTableFactory(SDMLTableFactory):
    @classmethod
    def build_table(cls, table_spec, *args, **kwargs):
        from .sdtp_table import RowTable
        spec = super().build_table(table_spec)
        return RowTable(spec, *args, **kwargs)


class RemoteSDMLTableFactory(SDMLTableFactory):
    @classmethod
    def build_table(cls, table_spec, *args, **kwargs):
        from .sdtp_table import RemoteSDMLTable
        spec = super().build_table(table_spec)
        return RemoteSDMLTable(spec, *args, **kwargs)


class ContainerTableFactory(SDMLTableFactory):
    @classmethod
    def build_table(cls, table_spec, *args, **kwargs):
        from .sdtp_table import ContainerTable
        spec = super().build_table(table_spec)
        return ContainerTable(spec, *args, **kwargs)
