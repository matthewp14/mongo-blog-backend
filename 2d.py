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


def user_auth(db):
	"""Step 1. register or login"""
	errmsg = 'Refer to https://www.cs.dartmouth.edu/~cs61/Labs/Lab%202 for usage.'
	while True:
		command = input().split()
		if command[0] == 'register':
			if command[1] == 'author':
				if len(command) != 6:
					print('usage: register author <fname> <lname> <email> <affiliation>')
					continue
				
				user_id = author_register(db, command[2], command[3], command[4], command[5])
				print(f'Your id is {user_id}. Write it down somewhere.')
				
				return user_id, 'author'
			elif command[1] == 'editor':
				if len(command) != 4:
					print('usage: register editor <fname> <lname>')
					continue
				
				user_id = editor_register(db, command[2], command[3])
				print(f'Your id is {user_id}. Write it down somewhere.')
				
				return user_id, 'editor'
			elif command[1] == 'reviewer':
				if len(command) != 7:
					print('usage: register reviewer <fname> <lname> <ICode 1> <ICode 2> <ICode 3>')
					continue
				
				user_id = reviewer_register(db, command[2], command[3], command[4:6])
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
				user = user_get(db, command[1], 'author')
				print(f"Hello, {user['fname']} {user['lname']} @ {user['email']}!")
				author_status(db, user['id'])
				
				return command[1], 'author'
			elif user_type == 'editor':
				user = user_get(db, command[1], 'editor')
				print(f"Hello, {user['fname']} {user['lname']}!")
				editor_status(db)
				
				return command[1], 'editor'
			elif user_type == 'reviewer':
				user = user_get(db, command[1], 'reviewer')
				print(f"Hello, {user['fname']} {user['lname']}!")
				reviewer_status(db, user['id'])
				
				return command[1], 'reviewer'
		else:
			print('You must register or login first! ' + errmsg)


def db_print(db: MySQLCursorPrepared):
	for row in db:
		print("".join(["{:<12}".format(col) for col in row]))


def user_register(db: MySQLCursorPrepared, user_type):
	db.execute('INSERT INTO Users (user_type) VALUES (?)', (user_type))
	
	return db.fetchone()['id']


def user_get(db: MySQLCursorPrepared, user_id, user_type):
	db.execute(f'SELECT * FROM {user_type.title()} WHERE id = ?', (user_id))
	
	return db.fetchone()


# TODO: need to figure out Affiliation
def author_register(db: MySQLCursorPrepared, fname, lname, email, affiliation):
	user_id = user_register(db, 'author')
	db.execute('INSERT INTO Author VALUES (?, ?, ?, ?, ?)',
	           (user_id, fname.title(), lname.title(), email, affiliation))
	
	return user_id


def author_status(db: MySQLCursorPrepared, user_id):
	"""produces a report of all the author’s manuscripts currently in the system where he/she
	is the primary author. Only the most recent status timesstamp is kept and reported."""
	db.execute('SELECT * FROM LeadAuthorManuscripts WHERE author_id = ?', (user_id))
	db_print(db)


# TODO: need to figure out Affiliation and Author4
def author_submit(db: MySQLCursorPrepared):
	pass


def editor_register(db: MySQLCursorPrepared, fname, lname):
	user_id = user_register(db, 'editor')
	db.execute('INSERT INTO Editor VALUES (?, ?, ?)',
	           (user_id, fname.title(), lname.title()))
	
	return user_id


def editor_status(db: MySQLCursorPrepared):
	"""lists all manuscripts by all authors in the system sorted by status and then manuscript #."""
	db.execute('SELECT * FROM Manuscript ORDER BY man_status, id')
	db_print(db)


def editor_assign(db: MySQLCursorPrepared):
	pass


def editor_reject(db: MySQLCursorPrepared):
	pass


def editor_accept(db: MySQLCursorPrepared):
	pass


def editor_schedule(db: MySQLCursorPrepared):
	pass


def editor_publish(db: MySQLCursorPrepared):
	pass


def reviewer_register(db: MySQLCursorPrepared, fname, lname, icodes):
	user_id = user_register(db, 'reviewer')
	db.execute('INSERT INTO Reviewer (id, fname, lname) VALUES (?, ?, ?)',
	           (user_id, fname.title(), lname.title()))
	for icode in icodes:
		db.execute('INSERT INTO Reviewer_ICode VALUES (?, ?)', (user_id, icode))
	
	return user_id


def reviewer_status(db: MySQLCursorPrepared, user_id):
	"""a listing of all the manuscripts assigned to reviewer,
	sorted by their status from under review through accepted/rejected."""


def reviewer_reject(db: MySQLCursorPrepared):
	pass


def reviewer_accept(db: MySQLCursorPrepared):
	pass


def reviewer_resign(db: MySQLCursorPrepared):
	pass


def cleanup(conn, db):
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
