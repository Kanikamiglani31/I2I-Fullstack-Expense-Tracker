# tests/test_user_management_db.py

import unittest
import sqlite3
from datetime import datetime

class TestUserManagementDB(unittest.TestCase):

    def setUp(self):
        # Connect to the in-memory SQLite database
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def tearDown(self):
        # Close the database connection after each test
        self.connection.close()

    def create_tables(self):
        # SQL command to create tables
        create_users_table = """
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_roles_table = """
        CREATE TABLE roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        );
        """
        
        create_permissions_table = """
        CREATE TABLE permissions (
            permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            permission_name TEXT NOT NULL UNIQUE
        );
        """
        
        create_user_roles_table = """
        CREATE TABLE user_roles (
            user_id INTEGER,
            role_id INTEGER,
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (role_id) REFERENCES roles (role_id)
        );
        """
        
        create_role_permissions_table = """
        CREATE TABLE role_permissions (
            role_id INTEGER,
            permission_id INTEGER,
            PRIMARY KEY (role_id, permission_id),
            FOREIGN KEY (role_id) REFERENCES roles (role_id),
            FOREIGN KEY (permission_id) REFERENCES permissions (permission_id)
        );
        """
        
        # Execute table creation queries
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_roles_table)
        self.cursor.execute(create_permissions_table)
        self.cursor.execute(create_user_roles_table)
        self.cursor.execute(create_role_permissions_table)
        self.connection.commit()
    
    def test_create_tables(self):
        # Check tables exist
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        self.assertEqual(len(tables), 5)
        table_names = [table[0] for table in tables]
        self.assertIn('users', table_names)
        self.assertIn('roles', table_names)
        self.assertIn('permissions', table_names)
        self.assertIn('user_roles', table_names)
        self.assertIn('role_permissions', table_names)
    
    def test_insert_user(self):
        # SQL command to insert a new user
        insert_user = """
        INSERT INTO users (username, password_hash, email)
        VALUES (?, ?, ?);
        """
        
        # Insert a user
        self.cursor.execute(insert_user, ("john_doe", "hashed_password", "john@example.com"))
        self.connection.commit()
        
        # Verify the user was inserted
        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("john_doe",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "john_doe")
    
    def test_update_user(self):
        # Insert a user to update
        self.cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES ('john_doe', 'hashed_password', 'john@example.com');
        """)
        self.connection.commit()
        
        # SQL command to update user details
        update_user = """
        UPDATE users
        SET username = ?, password_hash = ?, email = ?, updated_at = ?
        WHERE user_id = ?;
        """
        
        # Update the user details
        self.cursor.execute(update_user, ("jane_doe", "new_hashed_password", "jane@example.com", datetime.now(), 1))
        self.connection.commit()
        
        # Verify the user details were updated
        self.cursor.execute("SELECT username, email FROM users WHERE user_id = 1")
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[0], "jane_doe")
        self.assertEqual(user[1], "jane@example.com")
    
    def test_delete_user(self):
        # Insert a user to delete
        self.cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES ('john_doe', 'hashed_password', 'john@example.com');
        """)
        self.connection.commit()
        
        # SQL command to delete the user
        delete_user = """
        DELETE FROM users WHERE user_id = ?;
        """
        
        # Delete the user
        self.cursor.execute(delete_user, (1,))
        self.connection.commit()
        
        # Verify the user was deleted
        self.cursor.execute("SELECT * FROM users WHERE user_id = 1")
        user = self.cursor.fetchone()
        self.assertIsNone(user)
    
    def test_select_user_by_id(self):
        # Insert a user to select
        self.cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES ('john_doe', 'hashed_password', 'john@example.com');
        """)
        self.connection.commit()
        
        # SQL command to select user by user_id
        select_user_by_id = """
        SELECT * FROM users WHERE user_id = ?;
        """
        
        # Select the user
        self.cursor.execute(select_user_by_id, (1,))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "john_doe")
    
    def test_select_user_by_username(self):
        # Insert a user to select
        self.cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES ('john_doe', 'hashed_password', 'john@example.com');
        """)
        self.connection.commit()
        
        # SQL command to select user by username
        select_user_by_username = """
        SELECT * FROM users WHERE username = ?;
        """
        
        # Select the user
        self.cursor.execute(select_user_by_username, ("john_doe",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "john_doe")

if __name__ == '__main__':
    unittest.main()
