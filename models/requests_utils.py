import sys

import requests

from models.os_functions import remove_unnecessary_files


# ----------------------------------------------------------------------------------------------------------------------
# generic function to http requests
def request_call(method, url, headers, data, json, verify, status_code):
    response = None
    try:
        if method == 'delete':
            response = requests.delete(url, headers=headers, verify=verify)
        if method == 'post':
            response = requests.post(url, json=json, data=data, headers=headers, verify=verify)
        if response.status_code == status_code:
            return response
        else:
            raise requests.exceptions.RequestException("the status code does not matched")
    except requests.exceptions.RequestException as e:
        print('request call to: ' + url + ' ended with error: ' + str(e))
        print('delete content from storage')
        remove_unnecessary_files('storage')
        print('program ends')
        sys.exit()


# ----------------------------------------------------------------------------------------------------------------------

