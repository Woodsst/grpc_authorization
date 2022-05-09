import datetime

from server.config import Settings
import psycopg
from psycopg import sql


class Orm:
    def __init__(self, config: Settings):
        self.config = config
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        conn = psycopg.connect(dbname=self.config.db_name,
                               user=self.config.db_username,
                               host=self.config.db_host,
                               port=self.config.db_port,
                               password=self.config.db_password)
        return conn

    def client_exist(self, user_name, user_passwd):
        pass

    def add_client_id(self, user_name, token):
        self.cursor.execute("""
        UPDATE clients 
        SET token=%(token)s
        WHERE username=%(user_name)s
        """, {
            "token": token,
            "user_name": user_name
        }
                            )
        self.conn.commit()

    def add_client(self, user_name, user_passwd):
        self.cursor.execute("""
        INSERT INTO clients (username, passwd, registration_date) 
        VALUES (%(user_name)s, %(passwd)s, %(registration_date)s)
        """, {
            "user_name": user_name,
            "passwd": user_passwd,
            "registration_date": datetime.datetime.now()
        }
                            )
        self.conn.commit()
