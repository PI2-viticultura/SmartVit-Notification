#!/usr/bin/python 
import requests
import os
d = os.path.dirname(__file__) # directory of script


key = "6c28b1e2b14b47c3a34225157201110"
base_url = "http://api.weatherapi.com/v1/current.json?key="

locations = [{'lat': "-16.0062043", 'lon': "-48.0476886"}]

for location in locations:
    url = base_url + key + "&q=" + location['lat'] + "," + location['lon']
    response = requests.get(url)
    print(response.json())
