import psycopg
from config import Settings


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

    def get_token(self):
        self.cursor.execute("""
        SELECT token FROM clients WHERE username='test_user';
        """)
        return self.cursor.fetchone()
