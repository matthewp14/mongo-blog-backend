"""
Matthew Parker and Sungil Ahn
lab2c.py
Lab 2 python connector. Front end application
"""

import mysql.connector
import sys

SERVER = "sunapee.cs.dartmouth.edu"
USERNAME = "mattp"
PASSWORD = ""
DATABASE = "mattp_db"
QUERY = "SELECT * FROM Editor"



def start():
    initial = "null"
    
    while initial[-1] != "quit":
        initial = parse_input()
    
        
#        call register function if registering new user
        if initial[0] == "register":
            register(initial)

    
#get stdinput   
def parse_input():
    print("Please enter your username and password or 'quit' to quit: " )
    lines = sys.stdin.readline()
    lines = lines[:-1]
    
    words = list(lines.split(" "))
    
    for word in words:
        print(word)
        
    return words

#register a new user in the DB
def register(input_message):
    #change the table to uppercase
    values = []
    pre_table = input_message[1].upper()
    
    values.append(pre_table[0]+input_message[1][1:])
    
    #parse out all other entries
    for x in range(2, len(input_message)):
        values.append(input_message[x])
        
    db_insert(values)

        
#insert into the database
"""
values is a list of values to be inserted
values[0] is the table name correctly formatted

"""
def db_insert(values):
    QUERY = "INSERT INTO " + values[0] + " VALUES "
    
    value_string = "(" + values[1]
    
    for x in range(2,len(values)-1):
        
        value_string = value_string + "," + values[x] 
        
    value_string = value_string + "," + values[-1] +  ")"
        
    QUERY = QUERY + value_string
    
    print(QUERY)
    
        

if __name__ == '__main__':
    start()