# imports

import urllib3

from authentication.akeyless_api import set_credentials_to_keyring
from models.google_api import upload_files_to_drive
from models.os_functions import get_number_of_files_in_dir, get_files_names, pickle_in, pickle_out, \
    remove_unnecessary_files
from models.workbooks import get_unmodified_workbooks_above_x_weeks, remove_extract_schedulers, download_workbooks, \
    get_workbooks_to_archive, delete_workbooks_from_server


# ----------------------------------------------------------------------------------------------------------------------
# step 1 - getting unmodified workbooks and remove schedulers
def step_1(x_weeks_ago):
    print('starting step 1 - getting unmodified workbooks and remove schedulers')
    # get the unmodified workbooks from dev server that exceeded x weeks
    unmodified_workbooks = get_unmodified_workbooks_above_x_weeks(x_weeks_ago)
    if len(unmodified_workbooks) != 0:
        # remove extract schedulers for those workbooks
        remove_extract_schedulers(unmodified_workbooks)
    print("step 1 finished")


# ----------------------------------------------------------------------------------------------------------------------
# step 2 - getting and downloading unmodified workbooks for week after
def step_2(x_weeks_ago):
    print('starting step 2 - getting and downloading unmodified workbooks for week after')
    archived_workbooks = get_workbooks_to_archive(x_weeks_ago + 1)
    if len(archived_workbooks) != 0:
        # download workbooks
        download_workbooks(archived_workbooks)
        # check if all files were downloaded
        if get_number_of_files_in_dir('storage') == len(archived_workbooks):
            print("step 2 finished")
            return True
    print("step 2 finished")
    return False


# ----------------------------------------------------------------------------------------------------------------------
# step 3 - archive workbooks to google drive
def step_3():
    files_names = get_files_names('storage')
    upload_files_to_drive(files_names)
    print("step 3 finished")


# ----------------------------------------------------------------------------------------------------------------------
def step_4():
    archived_workbooks = pickle_out('unmodified_workbooks')
    delete_workbooks_from_server(archived_workbooks)
    print("step 4 finished")


# ----------------------------------------------------------------------------------------------------------------------
# the main process for dev server cleanup process
def main():
    x_weeks_ago = 3
    urllib3.disable_warnings()
    # connect to akeyless to get passwords
    set_credentials_to_keyring()
    print("credentials set")
    # step 1 - getting unmodified workbooks and remove schedulers
    step_1(x_weeks_ago)
    # step 2 - getting and downloading unmodified workbooks for week after
    if step_2(x_weeks_ago):
        # archive workbooks to google drive
        step_3()
        # delete workbook and notify the user
        step_4()
        remove_unnecessary_files('storage')
    else:
        print("there was no workbook to download and archive")
    print("program ends")
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
