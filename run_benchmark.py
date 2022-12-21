import sys

from queries_dubio import DUBIO_QUERIES_DICT
from queries_maybms import MAYBMS_QUERIES_DICT
from connect_db import execute_query, connect_pg, close_pg
from parameters import DBMS, QUERIES
from output_tui import create_result_file, write_results, write_query_type


def test_connection():
    if DBMS == 'MayBMS':
        execute_query(MAYBMS_QUERIES_DICT['query_test_1'])
    elif DBMS == 'DuBio':
        execute_query(DUBIO_QUERIES_DICT['query_test_1'])
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")


def run_benchmark():
    create_result_file()

    for query in QUERIES:
        write_query_type(query)
        execute_query(query)


if __name__ == '__main__':
    connect_pg(configname='database.ini')

    # test_connection()
    run_benchmark()

    close_pg()

    # debug()
