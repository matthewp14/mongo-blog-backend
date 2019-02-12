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
DELETE * FROM Reviewer WHERE id = 8;
-- should read 'rejected'
SELECT man_status from Manuscript WHERE id = 6;


-- ----------------------------- --
-- 		Testing Trigger 3 		 --
-- ----------------------------- --

-- updating first Id to "accepted"
UPDATE Manuscript 
	SET man_status = "accepted"
	 	WHERE id = 1;
-- should read "typesetting"
SELECT man_status FROM Manuscript WHERE id = 1;