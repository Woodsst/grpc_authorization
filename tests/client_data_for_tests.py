import jwt
from config import Settings

USER = 'test_user'
PASSWD = 'passwd'


def jwt_encoder(username: str) -> bytes:
    key = Settings()
    key = key.secret_key
    _token = jwt.encode({"user": username}, key, algorithm="HS256")
    return _token


TOKEN = jwt_encoder(USER)
