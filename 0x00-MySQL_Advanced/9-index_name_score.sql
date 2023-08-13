-- creates an index idx_name_first_score on the table names and the first letter of name and the score.

-- Create an index on the first letter of the name
CREATE INDEX idx_first_letter ON names (LEFT(name, 1));

-- Create an index on the score
CREATE INDEX idx_score ON names (score);
