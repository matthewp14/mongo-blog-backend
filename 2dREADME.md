# LAB 2d Font-End Application 

## Matthew Parker and Sungil Ahn

### General File Structure 2d.py

The file is broken into the follwing segments: 

- Database connection and configuration
- General input parsing
- User-specific function support

For the configuration and connection, 'Team32Lab2.ini' is used to store the database credentials. After a connection is established, a prepared cursor is established to combat any SLQ injections on the database. 

The file then determines if the command is a 'login' or 'register' command. For 'registers', the new users are added to the User table and then any additional information is added accordingly. A request to login is handled by determining which user is accessing the database and returning the appropriate data. Subsequent queries after the login command are handled by the specific functions pertaining to the user. 

When the user has logged out of the database, the file closes all connections and then terminates.

### Assumptions
It is assumed that all of the .sql files from Lab2c have been run prior to running the front end application. 