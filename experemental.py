from datetime import datetime
from time import sleep
import requests
from elasticsearch import Elasticsearch
import pprint as p


es = Elasticsearch( cloud_id="io_optim_efi:ZXUtd2VzdC0yLmF3cy5jbG91ZC5lcy5pbyQ5ZDE0YjAxMjY3NmM0ODM0Yjk3NmM2Mjk5NGU3ZjlmNCQ1NTMyOThkZTk4Y2U0OTNkYTU3Zjg3OWUyNmU0YWZiOA==",
    http_auth=("elastic", "I3XOzFDS7XdaCxfE5GQzK5HM"))

API_key = 'ba1be09c7f4757bc24349484c240f21e'
cities = ['Minsk', 'Grodno', 'Brest', 'Gomel', 'Vitebsk', 'Mogilev']
count_ids = 0
while True:
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        resp = requests.get(url).json()
        data = {
            "@datetime": resp['dt'],
            "country": "Belarus",
            "city": city,
            "temp": resp['main']['temp'],
            "humidity": resp['main']['humidity'],
            "pressure": resp['main']['pressure'],
            "wind_speed": resp['wind']['speed'],
            "wind_dir": resp['wind']['deg'],
            "desc": resp['weather'][0]['description']
        }
        #p.pprint(data)
        res = es.index(index="weather1", body=data)
        count_ids += 1
        print(str(count_ids), res['_id'])
    sleep(60)
        # p.pprint(resp.json())




# res = es.get(index="elasticsearch_cluster", id=0)
# p.pprint(res['_source'])

# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


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


import psycopg2


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



# rd = AutoRedis(host=os.getenv('RD_HOST'),
#                port=os.getenv('RD_PORT'),
#                password=os.getenv('RD_PASSWORD'),
#                socket_connect_timeout=1)
# ps = PostgreSQL(database=os.getenv('PS_NAME'),
#                 user=os.getenv('PS_USER'),
#                 password=os.getenv('PS_PASSWORD'),
#                 host=os.getenv('PS_HOST'),
#                 port=os.getenv('PS_PORT'))