import enum
from base64 import b64encode

from server.orm import Orm


class ClientStatus(enum.Enum):
    CLIENT_UNDEFINED = "client undefined"
    CLIENT_UNKNOWN = "client unknown"
    CLIENT_AUTHORIZATION = "client ok"


class Authorization:
    def __init__(self, user_name: str, user_passwd: str, orm: Orm) -> None:
        self.user_name = user_name
        self.passwd = b64encode(user_passwd.encode()).decode()
        self.orm = orm

    def client_authorization(self):
        check = self.orm.get_client(self.user_name, self.passwd)
        if check:
            if check[0] == self.user_name and check[1] == self.passwd:
                return ClientStatus.CLIENT_AUTHORIZATION
        return ClientStatus.CLIENT_UNKNOWN
