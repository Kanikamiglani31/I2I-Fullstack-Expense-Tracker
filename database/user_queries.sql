-- File: database/user_queries.sql

-- Function: insert_user
-- This function provides an SQL command for inserting a new user into the 'users' table.
-- Will include fields like user_id, username, password_hash, email, created_at, updated_at.
CREATE OR REPLACE FUNCTION insert_user(
    p_user_id UUID,
    p_username VARCHAR(255),
    p_password_hash VARCHAR(255),
    p_email VARCHAR(255),
    p_created_at TIMESTAMP,
    p_updated_at TIMESTAMP
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO users (user_id, username, password_hash, email, created_at, updated_at)
    VALUES (p_user_id, p_username, p_password_hash, p_email, p_created_at, p_updated_at);
END;
$$ LANGUAGE plpgsql;

-- Function: update_user
-- This function offers an SQL command to update user details in the 'users' table matching a specific user_id.
-- Fields that can be updated include username, password_hash, email, updated_at.
CREATE OR REPLACE FUNCTION update_user(
    p_user_id UUID,
    p_username VARCHAR(255),
    p_password_hash VARCHAR(255),
    p_email VARCHAR(255),
    p_updated_at TIMESTAMP
)
RETURNS VOID AS $$
BEGIN
    UPDATE users
    SET username = p_username,
        password_hash = p_password_hash,
        email = p_email,
        updated_at = p_updated_at
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Function: delete_user
-- This function offers an SQL command to delete a user from the 'users' table using a specific user_id.
CREATE OR REPLACE FUNCTION delete_user(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
    DELETE FROM users WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Function: select_user_by_id
-- This function provides an SQL command to retrieve a user's information from the 'users' table based on user_id.
CREATE OR REPLACE FUNCTION select_user_by_id(p_user_id UUID)
RETURNS TABLE (
    user_id UUID,
    username VARCHAR(255),
    password_hash VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, username, password_hash, email, created_at, updated_at
    FROM users
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Function: select_user_by_username
-- This function provides an SQL command to retrieve a user's information from the 'users' table based on username.
CREATE OR REPLACE FUNCTION select_user_by_username(p_username VARCHAR(255))
RETURNS TABLE (
    user_id UUID,
    username VARCHAR(255),
    password_hash VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, username, password_hash, email, created_at, updated_at
    FROM users
    WHERE username = p_username;
END;
$$ LANGUAGE plpgsql;
