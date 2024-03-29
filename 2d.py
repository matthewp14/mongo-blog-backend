from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error, errorcode
from mysql.connector.cursor import MySQLCursorPrepared
import sys
from random import randint

"""
config: reads from the .ini file to generate the database
        configuration. Returns the finialized credentials for login
"""


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


"""
connect: uses the credentials passed in to establish a connection to the database
         If successful, returns a connection and prepared cursor. Generates erros and exits
         if connection fails
"""


def connect(credentials):
	"""connect to the database"""
	try:
		conn = MySQLConnection(**credentials)
		if conn.is_connected():
			conn.autocommit = True
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

"""
user_auth: parses the initial user input to determine if the command is a 
           login or register command. Any additional arguments are stored in a 
           list for later use. Errors are generated for incorrect syntax
"""


def user_register_menu(db: MySQLCursorPrepared, command):
	if command[1] == 'author':
		if len(command) != 6:
			print('usage: register author <fname> <lname> <email> <affiliation>')
			return None, None
		
		user_id = author_register(db, command[2], command[3], command[4], command[5])
		print(f'Your id is {user_id}. Write it down somewhere.')
		
		return user_id, 'author'
	elif command[1] == 'editor':
		if len(command) != 4:
			print('usage: register editor <fname> <lname>')
			return None, None
		
		user_id = editor_register(db, command[2], command[3])
		print(f'Your id is {user_id}. Write it down somewhere.')
		
		return user_id, 'editor'
	elif command[1] == 'reviewer':
		if len(command) < 5 or len(command) > 7:
			print('usage: register reviewer <fname> <lname> <ICode 1> [<ICode 2> [<ICode 3>]]')
			return None, None
		
		user_id = reviewer_register(db, command[2], command[3], command[4:])
		print(f'Your id is {user_id}. Write it down somewhere.')
		
		return user_id, 'reviewer'
	else:
		print(errmsg)
		return None, None


def user_auth(db: MySQLCursorPrepared):
	print('Login or register')
	"""Step 1. register or login"""
	user_id = 0
	while True:
		command = input().split()
		if command[0] == 'register':
			user_id, user_type = user_register_menu(db, command)
			if user_id is None:
				continue
		
		if command[0] == 'login' or user_id:
			if not user_id and len(command) != 2:
				print('usage: login <id>')
				continue
			
			user_id = user_id or command[1]
			
			db.execute('SELECT * FROM Users WHERE id = ?', [user_id])
			try:
				user_type = db.fetchone()[1]
			except:
				return print('Wrong id!')
			
			if user_type == 'author':
				user = user_get(db, user_id, 'author')
				print(f"Hello, {user[1]} {user[2]} @ {user[3]}!")
				author_status(db, user[0])
				
				return user_id, 'author'
			elif user_type == 'editor':
				user = user_get(db, user_id, 'editor')
				print(f"Hello, {user[1]} {user[2]}!")
				editor_status(db, user[0])
				
				return user_id, 'editor'
			elif user_type == 'reviewer':
				user = user_get(db, user_id, 'reviewer')
				print(f"Hello, {user[1]} {user[2]}!")
				reviewer_status(db, user[0])
				
				return user_id, 'reviewer'
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
			if len(command) < 4:
				print('usage: submit <title> <Affiliation_name> <ICode> '
				      '[<author2-fname> <author2-lname> [<author3-fname> <author3-lname> [...]]] '
				      '<filename>')
				continue
			
			author_submit(db, user_id, command[1], command[2], command[3], command[4:-1], command[-1])
		else:
			print(errmsg)


def editor_main(db: MySQLCursorPrepared, user_id):
	while True:
		command = input().split()
		if command[0] == 'status':
			if len(command) != 1:
				print('usage: status')
				continue
			
			editor_status(db, user_id)
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
			
			reviewer_review(db, 'reject', user_id,
			                command[1], command[2], command[3], command[4], command[5])
		elif command[0] == 'accept':
			if len(command) != 6:
				print('usage: accept manuscriptid a_score c_score m_score e_score')
				continue
			
			reviewer_review(db, 'accept', user_id,
			                command[1], command[2], command[3], command[4], command[5])
		else:
			print(errmsg)


# Prints the sql query results
def db_print(db: MySQLCursorPrepared):
	rows = db.fetchall()
	for row in rows:
		print(row)


"""
user_register: registers a new user into the database, returns the id of the last added user
"""


def user_register(db: MySQLCursorPrepared, user_type):
	db.execute('INSERT INTO Users (user_type) VALUES (?)', [user_type])
	db.execute('SELECT LAST_INSERT_ID()')
	
	return db.fetchone()[0]


