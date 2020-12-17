import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch


load_dotenv()


class es_conn:

    def __init__(self, cloud_id=os.getenv('ES_ID'), password=os.getenv('ES_PASSWORD')):
        self.conn = None
        self.cloud_id = cloud_id
        self.password = password

    def __enter__(self):
        self.conn = Elasticsearch(cloud_id=self.cloud_id, http_auth=("elastic", self.password))
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
