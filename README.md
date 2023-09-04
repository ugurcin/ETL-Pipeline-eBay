# ETL-Pipeline-for-Semi-Structured-eBay-Auction-Data

In this project we created an ETL pipeline that takes semi-structured data from eBay and transforms and loads into an SQLite database. 

"Semi-Structured Data" folder contains all eBay data in JSON files.

"design.pdf" is an entity-relationship model or schema of this data.

"parser.py" is the main python program that reads these JSON files and transforms them into structured DAT files. 

The 'Powershell commands' includes the command to execute the main program, followed by sorting and cleaning the DAT files.

"Structured Data" folder contains all DAT files.

"create.sql" is a SQL program that creates tables based on the schema we have.

"load.txt" contains SQLite commands that loads these DAT files into the newly created tables.

"Queries" folder contains basic SQL queries to check that everything runs correctly.


