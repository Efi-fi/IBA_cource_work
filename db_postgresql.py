import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()


class ps_conn:

    def __init__(self, database=os.getenv('PS_NAME'),
                 user=os.getenv('PS_USER'),
                 password=os.getenv('PS_PASSWORD'),
                 host=os.getenv('PS_HOST'),
                 port=os.getenv('PS_PORT')):
        self.conn = None
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
