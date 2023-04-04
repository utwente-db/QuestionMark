import sys
from configparser import ConfigParser
import psycopg2
from parameters import ITERATIONS, DBMS, SHOW_QUERY_PLAN
from output_tui import format_result, write_time, write_explain_analyse, write_results, write_query
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
        print('\nConnecting to the PostgreSQL database...\n')
        global conn_pg
        conn_pg = psycopg2.connect(**params)

        # create a cursor
        cur = conn_pg.cursor()

        # execute a statement
        print('  PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print('  ' + str(db_version) + '\n')
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


def execute_preparation(query):
    global conn_pg
    try:
        cur = conn_pg.cursor()
        run_query(query, cur)
        cur.close()
        conn_pg.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error from execute_preparation():', error)


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
        write_query(query_name)
        if query_name.__contains__('_rollback') or query_name.__contains__('_view'):
            run_query("BEGIN;", cur)
        run_query(query, cur)  # to create a hot run and get a query output.
        if query_name.__contains__('_rollback') or query_name.__contains__('_view'):
            run_query("ROLLBACK;", cur)
            if query_name.__contains__('_view'):
                inner_query = query.partition('AS')[2]
                run_query(inner_query, cur)
                result = format_result(cur)
                write_results(result)
        else:  # The query is just a basic query that returns a result.
            result = format_result(cur)
            write_results(result)

        explain_analyse_each(query, cur, query_name)  # to obtain the average runtime.
        cur.close()
        # conn_pg.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print('Error from execute_query():', error)


def explain_analyse(query, cur, query_name):
    planning_times = []
    execution_times = []
    total_times = []
    result = ''
    for _ in range(ITERATIONS):
        if query_name.__contains__('_rollback') or query_name.__contains__('_view'):
            run_query("BEGIN;", cur)
        run_query(query, cur)
        result = cur.fetchall()
        if query_name.__contains__('_rollback') or query_name.__contains__('_view'):
            run_query("ROLLBACK;", cur)
        if DBMS == 'MayBMS':  # For PostgreSQL 8 it only shows the following total time.
            total_times.append(float(result[-1][0][15:20]))
        else:  # From PostgreSQL 10 onwards it displays the following two times.
            planning_times.append(float(result[-2][0][15:20]))
            execution_times.append(float(result[-1][0][16:21]))

    if DBMS == 'MayBMS':
        average_total = round(sum(total_times) / len(total_times), 3)
        write_time(None, None, average_total)
    else:
        average_planning = round(sum(planning_times) / len(planning_times), 3)
        average_execution = round(sum(execution_times) / len(execution_times), 3)
        write_time(average_planning, average_execution, None)

    if SHOW_QUERY_PLAN:
        if query_name.__contains__('_rollback'):
            run_query("BEGIN;", cur)
        run_query(query, cur)
        result = cur.fetchall()
        write_explain_analyse(cur, result[0:-2])
        if query_name.__contains__('_rollback'):
            run_query("ROLLBACK;", cur)


def explain_analyse_each(query, cur, query_name):
    # When the query is composed of multiple queries, we want to explain analyse each of them.
    query = "EXPLAIN ANALYSE" + query
    first = query[:query.find(";") + 1]
    rest = query[query.find(";") + 1:]

    explain_analyse(first, cur, query_name)
    if not rest.isspace():
        explain_analyse_each(rest, cur, query_name)

