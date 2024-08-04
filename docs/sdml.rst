================================
The Simple Data Markup Language
================================
The Simple Data Markup Language is a language for capturing and linking tabular data.  It is designed to do for tabular data what HTML did for documents.  However, while HTML documents are primarily designed for human consumption, SDML Tables are primarily designed for machine access.

In SDML, the unit is the table.  Each SDML document describes a _single_ table. 
A table is a (potentially infinite) list of fixed-length records.  Each record is called a _row_.  An SDML table is equivalent to:
* A PANDAS Dataframe
* A SQL database table
* A specific form of CSV file where
  * The data are in the rows of the CSV file
  * The rows of the CSV file are all the same length
  * The type of the entries in any column of the CSV file are the same as all the other entries
* A single spreadsheet tab with the same restrictions as the CSV file.

==================================
Example
==================================
The following example shows the key features of SDML.  This table is taken from Florence' Nightingale's famous 1854-1855 dataset investigating the causes of death in the Crimean War
.. literalinclude:: nightingale.sdml
  :language: JSON

This file describes a table named ``nightingale`` with 11 columns and one row per month.   Each row in ``row`` section of the table has exactly 11 entries, and the type of the kth column lines up with the type of the kth row.

====================
SDML Table Types
====================
