from server.orm import Orm
from base64 import b64encode


class Registration:
    def __init__(self, user_name: str, user_passwd: str, orm: Orm):
        self.user_name = user_name
        self.user_passwd = b64encode(user_passwd.encode()).decode()
        self.orm = orm

    def registration(self):
        if self.orm.add_client(self.user_name, self.user_passwd):
            return True
        return False
