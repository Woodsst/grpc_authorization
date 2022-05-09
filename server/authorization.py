from server.id_generator import token_generator


class Authorization:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def client_authorization(self):
        username = self.db.get_client_username(self.username)
        password = self.db.get_client_password(self.password)
        if username and password:
            token = token_generator()
            return token
        return self.authorization_error()

    def authorization_error(self):
        return 'error'
