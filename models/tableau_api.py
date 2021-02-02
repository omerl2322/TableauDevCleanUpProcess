import json
import sys

import keyring

from models import api_version, tableau_dev_url, tableau_auth, dev_server
from models.os_functions import change_dir, remove_unnecessary_files
from models.requests_utils import request_call


# ----------------------------------------------------------------------------------------------------------------------
# get sign in token for running http requests to tableau dev server
def get_token():
    password = keyring.get_password("dev_server_cleanup_process", "tableau_read")
    payload = {"credentials": {"name": "tableau_read", "password": password, "site": {"contentUrl": ""}}}
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    url = tableau_dev_url + '/api/' + api_version + '/auth/signin'
    req = request_call('post', url, headers, None, payload, False, 200)
    response = json.loads(req.content)
    token = response["credentials"]["token"]
    site_id = response["credentials"]["site"]["id"]
    return token, site_id


# ----------------------------------------------------------------------------------------------------------------------
# remove task from workbook
# status code 204
def remove_extract_scheduler(sign_in_token, site_id, task_id):
    url = tableau_dev_url + '/api/' + api_version + '/sites/' + site_id + '/tasks/extractRefreshes/' + task_id
    headers = {'x-tableau-auth': sign_in_token}
    response = request_call('delete', url, headers, None, None, False, 204)
    print(task_id+": was removed from tableau dev server")
    return True


# ----------------------------------------------------------------------------------------------------------------------
# download workbook without extract
# status code 200
def download_workbook_to_storage(workbook):
    change_dir('storage')
    with dev_server.auth.sign_in(tableau_auth):
        try:
            response = dev_server.workbooks.download(workbook.workbook_id, no_extract=True)
            print("\nDownloaded the file {0}.".format(workbook.workbook_name))
        except Exception as e:
            print("There was an issue with download_workbooks_to_storage function : " + str(e))
            print("can not download workbook: " + workbook.workbook_name)
            print('delete content from storage')
            change_dir('..')
            remove_unnecessary_files('storage')
            print("program ends")
            sys.exit()
    print("Finishing download workbook: " + workbook.workbook_name)
    change_dir('..')


# ----------------------------------------------------------------------------------------------------------------------
# delete workbook from the dev server
# status code 204
def delete_workbook(workbook):
    with dev_server.auth.sign_in(tableau_auth):
        try:
            response = dev_server.workbooks.delete(workbook.workbook_id)
            print("\nthe workbook: {0} was deleted from tableau dev server.".format(workbook.workbook_name))
        except Exception as e:
            print("There was an issue with delete_workbook function : " + str(e))
            print("can not delete workbook: " + workbook.workbook_name)
            print('delete content from storage')
            remove_unnecessary_files('storage')
            print("program ends")
            sys.exit()
    print("Finishing delete the workbook: " + workbook.workbook_name)
    return True


