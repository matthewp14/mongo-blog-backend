from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error, errorcode
import sys

# read configuration file
filename = 'Team32Lab2.ini'
section = 'mysql'

parser = ConfigParser()
parser.read(filename)

credentials = {}
if parser.has_section(section):
	for item in parser.items(section):
		credentials[item[0]] = item[1]
else:
	raise Exception(f'section {section} not found in ${filename}!')

# connect to the database
try:
	conn = MySQLConnection(**credentials)
	if conn.is_connected():
		db = conn.cursor()
	else:
		print('mysql connection failed.')
		sys.exit(1)
except Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
		sys.exit(2)
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
		sys.exit(3)
	else:
		print(err)
		sys.exit(4)

# we're assuming you ran all of the .sql files necessary

# cleanup
try:
	db.close()
	conn.close()
except:
	print('Thanks for playing wing commander!')