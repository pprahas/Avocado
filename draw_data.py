import requests
import json
r = requests.get("https://foodbukka.herokuapp.com/api/v1/restaurant")

json_string = r.json()

with open('json_data.json', 'w') as outfile:
    json.dump(json_string, outfile)