def user_delete(db: MySQLCursorPrepared, user_id):
	db.execute('DELETE FROM Users WHERE id = ?', [user_id])


"""
Fetches and returns the user id from the User table
"""


def user_get(db: MySQLCursorPrepared, user_id, user_type):
	db.execute(f'SELECT * FROM {user_type.title()} WHERE id = ?', [user_id])
	
	return db.fetchone()


"""
Author_register: Inserts a new Author into the Author table and returns the id
"""


def author_register(db: MySQLCursorPrepared, fname, lname, email, affiliation):
	user_id = user_register(db, 'author')
	db.execute('INSERT INTO Organizations (org_name) VALUES (?)', [affiliation])
	db.execute('SELECT LAST_INSERT_ID()')
	org_id = db.fetchone()[0]
	db.execute('INSERT INTO Author VALUES (?, ?, ?, ?, ?)',
	           [user_id, fname.title(), lname.title(), email, org_id])
	
	return user_id


def coauthor_register(db: MySQLCursorPrepared, fname, lname, org_id):
	user_id = user_register(db, 'author')
	db.execute('INSERT INTO Author (id, fname, lname, organization_id) VALUES (?, ?, ?, ?)',
	           [user_id, fname.title(), lname.title(), org_id])
	
	return user_id


def author_status(db: MySQLCursorPrepared, user_id):
	"""produces a report of all the author’s manuscripts currently in the system where he/she
	is the primary author. Only the most recent status timesstamp is kept and reported."""
	db.execute('SELECT * FROM LeadAuthorManuscripts WHERE author_id = ?', [user_id])
	db_print(db)


"""
author_submit: Inserts a new manuscript into the system. Following this the function
               registers all affiliated authors with the manuscript and updates the organization
               of the primary author
"""


def author_submit(db: MySQLCursorPrepared, author_id, title, org_name, icode, coauthors, filename):
	try:
		with open(filename, 'rb') as f:
			txt = f.read()
	except:
		return print('Filename is wrong!')
	x = randint(10, 30)
	db.execute('INSERT INTO Manuscript (title, body, received_date, ICode_id, pages)'
	           'VALUES (?, ?, CURDATE(), ?,?)', [title.title(), txt, icode, x])
	db.execute('SELECT LAST_INSERT_ID()')
	man_id = db.fetchone()[0]
	
	db.execute('INSERT INTO Organizations (org_name) VALUES (?)', [org_name])
	db.execute('SELECT LAST_INSERT_ID()')
	org_id = db.fetchone()[0]
	
	# all authors get organization_id assigned - primary author
	db.execute('UPDATE Author SET organization_id = ? WHERE id = ?', [org_id, author_id])
	
	# check if authors in the system
	authors = [author_id]
	for i in range(0, len(coauthors), 2):
		db.execute('SELECT id FROM Author WHERE fname = ? AND lname = ?',
		           [coauthors[i], coauthors[i + 1]])
		result = db.fetchone()
		co_id = result[0] if result else None
		if not co_id:
			co_id = coauthor_register(db, coauthors[i], coauthors[i + 1], org_id)
		authors.append(co_id)
	
	for i in range(len(authors)):
		db.execute('INSERT INTO Authorship VALUES (?, ?, ?)', [man_id, authors[i], i + 1])


"""
editor_register: inserts a new user and then adds the user to the editor table
                 returns the user_id
"""


def editor_register(db: MySQLCursorPrepared, fname, lname):
	user_id = user_register(db, 'editor')
	db.execute('INSERT INTO Editor VALUES (?, ?, ?)',
	           [user_id, fname.title(), lname.title()])
	
	return user_id


def editor_status(db: MySQLCursorPrepared, user_id):
	"""lists all manuscripts by all authors in the system sorted by status and then manuscript #."""
	db.execute('SELECT * FROM Manuscript ORDER BY man_status, id')
	db_print(db)


"""
editor_assign: assigns the manuscript to a reviwer in the Feedback table
"""


def editor_assign(db: MySQLCursorPrepared, manuscript_id, reviewer_id):
	db.execute('INSERT INTO Feedback (manuscript_id, reviewer_id) VALUES (?, ?)',
	           [manuscript_id, reviewer_id])


"""
editor_reject: updates the manuscript status to 'rejected' in the Manuscript table
"""


def editor_reject(db: MySQLCursorPrepared, man_id):
	db.execute('UPDATE Manuscript SET man_status = "rejected" WHERE id = ?', [man_id])


