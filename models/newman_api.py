# -----------------------------------------------------------------------------------------------------
# transform the file to byte array
import json

from models import send_internal_email_post_command
# -----------------------------------------------------------------------------------------------------
# arrange json object
from models.requests_utils import request_call


def arrange_json_object(dashboard_name, email_to, template):
    data_var = {
        "emailFrom": "TableauDevServer@outbrain.com",
        "fromName": "TableauDev",
        "sender": "TableauDevScript",
        "templateName": template,
        "templateContextMapOfSingleValues": {
            "dashboard_name": dashboard_name
        },
        "emailsTo": [email_to]
    }
    data_json = json.dumps(data_var)
    return data_json


# -----------------------------------------------------------------------------------------------------
# manage email sending
# status code 200
def send_email(dashboard_name, email_to, template):
    # arrange json object
    json_data = arrange_json_object(dashboard_name, email_to, template)
    post = request_call('post', send_internal_email_post_command, None, json_data, None, None, 200)
    print("sending email to: " + str(email_to))
    print("finish sending email")


