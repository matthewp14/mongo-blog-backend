-- Trigger file for lab2c
-- Matt Parker and Sungil Ahn



DROP TRIGGER IF EXISTS NoReviewerICode;
DROP TRIGGER IF EXISTS AcceptedUpdate;


-- Trigger to check whether or not the ICode for the Manuscript has been specified by an Author
DELIMITER $$

CREATE TRIGGER NoReviewerICode BEFORE INSERT ON Manuscript
	FOR EACH ROW
    BEGIN
		DECLARE signal_message VARCHAR(128);
        IF NEW.ICode_id NOT IN (SELECT DISTINCT ICode_id FROM Reviewer_ICode) THEN
			SET signal_message = CONCAT("No reviewers with the specified ICode: ", CAST(NEW.ICode_id AS CHAR), " currently exist. This manuscript cannot be reviewed at the moment.");
            SET NEW.man_status = "rejected";
			SIGNAL SQLSTATE '01000' SET message_text = signal_message;
		END IF;
	END$$
DELIMITER ;


-- TRIGGER 2
DELIMITER $$

CREATE TRIGGER ReviewerDied BEFORE DELETE ON Reviewer
    FOR EACH ROW
    BEGIN
        -- any manuscript in “UnderReview” state for which that reviewer was the only reviewer
        SELECT id INTO @result FROM Manuscript
        JOIN Feedback
        ON Manuscript.id = Feedback.manuscript_id
        WHERE reviewer_id = OLD.id
        AND man_status = 'under review'
        AND (SELECT COUNT(*)
        	 FROM Feedback
             WHERE manuscript_id = Manuscript.id) = 1;

        UPDATE Manuscript
            SET man_status = 'received'
        WHERE Manuscript.id IN @result;

        UPDATE Manuscript
            SET man_status = 'rejected'
        WHERE (
            SELECT COUNT(*)
            FROM Reviewer_ICode
            WHERE Reviewer_ICode.ICode_id = Manuscript.ICode_id
			) = 1;
	END $$
DELIMITER ;


-- Automatically changes man_status to "typesetting" when it is changed to "accepted" 
DELIMITER $$

CREATE TRIGGER AcceptedUpdate BEFORE UPDATE ON Manuscript
	FOR EACH ROW
    BEGIN
		IF NEW.man_status = "accepted" THEN 
			SET NEW.man_status = "typesetting";
		END IF;
	END$$
DELIMITER ;
