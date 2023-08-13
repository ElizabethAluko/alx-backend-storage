-- creates an index idx_name_first on the table names and the first letter of name.

-- Add a new column to store the first letter of the name
ALTER TABLE names
ADD COLUMN first_letter CHAR(1);

-- Update the new column with the first letter of the name
UPDATE names
SET first_letter = LEFT(name, 1);

-- Create an index on the first letter column
CREATE INDEX idx_name_first ON names (first_letter);
