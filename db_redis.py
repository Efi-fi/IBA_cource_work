import os
from dotenv import load_dotenv
import redis


load_dotenv()


class rd_conn:

    def __init__(self, host=os.getenv('RD_HOST'),
                 port=os.getenv('RD_PORT'),
                 password=os.getenv('RD_PASSWORD')):
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
