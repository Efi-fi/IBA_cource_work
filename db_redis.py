import redis
import logging
from datetime import datetime


# r_host = 'ec2-54-155-193-34.eu-west-1.compute.amazonaws.com'
# r_user = 'h'
# r_port = '6429'
# r_password = 'p78ebbf48e5bc9718198d3bb7816301c84fa685ccc940fc3e6ab021b3b873b723'
# id_ttl = 10  # 30 min
# r = redis.Redis(host=r_host,
#                 port=r_port,
#                 password=r_password)


class AutoRedis:
    attempt_count = 0
    error_count = 0
    max_attempts = 3

    def __init__(self, host=None, port=None, password=None,
                 socket_connect_timeout=None):
        self.rd = redis.Redis(host=host,
                              port=port,
                              password=password,
                              socket_connect_timeout=socket_connect_timeout)
        logging.info(f'Redis preparation\t[{datetime.now()}]')
        self.check()

    def check(self):
        if self.attempt_count > self.max_attempts:
            self.error_count += 1
            logging.error(f'Redis is not available, num errors {self.error_count}\t[{datetime.now()}]')
            AutoRedis.attempt_count = 0
        else:
            try:
                self.rd.ping()
                logging.info(f'Redis is ready\t[{datetime.now()}]')
                self.attempt_count = 0
            except Exception as e:
                logging.error(e)
                self.attempt_count += 1
                logging.info(f'Reconnecting attempt number {self.attempt_count}\t[{datetime.now()}]')
                self.check()


class rd_conn:

    def __init__(self, host, port, password):
        self.conn = None
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = redis.Redis(
            password=self.password,
            host=self.host,
            port=self.port)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# r.setex('1', id_ttl, '=1')
# r.delete("Bahamas")
# r.flushall()
# a = r.get("Bahamas")
# b = r.get("Belarus")
# print(a)
# print(b)
# print(r.ttl('1'))
# import time
# time.sleep(5)
# print(r.ttl('1'))
# print(r.get('1'))
# time.sleep(5)
# print(r.ttl('1'))
# print(r.get('1'))
