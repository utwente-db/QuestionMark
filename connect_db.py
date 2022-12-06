import time
from configparser import ConfigParser
import psycopg2
from parameters import ITERATIONS, TIMED

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


def format_result(cur):
    result = cur.fetchall()

    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    index = 0
    for cd in cur.description:
        max_col_length = max(list(map(lambda x: len(str(x[index])), result)))
        widths.append(max(max_col_length, len(cd[0])))
        columns.append(cd[0])
        index += 1

    for w in widths:
        tavnit += " %-" + "%ss |" % (w,)
        separator += '-' * w + '--+'

    printable_output = separator + '\n' + \
                       tavnit % tuple(columns) + '\n' + \
                       separator + '\n'

    for row in result:
        printable_output += tavnit % row + '\n'
    printable_output += separator + '\n'

    return printable_output


def execute_query(query):
    global conn_pg
    runtime = ''
    try:
        cur = conn_pg.cursor()
        start_time = time.time()
        for _ in range(ITERATIONS):
            run_query(query, cur)
        end_time = time.time()
        if TIMED:
            runtime = end_time - start_time
        printable_output = format_result(cur)

        cur.close()
        conn_pg.commit()
        return runtime, printable_output
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)
