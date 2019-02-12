DROP VIEW IF EXISTS LeadAuthorManuscripts;
DROP VIEW IF EXISTS AnyAuthorManuscripts;
DROP VIEW IF EXISTS PublishedIssues;
DROP VIEW IF EXISTS ReviewQueue;
DROP VIEW IF EXISTS WhatsLeft;
DROP VIEW IF EXISTS ReviewStatus;


CREATE VIEW LeadAuthorManuscripts AS
    SELECT lname, author_id, manuscript_id FROM Author
        JOIN Authorship
            ON Authorship.author_id = Author.id
    	JOIN Manuscript
    		ON Authorship.manuscript_id = Manuscript.id
	WHERE Authorship.author_order = 1
	ORDER BY lname, author_id, status_last_updated;

CREATE VIEW AnyAuthorManuscripts AS
    SELECT Concat(fname," ", lname) AS name, author_id, title FROM Author
		JOIN Authorship
			ON Authorship.author_id = Author.id
		JOIN Manuscript
			ON Authorship.manuscript_id = Manuscript.id
	ORDER BY lname, status_last_updated;

CREATE VIEW PublishedIssues AS
    SELECT title, pages FROM Journal
    	JOIN Accepted
    		ON Journal.journal_id = Accepted.journal_id
    	JOIN Manuscript
    		ON Accepted.manuscript_id = Manuscript.id
	WHERE published_date IS NOT NULL
	ORDER BY journal_year, journal_num, start_page;

CREATE VIEW ReviewQueue AS
    SELECT Concat(fname, " ", lname) AS primary_author_name,
           author_id,
           Manuscript.id,
		   GROUP_CONCAT((
		       SELECT Concat(fname," ", lname) AS reviewer_name
		       FROM Reviewer
		       		JOIN Feedback
		       			ON Feedback.reviewer_id = Reviewer.id
		       		JOIN Manuscript
		       			ON Manuscript.id = Feedback.manuscript_id
			   WHERE Manuscript.id = Authorship.manuscript_id GROUP BY manuscript_id) SEPARATOR ',') AS reviewer_names
    FROM Manuscript
    	JOIN Authorship
        	ON Manuscript.id = Authorship.manuscript_id
    	JOIN Author
        	ON Authorship.author_id = Author.id
	WHERE man_status = 'under review'
		AND author_order = 1
	ORDER BY status_last_updated;

CREATE VIEW WhatsLeft AS
    SELECT id, man_status, status_last_updated FROM Manuscript;
    
DROP FUNCTION IF EXISTS ViewRevId;
DELIMITER $$
CREATE FUNCTION ViewRevId() RETURNS INT
	BEGIN
		RETURN @rev_id;
	END$$
DELIMITER ;

SET @rev_id = 4;

CREATE VIEW ReviewStatus AS
    SELECT assigned_at,
           manuscript_id,
           Manuscript.title,
           A_score,
           C_score,
           M_score,
           E_score,
           recommendation
    FROM Reviewer
		JOIN Feedback
			ON Feedback.reviewer_id = Reviewer.id
		JOIN Manuscript
			ON Manuscript.id = Feedback.manuscript_id
    WHERE reviewer_id = ViewRevId()
	ORDER BY recommendation_date;

SELECT * FROM ReviewQueue;
SELECT * FROM ReviewStatus;
