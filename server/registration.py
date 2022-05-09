class Registration:
    def __init__(self, user_name, user_passwd, orm):
        self.user_name = user_name
        self.user_passwd = user_passwd
        self.orm = orm

    def registration(self):
        self.orm.add_client(self.user_name, self.user_passwd)

    def error(self):
        pass
