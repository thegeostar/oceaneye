import mysql.connector  # MySQL driver
from werkzeug.security import generate_password_hash, check_password_hash  # Werkzeug password hashing

class UserDatabase:
    def __init__(self, host, user, password, database):
        # open the database connection
        self.db = mysql.connector.connect(
            host=host,            # database host
            user=user,            # database user
            passwd=password,      # database password
            database=database     # database name
        )
        self.cursor = self.db.cursor()  # cursor for queries

    def register_user(self, username, password):
        """register a new user"""
        hashed_password = generate_password_hash(password)  # hash the password
        try:
            # insert the new user
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)", 
                (username, hashed_password)
            )
            self.db.commit()  # commit
            return True
        except mysql.connector.Error as err:
            # report SQL errors
            print("Error: ", err)
            return False

    def check_user(self, username, password):
        """check a login"""
        # look up the stored hash
        self.cursor.execute(
            "SELECT password FROM users WHERE username = %s", 
            (username,)
        )
        result = self.cursor.fetchone()  # fetch the row
        # does the password match?
        if result and check_password_hash(result[0], password):
            return True
        return False

    def reset_password(self, username, new_password):
        """reset a password"""
        hashed_password = generate_password_hash(new_password)  # hash the new password
        try:
            # store it
            self.cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (hashed_password, username)
            )
            self.db.commit()  # commit
            return True
        except mysql.connector.Error as err:
            # report SQL errors
            print("Error: ", err)
            return False