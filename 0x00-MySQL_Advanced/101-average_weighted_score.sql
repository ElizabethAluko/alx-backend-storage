-- Creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    
    -- Declare a cursor to iterate through user IDs
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    
    -- Variables to store user's average weighted score
    DECLARE avg_weighted_score DECIMAL(10, 2);
    
    -- Open the cursor
    OPEN user_cursor;
    
    -- Loop through users and calculate average weighted score
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF user_id IS NULL THEN
            LEAVE user_loop;
        END IF;
        
        -- Calculate the average weighted score for the user
        SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO avg_weighted_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
        
        -- Update the user's average weighted score in the users table
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP user_loop;
    
    -- Close the cursor
    CLOSE user_cursor;
    
END //

DELIMITER ;
