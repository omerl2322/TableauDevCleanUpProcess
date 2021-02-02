from models import alert_schedule_message_template, alert_delete_message_template
from models.newman_api import send_email
from models.os_functions import pickle_in
from models.postgresql_utils import *
from models.tableau_api import get_token, remove_extract_scheduler, download_workbook_to_storage, delete_workbook


# ----------------------------------------------------------------------------------------------------------------------


class Workbook:

    def __init__(self, workbook_name, workbook_id, owner_email, task_id):
        self.workbook_name = workbook_name
        self.workbook_id = workbook_id
        self.owner_email = owner_email
        self.task_id = task_id

    def get_workbook_name(self):
        return self.workbook_name

    def get_workbook_id(self):
        return self.workbook_id

    def get_owner_email(self):
        return self.owner_email

    def get_task(self):
        return self.task_id


# ----------------------------------------------------------------------------------------------------------------------
def get_unmodified_workbooks_above_x_weeks(x_weeks_ago):
    unmodified_workbooks = []
    query_content = get_query_content('weeks_query')
    query_content = query_content.replace('X', str(x_weeks_ago))
    query_result = run_query('weeks_query', query_content, 'matrix')
    n = len(query_result)
    if n != 0:
        for i in range(n):
            workbook_name = query_result[i][0]
            workbook_id = query_result[i][1]
            owner_email = query_result[i][2]
            task_id = query_result[i][3]
            unmodified_workbooks.append(Workbook(workbook_name, workbook_id, owner_email, task_id))
    return unmodified_workbooks


# ----------------------------------------------------------------------------------------------------------------------
# remove extract schedulers using the tableau api
def remove_extract_schedulers(unmodified_workbooks):
    sign_in_token, site_id = get_token()
    for workbook in unmodified_workbooks:
        if workbook.get_task() is not None:
            indicator = remove_extract_scheduler(sign_in_token, site_id, workbook.get_task())
            # if indicator == true - means that the task was removed
            if indicator:
                print("task id: " + workbook.task_id + " was removed from workbook: " + workbook.workbook_name)
            else:
                print("status code is not matched - check remove_extract_scheduler function for workbook:"
                      + workbook.workbook_name)
        send_email(workbook.workbook_name, workbook.owner_email, alert_schedule_message_template)


# ----------------------------------------------------------------------------------------------------------------------
# get workbooks for deletion from the server
def get_workbooks_to_archive(y_weeks_ago):
    workbook_list = get_unmodified_workbooks_above_x_weeks(y_weeks_ago)
    pickle_in('unmodified_workbooks', workbook_list)
    return workbook_list


# ----------------------------------------------------------------------------------------------------------------------
def download_workbooks(archived_workbooks):
    for workbook in archived_workbooks:
        download_workbook_to_storage(workbook)
    print("Finishing download workbooks to storage")


# ----------------------------------------------------------------------------------------------------------------------
def delete_workbooks_from_server(archived_workbooks):
    for workbook in archived_workbooks:
        delete_workbook(workbook)
        # send the owner a note that his dashboard was archived
        send_email(workbook.workbook_name, workbook.owner_email, alert_delete_message_template)
    print("Finishing delete workbooks process from dev server")
