import uuid


def token_generator():
    token = str(uuid.uuid4())
    return token
