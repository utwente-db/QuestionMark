import sys

from connect_db import execute_query, connect_pg, close_pg, execute_preparation
from parameters import DBMS
from queries_dubio_prepare import DUBIO_PREPARE_DICT
from queries_maybms_prepare import MAYBMS_PREPARE_DICT


def test_connection():
    connect_pg(configname='database.ini')
    execute_query('test_1')
    print('\nIf no error is shown, the connection is working! :)')
    close_pg()


def prepare_benchmark():
    connect_pg(configname='database.ini')

    if DBMS == 'DuBio':
        query_dict = DUBIO_PREPARE_DICT
    elif DBMS == 'MayBMS':
        query_dict = MAYBMS_PREPARE_DICT
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    count = 0
    for query_name, query in query_dict.items():
        execute_preparation(query)
        count += 1
        print(str(count) + " out of " + str(len(query_dict)) + " queries done.")

    close_pg()