"""
editor_accept: updates the manuscript status to 'accepted' only if the manuscript has at lease
               three reviews in the Feedback table
"""


def editor_accept(db: MySQLCursorPrepared, man_id):
	db.execute('SELECT COUNT(*) FROM Feedback WHERE manuscript_id = ? AND recommendation IS NOT NULL',
	           [man_id])
	if db.fetchone()[0] < 3:
		print('Manuscript MUST have at least three completed reviews!')
	else:
		db.execute('UPDATE Manuscript SET man_status = "accepted" WHERE id = ?', [man_id])


"""
editor_schedule: updates manuscript to 'sceduled' if its status is ready and the addition would not exceed 100 pages for the issue
"""


def editor_schedule(db: MySQLCursorPrepared, man_id, issue):
	db.execute('SELECT COUNT(*) FROM Journal WHERE journal_id = ?', [issue])
	if not db.fetchone()[0]:
		db.execute('INSERT INTO Journal (journal_id, journal_num, journal_year) VALUES (?, ?, ?)',
		           [issue, int(issue[:4]), int(issue[5])])
	
	db.execute('SELECT SUM(pages) FROM Manuscript JOIN Accepted on id = manuscript_id '
	           'WHERE journal_id = ?', [issue])
	total_pages = db.fetchone()[0] or 0
	
	db.execute('SELECT pages FROM Manuscript WHERE id = ?', [man_id])
	added_pages = db.fetchone()[0] or 0
	
	db.execute('SELECT man_status from Manuscript WHERE id = ?', [man_id])
	
	if db.fetchone()[0] != 'ready':
		print('The manuscripts must be ready to be published')
	elif total_pages + added_pages > 100:
		print('The page count is exceeded for this issue')
	else:
		db.execute('UPDATE Manuscript SET man_status = "scheduled" WHERE id = ?', [man_id])
		db.execute('SELECT MAX(man_order) FROM Accepted WHERE journal_id = ?', [issue])
		order = db.fetchone()[0] or 1
		db.execute('INSERT INTO Accepted VALUES (?, ?, ?, ?, CURDATE())',
		           [man_id, issue, order, total_pages + 1])

"""
editor_publish: sets all manuscripts in the issue to 'published' assuming at least one manuscript is scheduled for the issue
"""


def editor_publish(db: MySQLCursorPrepared, issue):
	db.execute('SELECT COUNT(*) FROM Accepted WHERE journal_id = ?', [issue])
	if db.fetchone()[0] < 1:
		print("The journal has no scheduled manuscripts")
	else:
		db.execute(
			'UPDATE Manuscript JOIN Accepted on id = manuscript_id SET man_status = "Published" '
			'WHERE journal_id = ?', [issue])

"""
reviewer_register: inserts a new user into the user table and then adds the user into the 
                   reviewer table. 
                   Returns the user_id
"""


def reviewer_register(db: MySQLCursorPrepared, fname, lname, icodes):
	user_id = user_register(db, 'reviewer')
	try:
		db.execute('INSERT INTO Reviewer (id, fname, lname) VALUES (?, ?, ?)',
		           [user_id, fname.title(), lname.title()])
	except Error as err:
		user_delete(db, user_id)
		return print(err.msg)
	for icode in icodes:
		db.execute('INSERT INTO Reviewer_ICode VALUES (?, ?)', [user_id, icode])
	
	return user_id


def reviewer_status(db: MySQLCursorPrepared, user_id):
	"""a listing of all the manuscripts assigned to reviewer,
	sorted by their status from under review through accepted/rejected."""
	db.execute('SELECT * FROM Feedback JOIN Manuscript ON manuscript_id = id '
	           'WHERE reviewer_id = ? ORDER BY man_status', [user_id])
	db_print(db)


"""
reviewer_review: updates the Feedback table for the reviewer with their scores and status
"""


def reviewer_review(db: MySQLCursorPrepared, status, user_id, man_id, a_score, c_score, m_score, e_score):
	db.execute('UPDATE Feedback SET A_score = ?, C_score = ?, M_score = ?, E_score = ?,'
	           'recommendation = ? WHERE manuscript_id = ? AND reviewer_id = ?',
	           [a_score, c_score, m_score, e_score, status, man_id, user_id])


"""
reviewer_resign: deletes the user from the user table 
"""


def reviewer_resign(db: MySQLCursorPrepared, user_id):
	db.execute('DELETE FROM Users WHERE id = ?', [user_id])


"""
cleanup: closes connection and cursor.
"""


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
