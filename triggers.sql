-- Trigger file for lab2c
-- Matt Parker and Sungil Ahn

DROP TRIGGER IF EXISTS NoReviewerICode;
DROP TRIGGER IF EXISTS AcceptedUpdate;
DROP TRIGGER IF EXISTS ReviewerDied;
DROP TRIGGER IF EXISTS ManStatusUpdate;
DROP TRIGGER IF EXISTS FeedbackUpdate;

-- Trigger to check whether or not the ICode for the Manuscript has been specified by an Author
DELIMITER $$

CREATE TRIGGER NoReviewerICode
  BEFORE INSERT
  ON Manuscript
  FOR EACH ROW
BEGIN
  DECLARE signal_message VARCHAR(128);
  IF NEW.ICode_id NOT IN (SELECT ICode_id FROM Reviewer_ICode) THEN
    SET signal_message = CONCAT("No reviewers with the specified ICode: ", CAST(NEW.ICode_id AS CHAR),
                                " currently exist. This manuscript cannot be reviewed at the moment.");
    SET NEW.man_status = "rejected";
    SIGNAL SQLSTATE '01000' SET message_text = signal_message;
  END IF;
END$$
DELIMITER ;


-- TRIGGER 2
DELIMITER $$

CREATE TRIGGER ReviewerDied
  BEFORE DELETE
  ON Reviewer
  FOR EACH ROW
BEGIN
  UPDATE Manuscript
  SET man_status = 'received'
  WHERE id IN (
    -- any manuscript in “UnderReview” state for which that reviewer was the only reviewer
    SELECT id
    FROM Manuscript
           JOIN Feedback
                ON Manuscript.id = Feedback.manuscript_id
    WHERE reviewer_id = OLD.id
      AND man_status = 'under review'
      AND (SELECT COUNT(*)
           FROM Feedback
           WHERE manuscript_id = Manuscript.id) = 1
  );

  -- any manuscript that doesn't have any more authors for that ICode is rejected
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

CREATE TRIGGER AcceptedUpdate
  BEFORE UPDATE
  ON Manuscript
  FOR EACH ROW
BEGIN
  IF NEW.man_status = "accepted" THEN
    SET NEW.man_status = "typesetting";
  END IF;
END$$
DELIMITER ;

DELIMITER $$


-- Automatically updates the status_last_updated for the manuscript table
CREATE TRIGGER ManStatusUpdate
  BEFORE UPDATE
  ON Manuscript
  FOR EACH ROW
BEGIN
  IF OLD.man_status != NEW.man_status THEN
    SET NEW.status_last_updated = CURDATE();
  END IF;
END$$
DELIMITER ;

DELIMITER $$
-- Automatically update the recommendation_date to the current date
CREATE TRIGGER FeedbackUpdate
  BEFORE UPDATE
  ON Feedback
  FOR EACH ROW
BEGIN
  SET NEW.recommendation_date = CURDATE();
END$$
DELIMITER ;
