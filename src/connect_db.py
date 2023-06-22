# This file has a high rate of shared functions with execute_query, but to keep the cursor declaration
# local and prevent circular import this new file is created to run non-benchmark related queries with.
from configparser import ConfigParser

import psycopg2

from src.output_tui import get_raw_result

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
        global conn_pg
        conn_pg = psycopg2.connect(**params)

        # create a cursor
        cur = conn_pg.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error from connect_pg:', error)
        exit()  # pretty fatal


def close_pg(verbose=True):
    # Close connection to the PostgreSQL database server
    global conn_pg
    try:
        if conn_pg is not None:
            conn_pg.close()
            if verbose:
                print('\nDatabase connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)


def run_query(query, cur):
    cur.execute(query)


# Could be used when defining new metrics.
def run_any_query(query):
    connect_pg(configname='database.ini')
    global conn_pg
    try:
        cur = conn_pg.cursor()
        run_query(query, cur)
        result = get_raw_result(cur)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error from run_any_query(): ', error)
    close_pg()
