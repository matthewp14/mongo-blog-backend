from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error, errorcode
import sys

"""read configuration file"""
def config(filename = 'Team32Lab2.ini', section = 'mysql'):
	parser = ConfigParser()
	parser.read(filename)
	
	credentials = {}
	if parser.has_section(section):
		for item in parser.items(section):
			credentials[item[0]] = item[1]
	else:
		raise Exception(f'section {section} not found in ${filename}!')
	
	return credentials

"""connect to the database"""
def connect(credentials):
	try:
		conn = MySQLConnection(**credentials)
		if conn.is_connected():
			return conn, conn.cursor()
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

"""we're assuming you ran all of the .sql files necessary"""

"""Step 1. register or login"""
def user_auth(db):
	errmsg = 'Refer to https://www.cs.dartmouth.edu/~cs61/Labs/Lab%202 for usage.'
	while True:
		command = input().split()
		if command[0] == 'register':
			if command[1] == 'author':
				"""register author <fname> <lname> <email> <affiliation>"""
				break
			elif command[1] == 'editor':
				"""register editor <fname> <lname>"""
				break
			elif command[1] == 'reviewer':
				"""register reviewer <fname> <lname> <ICode 1> <ICode 2> <ICode 3>"""
				break
			print(errmsg)
		elif command[0] == 'login':
			"""login <id>"""
			# TODO: we're supposed to figure out who the person is from their id
			print(errmsg)
		else:
			print('You must register or login first! ' + errmsg)

# cleanup
def cleanup(db, conn):
	try:
		db.close()
		conn.close()
	except:
		print('Thanks for playing wing commander!')

if __name__ == '__main__':
	credentials = config()
	conn, db = connect(credentials)
