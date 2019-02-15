from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error, errorcode
from mysql.connector.cursor import MySQLCursorPrepared
import sys


def config(filename='Team32Lab2.ini', section='mysql'):
	"""read configuration file"""
	parser = ConfigParser()
	parser.read(filename)
	
	credentials = {}
	if parser.has_section(section):
		for item in parser.items(section):
			credentials[item[0]] = item[1]
	else:
		raise Exception(f'section {section} not found in ${filename}!')
	
	return credentials


def connect(credentials):
	"""connect to the database"""
	try:
		conn = MySQLConnection(**credentials)
		if conn.is_connected():
			return conn, conn.cursor(prepared=True)
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


def user_auth(db: MySQLCursorPrepared):
	"""Step 1. register or login"""
	errmsg = 'Refer to https://www.cs.dartmouth.edu/~cs61/Labs/Lab%202 for usage.'
	while True:
		command = input().split()
		if command[0] == 'register':
			user_cmd = 'INSERT INTO Users (user_type) VALUES (?)'
			
			if command[1] == 'author':
				if len(command) != 6:
					print('usage: register author <fname> <lname> <email> <affiliation>')
					continue
				
				db.execute(user_cmd, ('author'))
				user_id = db.fetchone()['id']
				
				# TODO: affiliation
				
				# insert author
				db.execute('INSERT INTO Author VALUES (?, ?, ?, ?, ?)', (user_id) + command[2:])
				
				print(f'Your id is {user_id}. Write it down somewhere.')
				return user_id, 'author'
			elif command[1] == 'editor':
				if len(command) != 4:
					print('usage: register editor <fname> <lname>')
					continue
				
				db.execute(user_cmd, ('editor'))
				user_id = db.fetchone()['id']
				
				# insert editor
				db.execute('INSERT INTO Editor VALUES (?, ?, ?)', (user_id) + command[2:])
				
				print(f'Your id is {user_id}. Write it down somewhere.')
				return user_id, 'editor'
			elif command[1] == 'reviewer':
				if len(command) != 7:
					print('usage: register reviewer <fname> <lname> <ICode 1> <ICode 2> <ICode 3>')
					continue
				
				# normalize name because it is used for unique constraint
				fname = command[2].lower()
				lname = command[3].lower()
				
				db.execute(user_cmd, ('reviewer'))
				user_id = db.fetchone()['id']
				
				# insert reviewer
				db.execute('INSERT INTO Reviewer (id, fname, lname) VALUES (?, ?, ?)', (user_id, fname, lname))
				
				# insert ICodes
				for icode in command[4:]:
					db.execute('INSERT INTO Reviewer_ICode VALUES (?, ?)', (user_id, icode))
				
				print(f'Your id is {user_id}. Write it down somewhere.')
				return user_id, 'reviewer'
			else:
				print(errmsg)
		elif command[0] == 'login':
			if len(command) != 2:
				print('usage: login <id>')
				continue
			
			db.execute('SELECT * FROM Users WHERE id = ?', (command[1]))
			user_type = db.fetchone()['user_type']
			
			if user_type == 'author':
				db.execute('SELECT * FROM Author WHERE id = ?', (command[1]))
				result = db.fetchone()
				print(f"Hello, {result['fname']} {result['lname']}! ({result['email']})")
				
				# TODO: WTF is the 'status' command?
				
				return command[1], 'author'
			elif user_type == 'editor':
				db.execute('SELECT * FROM Editor WHERE id = ?', (command[1]))
				result = db.fetchone()
				print(f"Hello, {result['fname']} {result['lname']}!")
				
				# TODO: WTF is the 'status' command?
				
				return command[1], 'editor'
			elif user_type == 'reviewer':
				db.execute('SELECT * FROM Reviewer WHERE id = ?', (command[1]))
				result = db.fetchone()
				print(f"Hello, {result['fname']} {result['lname']}!")
				
				# TODO: wtf is the 'status' command?
			
				return command[1], 'reviewer'
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
	user_id, user_type = user_auth(db)
	cleanup(db, conn)
