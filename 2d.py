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
errmsg = 'Refer to https://www.cs.dartmouth.edu/~cs61/Labs/Lab%202 for usage.'


def user_auth(db):
	"""Step 1. register or login"""
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
				if len(command) < 5 or len(command) > 7:
					print('usage: register reviewer <fname> <lname> <ICode 1> [<ICode 2> [<ICode 3>]]')
					continue
				
				user_id = reviewer_register(db, command[2], command[3], command[4:])
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
		elif command[0] == 'resign':
			if len(command) != 1:
				print('usage: resign')
				continue
			
			user_id = input('Enter your user id: ')
			reviewer_resign(db, user_id)
			print('Thank you for your service.')
		else:
			print('You must register or login first! ' + errmsg)


def author_main(db: MySQLCursorPrepared, user_id):
	while True:
		command = input().split()
		if command[0] == 'status':
			if len(command) != 1:
				print('usage: status')
				continue
			
			author_status(db, user_id)
		elif command[0] == 'submit':
			if len(command) < 4 or len(command) > 7:
				print('usage: submit <title> <Affiliation> <ICode> <author2> <author3> <author4>'
				      ' <filename>')
				continue
			
			# TODO
		else:
			print(errmsg)


def editor_main(db: MySQLCursorPrepared, user_id):
	while True:
		command = input().split()
		if command[0] == 'status':
			if len(command) != 1:
				print('usage: status')
				continue
			
			editor_status(db)
		elif command[0] == 'assign':
			if len(command) != 3:
				print('usage: assign <manuscriptid> <reviewer_id>')
				continue
			
			editor_assign(db, command[1], command[2])
		elif command[0] == 'reject':
			if len(command) != 2:
				print('usage: reject <manuscriptid>')
				continue
			
			editor_reject(db, command[1])
		elif command[0] == 'accept':
			if len(command) != 2:
				print('usage: accept <manuscriptid>')
				continue
			
			editor_accept(db, command[1])
		elif command[0] == 'schedule':
			if len(command) != 3:
				print('usage: schedule <manuscriptid> <issue>')
				continue
			
			editor_schedule(db, command[1], command[2])
		elif command[0] == 'publish':
			if len(command) != 2:
				print('usage: publish <issue>')
				continue
			
			editor_publish(db, command[1])
		else:
			print(errmsg)


def reviewer_main(db: MySQLCursorPrepared, user_id):
	while True:
		command = input().split()
		if command[0] == 'reject':
			if len(command) != 6:
				print('usage: reject manuscriptid a_score c_score m_score e_score')
				continue
			
			reviewer_review(db, 'reject', command[1], command[2], command[3], command[4], command[5])
		elif command[0] == 'accept':
			if len(command) != 6:
				print('usage: accept manuscriptid a_score c_score m_score e_score')
				continue
			
			reviewer_review(db, 'accept', command[1], command[2], command[3], command[4], command[5])
		else:
			print(errmsg)


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


def editor_assign(db: MySQLCursorPrepared, manuscript_id, reviewer_id):
	db.execute('INSERT INTO Feedback (manuscript_id, reviewer_id) VALUES (?, ?)',
	           (manuscript_id, reviewer_id))


def editor_reject(db: MySQLCursorPrepared, man_id):
	db.excute('UPDATE Manuscript SET man_status = "rejected" WHERE id = ?', (man_id))


def editor_accept(db: MySQLCursorPrepared, man_id):
	db.execute('SELECT COUNT(*) FROM Feedback WHERE manuscript_id = ? AND recommendation IS NOT NULL',
	           (man_id))
	if db.fetchone() < 3:
		print('Manuscript MUST have at least three completed reviews!')
	else:
		db.excute('UPDATE Manuscript SET man_status = "accepted" WHERE id = ?', (man_id))


def editor_schedule(db: MySQLCursorPrepared, man_id, issue):
	pass


def editor_publish(db: MySQLCursorPrepared, issue):
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


def reviewer_review(db: MySQLCursorPrepared, status, man_id, a_score, c_score, m_score, e_score):
	db.execute('UPDATE Feedback SET A_score = ?, C_score = ?, M_score = ?, E_score = ?,'
	           'recommendation = ? WHERE manuscript_id = ?',
	           (a_score, c_score, m_score, e_score, status, man_id))


def reviewer_resign(db: MySQLCursorPrepared, user_id):
	db.execute('DELETE FROM Users WHERE id = ?', (user_id))


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
	globals()[f'{user_type}_main'](db, user_id)
	cleanup(db, conn)
