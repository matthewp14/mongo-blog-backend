-- Procedure file for lab2c
-- Matt Parker and Sungil Ahn



DROP PROCEDURE IF EXISTS FinalScore;

DELIMITER $$
CREATE PROCEDURE FinalScore(IN man_id INT, OUT decision VARCHAR(15))
BEGIN
	DECLARE avg_score INT DEFAULT 0;
	SELECT AVG(A_score+E_score+M_score+C_score) INTO avg_score FROM Feedback WHERE manuscript_id = man_id;

	IF avg_score < 37 THEN 
		SELECT "rejected" INTO decision;
	ELSE 
		SELECT "accepted" INTO decision;
	END IF;
END$$

DELIMITER ;
