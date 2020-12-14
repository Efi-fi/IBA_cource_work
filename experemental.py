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