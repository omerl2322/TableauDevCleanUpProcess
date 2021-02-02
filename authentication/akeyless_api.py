import json
import sys

import keyring
import requests

from authentication import access_id, access_key, akeyless_api_url


# ----------------------------------------------------------------------------------------------------------------------
# getting the token to get secrets from Akeyless api
from models.requests_utils import request_call


def get_token():
    data = 'cmd=auth&access-id=' + access_id + '&access-key=' + access_key
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = request_call('post', akeyless_api_url, headers, data, None, False, 200)
        # response = requests.post(akeyless_api_url, headers=headers, data=data, verify=False)
        if response.status_code == 200:
            json_response = json.loads(response.text.replace('\n', ""))
            token = json_response['token']
    except requests.exceptions.RequestException as e:
        print('get_token ,with the following error : ' + str(e))
        sys.exit()
    return token


# ----------------------------------------------------------------------------------------------------------------------
# read secret from Akeyless api
def read_secret(secret_name):
    token = get_token()
    data = 'cmd=get-secret-value&name=/BI/' + secret_name + '&token=' + str(token)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(akeyless_api_url, headers=headers, data=data, verify=False)
    if r.status_code != 200:
        e = r.json()
        print(e['error'])
        sys.exit()
    else:
        json_response = json.loads(r.text.replace('\n', ""))
        res = json_response['response']
    return res[1]


# ----------------------------------------------------------------------------------------------------------------------
def set_credentials_to_keyring():
    users_list = [line.rstrip('\n') for line in open("authentication/users.txt")]
    for user in users_list:
        secret = read_secret(user)
        keyring.set_password("dev_server_cleanup_process", user, secret)


