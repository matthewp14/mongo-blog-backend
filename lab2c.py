"""
Matthew Parker and Sungil Ahn
lab2c.py
Lab 2 python connector. Front end application
"""

import mysql.connector
import sys

SERVER = "sunapee.cs.dartmouth.edu"
USERNAME = "mattp"
PASSWORD = "h8d8S0SQ"
DATABASE = "mattp_db"
QUERY = "SELECT * FROM Editor"

CURRENT_USER = ""

#dictionary configuration for database connection
config = {
  'user': USERNAME,
  'password': PASSWORD,
  'host': SERVER,
  'database' : DATABASE,
  'raise_on_warnings': True
}



def start():
    initial = " "
    
    try:
        con = mysql.connector.connect(**config)
        cursor = con.cursor()
        
        print("Connected to DB")
    
        while initial[-1] != "quit":
            initial = parse_input()
        
    #        call register function if registering new user
            if initial[0] == "register":
                register(initial, cursor)
            elif initial[0] =="login":
                login(initial[1], cursor)
                
                
        #close the connection to the DB
        con.close()
        print("Closed connection")

    except mysql.connector.Error as err:
       print(err)
       
    
#get stdin   
def parse_input():
    print("Welcome! To register a new user please type 'register user_type name etc' (type quit to leave the program):" )
    lines = sys.stdin.readline()
    lines = lines[:-1]
    
    words = list(lines.split(" "))
        
    return words

#register a new user in the DB
def register(input_message,cursor):
    #change the table to uppercase
    values = []
    pre_table = input_message[1].upper()
    
    values.append(pre_table[0]+input_message[1][1:].lower())
    
    CURRENT_USER = pre_table[0]+input_message[1][1:].lower()
    
    
    #parse out all other entries
    for x in range(2, len(input_message)):
        values.append(input_message[x])
        
    
    #add quotes where necessary
    if pre_table == "EDITOR": 
        indices = [1,2]
        values = add_quotes(values, indices)
    elif pre_table == "AUTHOR":
        indices = [1,2,3]
        values = add_quotes(values, indices)
    elif pre_table == "REVIEWER":
        indices = [1,2]
        values = add_quotes(values,indices)
    
    
        
    db_insert(values,cursor)
     
#insert into the database
"""
values is a list of values to be inserted
values[0] is the table name correctly formatted

"""
def db_insert(values,cursor):
    
    if values[0] == "Editor":
        att_list = " (fname,lname)"
    elif values[0] == "Author":
        att_list = " (fname,lname,email,organization_id)"
    
    
    REGISTER_QUERY = "INSERT INTO " + values[0]+ att_list+ " VALUES "
    
    
    """
    TODO: This does not work because the values in the field list need to be surrounded
    by physical quotation marks ie ("matt", "parker"). Need to fix tomorrow
    """
    value_string = "(" + values[1]
    
    for x in range(2,len(values)-1):  
        value_string = value_string + "," + values[x] 
    
    if values[-1] != "":
        value_string = value_string + "," + values[-1] +  ")"
    else:
        value_string = value_string + ")"
        
    REGISTER_QUERY = REGISTER_QUERY + value_string
    print(REGISTER_QUERY)
    print("Registering new user")
    cursor.execute(REGISTER_QUERY)
    

def add_quotes(values, indices):
    for num in indices: 
        values[num] = "\"" + values[num] + "\""
    
    return values
    
 
""" 
TODO: should handle the login process 
"""
def login(id,con):
    pass


if __name__ == '__main__':
    start()