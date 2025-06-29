import bcrypt

class PasswordUtil:
    @staticmethod
    def hash_password(password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(plain_password, hashed_password):
        # Check if the plain password matches the hashed password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
