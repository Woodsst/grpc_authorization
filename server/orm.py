import time

import psycopg
from server.logger_config import logger
from server.config import Settings


class Orm:
    """Class for connect PostgreSQL and use SQL-requests"""

    def __init__(self, config: Settings):
        self.config = config
        self.conn = self.connect()

    def connect(self) -> psycopg.Connection:
        """connecting with database"""

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
                    logger.critical('Error - connect to database host: %s, port: %s',
                                    self.config.db_host, self.config.db_port)
                    raise psycopg.OperationalError('connection with database failed')
                continue
            connect = True
        return conn

    def add_client(self, user_name: str, user_passwd: str) -> bool:
        """SQL-request for added new client"""

        with self.conn.cursor() as cur:
            if self.client_exist(cur, user_name):
                return False
            cur.execute("""
            INSERT INTO clients (username, passwd, registration_date) 
            VALUES (%(user_name)s, %(passwd)s, %(registration_date)s)
            """, {
                "user_name": user_name,
                "passwd": user_passwd,
                "registration_date": int(time.time())
            }
                                )
            self.conn.commit()
        return True

    def get_client(self, user_name: str, passwd: str) -> bool:
        """SQL-request in database for client information"""

        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT username, passwd 
            FROM clients 
            WHERE username=%(user_name)s and passwd=%(passwd)s;
            """, {
                "user_name": user_name,
                "passwd": passwd
            }
                                )
            return cur.fetchone()

    @staticmethod
    def client_exist(cur: psycopg.Cursor, username: str) -> bool:
        """SQL-request to verify the existence of a client"""

        cur.execute("""
        SELECT username
        FROM clients
        WHERE username=%s
        """, (username,))

        if cur.fetchone() is None:
            return False
        return True
