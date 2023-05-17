import sys

from connect_db import run_any_query, connect_pg, close_pg
from parameters import DBMS, QUERIES
from queries_dubio import DUBIO_QUERIES_DICT
from queries_maybms import MAYBMS_QUERIES_DICT
from output_tui import write_metric, write_errors

QUERIES_FAILED = 0
ERRORS = {}
SUM_RUNTIME_TOTAL = 0
SUM_RUNTIME_PLAN = 0
SUM_RUNTIME_EXEC = 0


def add_failed(error, query_name):
    global QUERIES_FAILED
    global ERRORS
    QUERIES_FAILED += 1
    ERRORS[query_name] = (str(error))


def add_runtime(total, plan, exe):
    global SUM_RUNTIME_TOTAL
    global SUM_RUNTIME_EXEC
    global SUM_RUNTIME_PLAN
    SUM_RUNTIME_TOTAL += total
    SUM_RUNTIME_EXEC += plan
    SUM_RUNTIME_PLAN += exe


def char_count():
    if DBMS == 'MayBMS':
        query_dict = MAYBMS_QUERIES_DICT
    elif DBMS == 'DuBio':
        query_dict = DUBIO_QUERIES_DICT
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    count = 0
    for query_name in QUERIES:
        query = query_dict[query_name]
        count += len(query)

    write_metric('char', count)


def error_rate():
    percentage_failed = round((QUERIES_FAILED / len(QUERIES)) * 100, 2)
    write_metric('error', 100 - percentage_failed)


def runtime():
    write_metric('runtime', [round(SUM_RUNTIME_TOTAL, 2), round(SUM_RUNTIME_PLAN, 2), round(SUM_RUNTIME_EXEC, 2)])


def prob_size():
    sizes = {}

    connect_pg()
    if DBMS == 'DuBio':
        sentence_size = "SELECT pg_size_pretty(SUM(pg_column_size(_sentence))) FROM offers;"
        dict_size = "SELECT pg_size_pretty(pg_total_relation_size('_dict'));"
        total_size = "SELECT pg_size_pretty(pg_total_relation_size('offers'));"

        size_sentence = run_any_query(sentence_size)
        sizes['_sentence column is:                     '] = size_sentence
        size_dict = run_any_query(dict_size)
        sizes['dict table is:                           '] = size_dict
        size_total = run_any_query(total_size)
        size_sentence_int = int(size_sentence[:-4])
        size_dict_int = int(size_dict[:-4])
        size_total_int = int(size_total[:-4])
        percentage = round(((size_sentence_int + size_dict_int) / (size_total_int + size_dict_int)) * 100, 2)
        sizes['total'] = percentage

    elif DBMS == 'MayBMS':
        pass
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    close_pg()
    write_metric('size', sizes)


def get_metrics():
    char_count()
    error_rate()
    runtime()
    prob_size()
    if ERRORS:
        write_errors(ERRORS)
