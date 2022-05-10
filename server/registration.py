from server.orm import Orm


class Registration:
    def __init__(self, user_name: str, user_passwd: str, orm: Orm):
        self.user_name = user_name
        self.user_passwd = user_passwd
        self.orm = orm

    def registration(self):
        if self.orm.add_client(self.user_name, self.user_passwd):
            return True
        return False
