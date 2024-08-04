=================================
The Simple Data Transfer Protocol
=================================

Rationale and Motivation
------------------------
The Simple Data Transfer Protocol is designed to make it as easy to publish and use
a structured dataset as it is to publish and read a web page.

Simple Data Transfer Protocol Basics
------------------------------------
The basic data structure in the Simple Data Transfer Protocol is the *table*.  A Table is a fixed list of *columns* and  (potentially) infinite list of *rows*.  It is a generalization of a (simple) SQL database table, or a comma-separated values file.
It is important to note that a Table is a *semantic*, not a physical, object (though it may well have a physical realization).  A table is simply an object with:
- A fixed-size list of columns, called a *schema*.  A column is simply a pair (name, type), where type is an STDP type (see below).
- A list of rows, where each row is the length of the table's column list, and the *k*th entry in each row is of the type specified for the *k*th column.