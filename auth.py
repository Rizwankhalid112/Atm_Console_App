import hashlib

class Auth:
    @staticmethod
    def hash_password(password):
        """Converts plain text password to a SHA-256 hash."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validate_login(username, provided_password, stored_accounts):
        """Verifies if the hashed input matches the stored hash."""
        if username in stored_accounts:
            if stored_accounts[username]['password'] == Auth.hash_password(provided_password):
                return True, stored_accounts[username].get('role')
        return False, None