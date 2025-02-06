-- Define indexes on frequently queried columns in the user table to improve query performance.

-- Adding index on the username column
CREATE INDEX idx_username
ON user_table (username);

-- Adding index on the email column
CREATE INDEX idx_email
ON user_table (email);
