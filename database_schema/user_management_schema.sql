-- database_schema/user_management_schema.sql

-- Create User Table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add Indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Add Constraints
ALTER TABLE users
ADD CONSTRAINT unique_username UNIQUE (username);

ALTER TABLE users
ADD CONSTRAINT unique_email UNIQUE (email);
