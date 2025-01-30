import secrets
import jwt
import time
import os
import dotenv
from datetime import timedelta, datetime, timezone


class JwtHelper:
    def __init__(self):
        dotenv.load_dotenv()
        self.secret = os.getenv("secret")
        self.algorithm = os.getenv("algorithm")

    def generate_jwt(self, user_id: int) -> jwt:
        payload: dict = {
            "user_id": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=2)
        }

        return jwt.encode(payload, self.secret, self.algorithm)

    def decode_jwt(self, token: jwt) -> bool:
        try:
            token = jwt.decode(token, self.secret, self.algorithm)
            if token["user_id"]:
                return True
        except:
            return False