import bcrypt


class EncryptService:
    @staticmethod
    def hash(text_to_hash: str) -> str:
        return bcrypt.hashpw(text_to_hash.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
