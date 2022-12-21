import sys
import time
from configparser import ConfigParser
import psycopg2
from parameters import ITERATIONS, DBMS
from output_tui import format_result, write_time, write_explain_analyse, write_results
from queries_dubio import DUBIO_QUERIES_DICT
from queries_maybms import MAYBMS_QUERIES_DICT

conn_pg = None


# This part is copied and adapted from https://github.com/utwente-dmb/wdc_pdb

def config(configname='database.ini', section='postgresql'):
    parser = ConfigParser()  # create a parser
    parser.read(configname)  # read config file

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, configname))

    return db


def connect_pg(configname='database.ini'):
    # Connect to the PostgreSQL database server
    try:
        # read connection parameters
        params = config(configname=configname)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        global conn_pg
        conn_pg = psycopg2.connect(**params)

        # create a cursor
        cur = conn_pg.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)
        exit()  # pretty fatal


def close_pg():
    # Close connection to the PostgreSQL database server
    global conn_pg
    try:
        if conn_pg is not None:
            conn_pg.close()
            print('\nDatabase connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)


def run_query(query, cur):
    cur.execute(query)


def execute_query(query_name):
    if DBMS == 'MayBMS':
        query_dict = MAYBMS_QUERIES_DICT
    elif DBMS == 'DuBio':
        query_dict = DUBIO_QUERIES_DICT
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    query = query_dict[query_name]
    global conn_pg
    try:
        cur = conn_pg.cursor()
        run_query(query, cur)  # to create a hot run and get a query output.
        if query_name.__contains__('_view'):
            inner_query = query.partition('AS')[2]
            run_query(inner_query, cur)
            result = format_result(cur)
            write_results(result, query)
        else:  # The query is just a basic query that returns a result.
            result = format_result(cur)
            write_results(result, query_name)

        explain_analyse(query, cur)  # to obtain the average runtime.
        cur.close()
        conn_pg.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error from execute_query():', error)


def explain_analyse(query, cur):
    query = "EXPLAIN ANALYSE" + query
    planning_times = []
    execution_times = []
    result = ''
    for _ in range(ITERATIONS):
        run_query(query, cur)
        result = cur.fetchall()
        planning_times.append(float(result[2][0][15:20]))
        execution_times.append(float(result[3][0][16:21]))

    average_planning = round(sum(planning_times) / len(planning_times), 3)
    average_execution = round(sum(execution_times) / len(execution_times), 3)

    write_time(average_planning, average_execution)
    write_explain_analyse(cur, result[0:2])
