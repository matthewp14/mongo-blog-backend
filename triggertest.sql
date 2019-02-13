-- File to test the triggers for lab2c
-- Matt Parker and Sungil Ahn

-- Notes:
-- triggersetup.sql and triggers.sql must be run first in order for this to work correctly


-- ----------------------------- --
-- 		Testing Trigger 1 		 --
-- ----------------------------- --

-- should cause error, there are no reviewers in the system with ICode = 111
INSERT INTO Manuscript VALUES (11, "test", "body", "2018-09-10","received",111,7,30,"2018-09-10");
-- should read 'rejected'
SELECT man_status FROM Manuscript WHERE id = 11;
-- should be fine, reviewers exist with ICode 122
INSERT INTO Manuscript VALUES (12,"test2","body","2018-09-10","recieved",122,7,30,"2019-09-10");
-- should read "recieved"
SELECT man_status FROM Manuscript WHERE id = 12;


-- ----------------------------- --
-- 		Testing Trigger 2 		 --
-- ----------------------------- --

-- Reviewer 8 is the only one editing manuscript number 6 so this should cause the trigger to take action
DELETE FROM Reviewer WHERE id = 8;
SELECT man_status FROM Manuscript WHERE id = 6; -- should be "received"

-- reviewers 9, 10 also have ICode 35 (the manuscript's ICode)
DELETE FROM Reviewer WHERE id = 9;
DELETE FROM Reviewer WHERE id = 10;
SELECT man_status from Manuscript WHERE id = 6; -- should now be "rejected"


-- ----------------------------- --
-- 		Testing Trigger 3 		 --
-- ----------------------------- --

-- updating first Id to "accepted"
UPDATE Manuscript 
	SET man_status = "accepted"
	 	WHERE id = 1;
-- should read "typesetting" and have the current date
SELECT man_status, status_last_updated FROM Manuscript WHERE id = 1;

UPDATE Feedback
	SET A_score = 10
		WHERE manuscript_id = 7 and reviewer_id = 3;

-- should read 10 and have the current date
SELECT A_score, recommendation_date FROM Feedback WHERE manuscript_id = 7 AND reviewer_id = 3;




