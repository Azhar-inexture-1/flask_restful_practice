from core import bcrypt


class Hasher:

    @staticmethod
    def verify_password(hashed_password, plain_password):
        return bcrypt.check_password_hash(hashed_password, plain_password)

    @staticmethod
    def get_hashed_password(password):
        return bcrypt.generate_password_hash(password).decode('utf8')