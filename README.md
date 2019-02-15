# CS61 Lab2

## Matt Parker and Sungil Ahn

### General Information 
The main files for this database are 'tables.sql', 'insert.sql', 'views.sql', 'procedures.sql' and 'triggers.sql'. When the database goes live, the files should be run in this order to ensure that the data is entered correctly. The files indicate the function of each file. For example, 'tables.sql' creates the tables for the database while 'insert.sql' inserts all of the necessary data into the tables.

In addition to these files, there are helper files for the procedure and trigger files to ensure that they are working properly. When testing the procedures and triggers, 'proceduressetup.sql' and 'triggerssetup.sql' should be run first. These files create small tables with test-specific data. Following this, 'procedures.sql' and 'triggers.sql' should be run followed by their respective test files. There are comments within the test files that outline the expected behavior of each query or action on the database. 


#### Triggers.sql
In addition to the triggers outlined in the lab description, this file contains two triggers to automatically update the date columns in the Manuscript and Feedback tables. The reason for this is that there are a few instances where we need to keep track of the last update on these tables. 

### Configuration
You MUST copy `Team32Lab2.ini.example` into `Team32Lab2.ini` and configure it properly for the CLI to connect to mysql.
Put your own database credentials in it.

### PYTHON VERSION
This will *not* run on Python < 3.6 since the CLI uses f-strings! So please make sure your Python is version 3.6/3.7 before running this program!
