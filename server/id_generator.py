import jwt
from server.config import Settings


def token_generator(username: str) -> str:
    key = Settings()
    key = key.secret_key
    token = jwt.encode(payload={"user": username}, key=key, algorithm="HS256")
    return token
