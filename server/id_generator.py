import jwt
from server.config import Settings


def token_generator(username: str, passwd: str) -> str:
    """Generator jwt token"""

    key = Settings()
    key = key.secret_key
    token = jwt.encode(
        payload={"user": username, "passwd": passwd},
        key=key,
        algorithm="HS256",
    )
    return token
