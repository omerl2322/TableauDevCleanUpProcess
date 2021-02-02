import json
import os

print(os.getcwd())
with open('files/keys.json') as json_file:
    data = json.load(json_file)
    access_id = data["access_id"]
    access_key = data["access_key"]

akeyless_api_url = 'https://vault-api.outbrain.com'
