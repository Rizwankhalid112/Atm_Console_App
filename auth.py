import hashlib

class Auth:
    @staticmethod
    def hash_password(password):
        """Basic parsing/hashing concept for security[cite: 7]."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validate_login(username, provided_password, stored_accounts):
        """
        Check if user exists and password matches.
        Uses a dict comprehension internally to filter[cite: 5, 25].
        """
        if username in stored_accounts:
            if stored_accounts[username]['password'] == Auth.hash_password(provided_password):
                return True, stored_accounts[username]['role']
        return False, None