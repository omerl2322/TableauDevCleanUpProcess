# use to handle queries form Tableau postgresql db
import logging
import sys

import keyring
import numpy as np
import psycopg2
import tableauserverclient as TSC
from models import dbname, user, port


# to get more the 100 results from Tableau
req_options = TSC.RequestOptions(pagesize=1000)
# Define the log file
logging.basicConfig(level=logging.INFO, format='%(asctime)s	:%(levelname)s: %(message)s')


# ----------------------------------------------------------------------------------------------------------------------
def get_tableau_postgresql_credentials():
    host = keyring.get_password("dev_server_cleanup_process", "tableau_dev_url")
    password = keyring.get_password("dev_server_cleanup_process", "readonly")
    return ("dbname=" + str(dbname) + " user=" + str(user) + " host=" + str(host) + " port=" + str(
        port) + " password=" + str(password))


# ----------------------------------------------------------------------------------------------------------------------
# the function gets query name and return the query content (select * ...)
def get_query_content(query_name):
    try:
        with open('files/' + query_name + '.sql') as myQuery:
            query_content = myQuery.read()
    except Exception as e:
        logging.error('get_query_content -' + query_name + ' with the following error : ' + str(e))
        logging.error('The script ends')
        # raise exception to fail the WFE job
        raise
    return query_content


# ----------------------------------------------------------------------------------------------------------------------
# The function gets query content, run it on db and get the result as array
def run_query(query_name, query_content, return_type):
    result = None
    try:
        # Connect to Tableau Server's postgreSQL database
        conn = psycopg2.connect(get_tableau_postgresql_credentials())
        # Define cursor for postgreSQL connection
        cur = conn.cursor()
        # Query statement
        cur.execute(str(query_content))
        rows_from_query = cur.fetchall()
        if return_type == 'list':
            result = [i[0] for i in rows_from_query]
            result.sort()
        else:
            # return np array
            result = np.array(rows_from_query)
    except Exception as e:
        print('run_query: ' + query_name + ' - with the following error : ' + str(e))
        sys.exit()
    return result

# ----------------------------------------------------------------------------------------------------------------------
