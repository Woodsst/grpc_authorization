from base64 import b64encode

from server.orm import Orm


class Registration:
    """Class for the client who requested registration"""

    def __init__(self, user_name: str, user_passwd: str, orm: Orm):
        self.user_name = user_name
        self.user_passwd = b64encode(user_passwd.encode()).decode()
        self.orm = orm

    def registration(self) -> bool:
        """Request in database for registration new client"""

        if self.orm.add_client(self.user_name, self.user_passwd):
            return True
        return False

    @classmethod
    def validation(cls, username: str, passwd: str) -> bool:
        if len(username) <= 0 or len(passwd) <= 0:
            return False
        return True
