import bcrypt


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        if password is None:
            return ""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        if password is None or hashed is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def clean_text(value: str) -> str:
        if value is None:
            return ""
        return value.strip()
