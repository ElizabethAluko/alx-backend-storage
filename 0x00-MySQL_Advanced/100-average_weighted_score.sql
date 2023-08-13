-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_weighted_score DECIMAL(10, 2);

    -- Calculate the average weighted score for the user
    SELECT SUM(score * weight) / SUM(weight) INTO avg_weighted_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average weighted score in the users table
    UPDATE users
    SET average_weighted_score = avg_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
