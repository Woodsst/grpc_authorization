import datetime
import time

import psycopg

from server.config import Settings


class Orm:
    def __init__(self, config: Settings):
        self.config = config
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        timeout = 0.1
        connect = False
        while not connect:
            time.sleep(timeout)
            try:
                conn = psycopg.connect(dbname=self.config.db_name,
                                       user=self.config.db_username,
                                       password=self.config.db_password,
                                       host=self.config.db_host,
                                       port=self.config.db_port)
            except psycopg.OperationalError:
                timeout += 0.1
                if timeout > 0.5:
                    raise psycopg.OperationalError('connection with database failed')
                continue
            connect = True
        # conn = psycopg.connect(dbname=self.config.db_name,
        #                        user=self.config.db_username,
        #                        host=self.config.db_host,
        #                        port=self.config.db_port,
        #                        password=self.config.db_password)
        return conn

    def add_client(self, user_name: str, user_passwd: str) -> bool:
        try:
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
        except psycopg.errors.UniqueViolation:
            return False
        return True

    def get_client(self, user_name: str, passwd: str) -> bool:
        self.cursor.execute("""
        SELECT username, passwd 
        FROM clients 
        WHERE username=%(user_name)s and passwd=%(passwd)s;
        """, {
            "user_name": user_name,
            "passwd": passwd
        }
                            )
        return self.cursor.fetchone()
