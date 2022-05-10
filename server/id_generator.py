import uuid


def token_generator() -> str:
    token = str(uuid.uuid4())
    return token
