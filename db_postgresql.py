import psycopg2
import logging
from datetime import datetime


class PostgreSQL:
    attempt_count = 0
    error_count = 0
    max_attempts = 3

    def __init__(self, database='', user='', password='',
                 host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port)
        self.cur = self.conn.cursor()
        self.preparation()

    def preparation(self):
        self.check()

    def check(self):
        logging.info(f'PostgreSQL preparation\t[{datetime.now()}]')
        if self.attempt_count > self.max_attempts:
            PostgreSQL.error_count += 1
            logging.error(f'Redis is not available, num errors {self.error_count}\t[{datetime.now()}]')
            PostgreSQL.attempt_count = 0
        else:
            try:
                # self.cur.execute(qr.create_tbl_users.substitute(tbl_name='Users1'))
                # self.cur.execute(qr.create_tbl_products.substitute(tbl_name='Products1'))
                # self.conn.commit()
                self.cur.execute('create table TempTable0123456789()')
                self.cur.execute('drop table TempTable0123456789')
                logging.info(f'PostgreSQL is ready\t[{datetime.now()}]')
                return True
            except Exception as e:
                logging.error(e)
                self.conn.close()
                self.attempt_count += 1
                logging.info(f'Reconnecting attempt number {self.attempt_count}\t[{datetime.now()}]')
                self.check()

    def exec_query(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            if self.cur.description:
                return self.cur.fetchall()
        except Exception as e:
            logging.error(e)
            self.check()


class ps_conn:

    def __init__(self, database, user, password,
                 host='localhost', port='5432'):
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
