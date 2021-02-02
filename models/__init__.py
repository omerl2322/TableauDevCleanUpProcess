import keyring
import tableauserverclient as TSC


# ------------------------------------------------------------------------------------------------
# get tableau dev server login data
def get_tableau_dev_server_data(tableau_dev_link):
    tableau_http_url = 'http://{}'.format(tableau_dev_link)
    return TSC.Server(tableau_http_url, use_server_version=True)


# ------------------------------------------------------------------------------------------------
def get_tableau_auth_data():
    tableau_read_credentials = keyring.get_password("dev_server_cleanup_process", "XXX")
    return TSC.TableauAuth('XXX', tableau_read_credentials, site_id='')


# ------------------------------------------------------------------------------------------------
# tableau api variables
tableau_dev = keyring.get_password("dev_server_cleanup_process", "tableau_dev_url")
api_version = '3.9'
tableau_dev_url = 'https://{}'.format(tableau_dev)
tableau_auth = get_tableau_auth_data()
dev_server = get_tableau_dev_server_data(tableau_dev)

# ------------------------------------------------------------------------------------------------
# postgresql connection details
dbname = 'workgroup'
user = 'readonly'
port = '8060'

# ------------------------------------------------------------------------------------------------
# newman api variables
send_internal_email_post_command = 'XXX'
alert_schedule_message_template = "cleaningTableauDevProcessTemplate"
alert_delete_message_template = "cleaningTableauDevProcessTemplate1"
# ------------------------------------------------------------------------------------------------
# google api variables
CLIENT_SECRET_FILE = 'files/google_drive_credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
shared_folder_id = 'XXX'
