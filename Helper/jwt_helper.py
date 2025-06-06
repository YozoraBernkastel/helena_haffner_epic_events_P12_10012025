import jwt
import os
import dotenv
from datetime import timedelta, datetime, timezone


class JwtHelper:
    """
    Class used to gererate or to decode a JWT Token.
    """

    @staticmethod
    def __load_jwt_detail() -> tuple[str, str]:
        dotenv.load_dotenv()
        return os.getenv("secret"), os.getenv("algorithm")

    @staticmethod
    def generate_payload(user_id: int) -> dict:
        return {
            "user_id": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=2)
        }

    @staticmethod
    def generate_jwt(user_id: int) -> jwt:
        payload: dict = JwtHelper.generate_payload(user_id)
        secret, algorithm = JwtHelper.__load_jwt_detail()

        return jwt.encode(payload, secret, algorithm)

    @staticmethod
    def decode_jwt(token: jwt) -> int | None:
        try:
            secret, algorithm = JwtHelper.__load_jwt_detail()
            decoded_token = jwt.decode(token, secret, algorithm)

            return int(decoded_token["user_id"]) if decoded_token["exp"] > int(datetime.now().timestamp()) else None
        except Exception:
            return None
