-- database_schema/constraint_table.sql

-- Function: add_constraints
-- Description: This function will create a SQL script to define database constraints on the user table. 
-- The constraints include the primary key constraint on user_id, unique constraints on username and email 
-- to ensure no duplication, and foreign key constraints if there are relationships with any other tables.

-- Create user table with constraints
CREATE TABLE IF NOT EXISTS user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Adding constraints 
    CONSTRAINT unique_username UNIQUE (username),
    CONSTRAINT unique_email UNIQUE (email)

    -- Future foreign key constraint example
    -- CONSTRAINT fk_example FOREIGN KEY (example_id) REFERENCES another_table (example_id)
);

-- Note: 
-- 1. SERIAL data type is used for auto-incrementing the user_id.
-- 2. UNIQUE constraints are added on username and email columns.
-- 3. Uncomment and modify the foreign key constraint according to relationships with other tables.
