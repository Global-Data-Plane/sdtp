# Basic Simple Data Transfer Protocol Data Structures
This directory contains the modules for the basic SDTP data structures and a Python server framework.  The SDTP structures are in the submodule sdtp, with the following two submodules:
1. sdtp_utils: this contains the constant type declarations and an exception thrown by the SDTP routines
2. sdtp_table. This module contains the basic SDTPTable structure, which is the basis for both client- and server-side SDTP operations.  I
3. sdtp_filter. This module contains  the SDTPFilter class, which when instantiated filters SDTPTables.  In addition, a utility `check_valid_spec` checks to ensure that a filter specification is valid

