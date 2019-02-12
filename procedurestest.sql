-- test file for the procedures
-- Matt Parker and Sungil Ahn

-- should return 'accept'
CALL FinalScore(7, @finalscore);
SELECT @finalscore;

-- should return 'reject'
CALL FinalScore(4, @finalscore);
SELECT @finalscore;

-- should return 'reject'
CALL FinalScore(5, @finalscore);
SELECT @finalscore;

-- should return 'accept'
CALL FinalScore(9, @finalscore);
SELECT @finalscore;