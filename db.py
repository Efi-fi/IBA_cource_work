from db_elasticsearch import es_conn
from db_postgresql import ps_conn
from db_redis import rd_conn


def es_preparation():
    with es_conn() as conn:
        pass


def ps_preparation():
    with ps_conn() as conn:
        cur = conn.cur()



def rd_preparation():
    with rd_conn() as conn:
        pass


def dbs_preparation():
    es_preparation()
    ps_preparation()
    rd_preparation()
