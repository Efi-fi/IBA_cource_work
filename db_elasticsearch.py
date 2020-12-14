import requests
from elasticsearch import Elasticsearch

s = Elasticsearch( cloud_id="io_optim_efi:ZXUtd2VzdC0yLmF3cy5jbG91ZC5lcy5pbyQ5ZDE0YjAxMjY3NmM0ODM0Yjk3NmM2Mjk5NGU3ZjlmNCQ1NTMyOThkZTk4Y2U0OTNkYTU3Zjg3OWUyNmU0YWZiOA==",
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