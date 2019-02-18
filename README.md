# Database Application

## Matthew Parker and Sungil Ahn

### Database
The main files for this database are 'tables.sql', 'insert.sql', 'views.sql', 'procedures.sql' and 'triggers.sql'. When the database goes live, the files should be run in this order to ensure that the data is entered correctly. The files indicate the function of each file. For example, 'tables.sql' creates the tables for the database while 'insert.sql' inserts all of the necessary data into the tables.

In addition to these files, there are helper files for the procedure and trigger files to ensure that they are working properly. When testing the procedures and triggers, 'proceduressetup.sql' and 'triggerssetup.sql' should be run first. These files create small tables with test-specific data. Following this, 'procedures.sql' and 'triggers.sql' should be run followed by their respective test files. There are comments within the test files that outline the expected behavior of each query or action on the database. 

### File Structure 2d.py

The file is broken into the follwing segments: 

- Database connection and configuration
- General input parsing
- User-specific function support

For the configuration and connection, 'Team32Lab2.ini' is used to store the database credentials. After a connection is established, a prepared cursor is established to combat any SLQ injections on the database. 

The file then determines if the command is a 'login' or 'register' command. For 'registers', the new users are added to the User table and then any additional information is added accordingly. A request to login is handled by determining which user is accessing the database and returning the appropriate data. Subsequent queries after the login command are handled by the specific functions pertaining to the user. 

When the user has logged out of the database, the file closes all connections and then terminates.

### Usage
All .sql files must be run first in order for the front-end application to work properly. Please see 'Configuration' below for instructions on the configuration file.

run `python3 2d.py` to start the file

The user is then prompted to either login or register. Please see 
`https://www.cs.dartmouth.edu/~cs61/Labs/Lab%202/` for all details about the specific command syntax.

An example of Login and Register: 
1. `register author fname lname email affiliation`
2. `login user_id`

Once the user is logged in, they are able to call the commands pertaining to their specific role. 

An example of Reviewer commands: 

1. `reject man_id ascore cscore mscore escore`
2. `accept man_id ascore cscore mscore escore`

Please see implementation details for more specific information on usage.


### Assumptions
It is assumed that all of the .sql files from Lab2c have been run prior to running the front end application. 

After a 'register' command, the user is automatically logged into the system and given access to their respective commands.

Any 'Affiliation' category is assumed to be the name of the affiliation rather than the ID of the affiliation. 

The 'filename' in the author submit command is used to read the file into a MySQL Blob.

### Implementation Details
We changed the trigger from lab 2c to automatically update the status of manuscripts to 'ready' when they are set to 'accepted'.

The application does not support multiple user interaction. In other words, only one user is able to access the database upon the launch of the file and should another user with to register or login they must kill the file and launch it again. So if you wish to register multiple users you will have to run this file multiple times.


#### Triggers.sql
In addition to the triggers outlined in the lab description, this file contains two triggers to automatically update the date columns in the Manuscript and Feedback tables. The reason for this is that there are a few instances where we need to keep track of the last update on these tables. 

### Configuration
You MUST copy `Team32Lab2.ini.example` into `Team32Lab2.ini` and configure it properly for the CLI to connect to mysql.
Put your own database credentials in it.

### PYTHON VERSION
This will *not* run on Python < 3.6 since the CLI uses f-strings! So please make sure your Python is version 3.6/3.7 before running this program!