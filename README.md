# PUML-ERD-Generator
Generate PUML files for ER diagrams using an Excel file 

This program will take a formatted Excel workbook and generate a PlantUML file, which can then be generated into an entity-relationship diagram.

The workbook should have a separate worksheet for each table (named after the table) and a worksheet called *relationships* as the last table, which will denote the relationships between the tables.
The *relationships* table uses the following relationship notation:
|Relationship|Format|
|-----|-----|
|Zero-to-One|[0:1]|
|One-to-One|[1:1]|
|Zero-to-Many|[0:M]|
|One-to-Many|[1:M]|

If, for example, you want to create a relationship between PROFESSOR and COURSE, such that PROFESSOR ||--|{ COURSE, or PROFESSOR [1:1] -- [1:M] COURSE, you write the following in the *relationships* table:
|Left|L_Relationship|R_Relationship|Right|
|-----|-----|-----|-----|
PROFESSOR|[1:1]|[1:M]|COURSE

Table worksheets have two columns, *Attribute* and *Key*. A key can be either *PRIMARY* or *FOREIGN* (must be capitalized). ***Primary and foriegn keys should be place first before any other attribute***. *Key* also supports the keyword *REQUIRED*, which will bold an attribute. Subclasses can be denoted by placing the superclass within parentheses when naming the class e.g., **PROFESSOR (FACULTY)** indicates that *PROFESSOR* is a subclass of *FACULTY*. 

It is important that the XLSX file is correctly formatted in order for the PUML file to be successfully generated. 

A few rules:
1. Worksheet names should be named after tables and capitalized e.g. **STUDENT**.
2. The "relationships" worksheet should be placed ***last*** in the workbook and *should not* be capitalized i.e. **relationships**.
3. Each table worksheet should have the first row with an *Attribute* and *Key* cell, in that order and with that capitalization (title format).
