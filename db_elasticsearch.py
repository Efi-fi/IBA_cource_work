from elasticsearch import Elasticsearch

s = Elasticsearch(cloud_id="io_optim_efi:ZXUtd2VzdC0yLmF3cy5jbG91ZC5lcy5pbyQ5ZDE0YjAxMjY3NmM0ODM0Yjk3NmM2Mjk5NGU3ZjlmNCQ1NTMyOThkZTk4Y2U0OTNkYTU3Zjg3OWUyNmU0YWZiOA==",
    http_auth=("elastic", "I3XOzFDS7XdaCxfE5GQzK5HM"))


class es_conn:

    def __init__(self, cloud_id, password):
        self.conn = None
        self.cloud_id = cloud_id
        self.password = password

    def __enter__(self):
        self.conn = Elasticsearch(cloud_id=self.cloud_id, http_auth=("elastic", self.password))
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
