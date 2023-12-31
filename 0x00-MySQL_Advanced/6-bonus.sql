-- creates a stored procedure AddBonus that adds a new correction 
-- for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score DECIMAL(10, 2)
)
BEGIN
	DECLARE project_id INT;
	-- Check if the project exists
	SELECT id INTO project_id FROM projects WHERE name = project_name;

	-- If the project doesn't exist, create it
	IF project_id IS NULL THEN
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;

	-- Add the correction
	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);

	-- Update the user's total score
	UPDATE users u
	SET u.average_score = (
		SELECT AVG(c.score) FROM corrections c WHERE c.user_id = u.user_id
	)
	WHERE u.user_id = user_id;
END //

DELIMITER ;

