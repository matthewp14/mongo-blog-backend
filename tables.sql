-- Database creation for Lab 2 CS61
-- Matt Parker, Sungil Ahn
-- no need to run ICodes.sql!

-- Drop tables if they exist
DROP TABLE IF EXISTS Manuscript; 
DROP TABLE IF EXISTS Authorship; 
DROP TABLE IF EXISTS Author; 
DROP TABLE IF EXISTS Organizations; 
DROP TABLE IF EXISTS Reviewer; 
DROP TABLE IF EXISTS Reviewer_ICode; 
DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS Editor;
DROP TABLE IF EXISTS Accepted;
DROP TABLE IF EXISTS Journal;
DROP TABLE IF EXISTS RICodes;

-- ------------------------------------
-- TABLE CREATION 
-- ------------------------------------

CREATE TABLE Manuscript (
	id INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(45) NOT NULL,
	body BLOB NOT NULL,
	received_date DATE NOT NULL,
	man_status VARCHAR(45) NOT NULL DEFAULT('received'),
	ICode_id MEDIUMINT NOT NULL REFERENCES Editor(id),
	editor_id INT NOT NULL REFERENCES RICodes(code),
	pages INT UNSIGNED NOT NULL,
	status_last_updated DATE
);

CREATE TABLE Authorship(
	manuscript_id INT NOT NULL REFERENCES Manuscript(id),
	author_id INT NOT NULL REFERENCES Author(id),
	author_order TINYINT NOT NULL,
	PRIMARY KEY (manuscript_id, author_id)
);

CREATE TABLE Author (
	id INT PRIMARY KEY AUTO_INCREMENT,
	fname VARCHAR(45) NOT NULL,
	lname VARCHAR(45) NOT NULL,
	email VARCHAR(45),
	organization_id INT REFERENCES Organizations(id)
);

CREATE TABLE Organizations (
	id INT PRIMARY KEY AUTO_INCREMENT,
	org_name VARCHAR(45) NOT NULL,
	type_org VARCHAR(45) NOT NULL
);

CREATE TABLE Reviewer (
	id INT PRIMARY KEY AUTO_INCREMENT,
	fname VARCHAR(45) NOT NULL,
	lname VARCHAR(45) NOT NULL,
	email VARCHAR(45) NOT NULL,
	organization_id INT NOT NULL REFERENCES Organizations(id)
);

CREATE TABLE Reviewer_ICode (
	reviewer_id INT NOT NULL,
	ICode_id MEDIUMINT NOT NULL REFERENCES RICodes(code),
    CONSTRAINT FOREIGN KEY (reviewer_id) REFERENCES Reviewer(id) ON DELETE CASCADE,
	PRIMARY KEY (reviewer_id, ICode_id)
);
  
CREATE TABLE Feedback (
manuscript_id INT NOT NULL REFERENCES Manuscript(id),
reviewer_id INT NOT NULL,
A_score INT UNSIGNED,
C_score INT UNSIGNED,
M_score INT UNSIGNED,
E_score INT UNSIGNED,
recommendation VARCHAR(6),
recommendation_date DATE,
assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
CONSTRAINT FOREIGN KEY (reviewer_id)  REFERENCES Reviewer(id) ON DELETE CASCADE,
PRIMARY KEY (manuscript_id, reviewer_id));

CREATE TABLE Editor (
id INT PRIMARY KEY AUTO_INCREMENT,
fname VARCHAR(45),
lname VARCHAR(45));

CREATE TABLE Accepted (
manuscript_id INT NOT NULL REFERENCES Manuscript(id),
journal_id VARCHAR(6) NOT NULL REFERENCES Journal(journal_id),
man_order INT UNSIGNED NOT NULL,
start_page INT UNSIGNED NOT NULL DEFAULT 1,
accepted_date DATE NOT NULL);

CREATE TABLE Journal (
journal_id VARCHAR(6) PRIMARY KEY,
is_full BOOLEAN NOT NULL DEFAULT false,
published_date DATE,
journal_num INT UNSIGNED NOT NULL,
journal_year INT NOT NULL);

CREATE TABLE RICodes (
	code     MEDIUMINT   NOT NULL AUTO_INCREMENT,
	interest varchar(64) NOT NULL,
	PRIMARY KEY (code)
);
