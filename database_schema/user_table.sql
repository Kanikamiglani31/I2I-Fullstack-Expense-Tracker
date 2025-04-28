-- File: database_schema/user_table.sql

-- Function: create_user_table
-- Description: This function will create a SQL script to define the user table. The user table will store user-related information.

CREATE TABLE IF NOT EXISTS user_table (
    user_id SERIAL PRIMARY KEY,     -- Primary key: unique identifier for each user, automatically incremented
    username VARCHAR(50) NOT NULL,  -- Username: required, up to 50 characters
    password VARCHAR(255) NOT NULL, -- Password: required, stored as a hash
    email VARCHAR(255) NOT NULL,    -- Email: required, up to 255 characters
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Created timestamp: defaults to current time
);

-- Note: This script assumes the use of a PostgreSQL database.
-- Note: Ensure to apply security measures for password storage, such as hashing before storing.
