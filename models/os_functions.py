import os
import pickle
import subprocess


# ----------------------------------------------------------------------------------------------------------------------
# change path
def change_dir(statement):
    print(os.getcwd())
    os.chdir(statement)
    print(os.getcwd())


# ----------------------------------------------------------------------------------------------------------------------
# run command lines
def run_command_on_commandline(command):
    try:
        output1 = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_string = output1.stdout
        stderr_string = output1.stderr
        print(output_string)
        print(stderr_string)
    except Exception as e:
        print("There was an issue tab to sql command: " + str(e))
        exit()


# ----------------------------------------------------------------------------------------------------------------------
# delete unnecessary files - twb or twbx from the workbooks_storage folder
def remove_unnecessary_files(dir_name):
    change_dir(dir_name)
    command1 = "rm *.twb"
    command2 = "rm *.twbx"
    print("delete all twb files")
    run_command_on_commandline(command1)
    print("delete all twbx files")
    run_command_on_commandline(command2)
    change_dir('..')


# ----------------------------------------------------------------------------------------------------------------------
# get the number of files in dir
def get_number_of_files_in_dir(dir_name):
    count = 0
    for path in os.listdir(dir_name):
        if os.path.isfile(os.path.join(dir_name, path)):
            count += 1
    return count


# ----------------------------------------------------------------------------------------------------------------------
def get_files_names(dir_name):
    change_dir(dir_name)
    files_names_list = os.listdir()
    change_dir('..')
    return files_names_list


# ----------------------------------------------------------------------------------------------------------------------
def pickle_in(obj_name, obj):
    with open('files/' + obj_name + '.pkl', 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)


# ----------------------------------------------------------------------------------------------------------------------
def pickle_out(obj_name):
    with open('files/' + obj_name + '.pkl', 'rb') as pickle_file:
        obj = pickle.load(pickle_file)
        return obj
