#!/usr/bin/python
import requests
import os


def get_climate():
    key = os.getenv('CLIMATE_KEY')
    base_url = "http://api.weatherapi.com/v1/current.json?key="
    notification_api = "http://0.0.0.0:8000/notification"
    winery_api = "https://smartvit-winery-dev.herokuapp.com/winery"

    wineries = requests.get(winery_api)

    if wineries.status_code in [404, 500]:
        return

    for winery in wineries.json():
        if 'system' in winery.keys():
            if isinstance(winery['system'], list):
                system = winery['system'][0]
                url = (
                    base_url +
                    key +
                    "&q=" +
                    system['latitude'] +
                    "," +
                    system['longitude']
                )
                response = requests.get(url)

                if response.status_code in [404, 500]:
                    continue

                climate = response.json()

                if climate['current']['wind_kph'] > 45:
                    data = dict()
                    data['type'] = 'climate'
                    data['title'] = 'Vento forte'
                    data['winery'] = winery['_id']['$oid']
                    data['message'] = 'Cuidado com o clima'

                    requests.post(notification_api, json=data)
                elif climate['current']['humidity'] < 25:
                    data = dict()
                    data['type'] = 'climate'
                    data['title'] = 'Baixa umidade'
                    data['winery'] = winery['_id']['$oid']
                    data['message'] = 'Cuidado com o clima'

                    requests.post(notification_api, json=data)
                elif climate['current']['precip_mm'] > 25:
                    data = dict()
                    data['type'] = 'climate'
                    data['title'] = 'Chuva forte'
                    data['winery'] = winery['_id']['$oid']
                    data['message'] = 'Cuidado com o clima'

                    requests.post(notification_api, json=data)


get_climate()
