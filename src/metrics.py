import sys

from src.connect_db import run_any_query
from src.graph_creator import gen_char_bar, gen_time_bar
from parameters import DBMS, QUERIES
from queries_dubio import DUBIO_QUERIES_DICT
from queries_maybms import MAYBMS_QUERIES_DICT
from src.output_tui import write_metric, write_errors, write_table

QUERY_FUNCTIONALITY = {
    'test_1':           'There is likely an error in the database connection, \n' 
                        '                        or the database systems itself might be setup inappropriately.',
    'insight_1':        'The database likely has problems digesting large volumes of data.',
    'insight_2':        'No special function is tested in this query. The error is likely due to other reasons.',
    'insight_3':        'No special function is tested in this query. The error is likely due to other reasons.',
    'insight_4':        'The DBMS might lack the ability to verify if a record is certain.',
    'insight_5':        'The DBMS might lack the ability to retrieve an offer based on its sentence/probability space.',
    'insight_6':        'The DBMS might lack the ability to calculate the probability of a composed query result.',
    'probabilistic_1':  'The DBMS might lack the ability to retrieve the probability of a single record.',
    'probabilistic_2':  'The DBMS might lack the ability to calculate the expected count.',
    'probabilistic_3':  'The DBMS might lack the ability to calculate the expected sum.',
    'probabilistic_4':  'The DBMS might lack the ability to calculate the probability of a composed query result. \n'
                        '                        It may struggle composing large and/or complex sentences/probability spaces.',
    'probabilistic_5':  'The DBMS might lack the ability to return a single most probable answer. \n'
                        '                        It might lack the ability to filter based on probability.',
    'probabilistic_6':  'The DBMS might lack the ability to filter based on probability.',
    'IUD_1_rollback':   'There is likely an error in the database connection, \n'
                        '                        or the database systems itself might be setup inappropriately. \n'
                        '                        The DBMS might lack the ability to add probabilistic data. \n'
                        '                        The DBMS might lack the ability to repair the probability space after insertion of new data.',
    'IUD_2_rollback':   'There is likely an error in the database connection, \n'
                        '                        or the database systems itself might be setup inappropriately. \n'
                        '                        The DBMS might struggle with digesting and inserting large volumes of data. \n'
                        '                        The DBMS might lack the ability to repair the probability space after insertion of new data.',
    'IUD_3_rollback':   'The DBMS might lack the support to alter the uncertainty of a record.',
    'IUD_4_rollback':   'The DBMS might lack the ability to add new evidence to the database, \n'
                        '                        or repair the probability space after this data is added.',
    'IUD_5_rollback':   'There is likely an error in the database connection, \n'
                        '                        or the database systems itself might be setup inappropriately. \n'
                        '                        The DBMS might lack the ability to delete probabilistic data. \n'
                        '                        The DBMS might lack the ability to repair the probability space after deletion of data.',
    'IUD_repairkey':    'No error may occur in this piece of code. In case of an error, verify how this code differs '
                        '                        from the repair key statements in QuestionMark: The Dataset Generator.'
}
QUERIES_FAILED = 0
ERRORS = {}
RUNTIME_TOTAL = {}
RUNTIME_PLAN = {}
RUNTIME_EXEC = {}


def add_failed(error, query_name):
    global QUERIES_FAILED
    global ERRORS
    QUERIES_FAILED += 1
    ERRORS[query_name] = (str(error))


def add_runtime(query, total, plan, exe):
    global RUNTIME_TOTAL
    global RUNTIME_PLAN
    global RUNTIME_EXEC

    if total:
        RUNTIME_TOTAL[query] = total
    if plan:
        RUNTIME_PLAN[query] = plan
    if exe:
        RUNTIME_EXEC[query] = exe


def char_count():
    if DBMS == 'MayBMS':
        query_dict = MAYBMS_QUERIES_DICT
    elif DBMS == 'DuBio':
        query_dict = DUBIO_QUERIES_DICT
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    count = 0
    query_characters = {}
    for query_name in QUERIES:
        query = query_dict[query_name]
        query_count = sum(len(x) for x in query.split())
        count += query_count
        query_characters[query_name] = query_count

        # For some insert, update, delete queries, large text inputs are included. These skew the results.
        # The character count of that is manually determined and subtracted here.
        # Be critical of what you want to delete and what you want to include.
        if DBMS == 'DuBio':
            if query_name == 'IUD_1_rollback':
                count -= 9805
                query_characters[query_name] = query_count - 9805
            if query_name == 'IUD_2_rollback':
                count -= 35410
                query_characters[query_name] = query_count - 35410

        if DBMS == 'MayBMS':
            if query_name == 'IUD_1_rollback':
                count -= 9439
                query_characters[query_name] = query_count - 9439

    write_metric('char', count)
    gen_char_bar(query_characters)


def error_rate():
    percentage_failed = round((QUERIES_FAILED / len(QUERIES)) * 100, 2)
    write_metric('error', 100 - percentage_failed)


def runtime():
    write_metric('runtime', [round(sum(RUNTIME_TOTAL.values()), 2), round(sum(RUNTIME_PLAN.values()), 2),
                             round(sum(RUNTIME_EXEC.values()), 2)])
    gen_time_bar(RUNTIME_TOTAL, RUNTIME_PLAN, RUNTIME_EXEC)


def prob_size():
    sizes = {}

    if DBMS == 'DuBio':
        sentence_size = "SELECT pg_size_pretty(SUM(pg_column_size(_sentence))) FROM offers;"
        dict_size = "SELECT pg_size_pretty(pg_total_relation_size('_dict'));"
        total_size = "SELECT pg_size_pretty(pg_total_relation_size('offers'));"

        size_sentence = run_any_query(sentence_size)
        sizes['_sentence column is:'] = size_sentence
        size_dict = run_any_query(dict_size)
        sizes['dict table is:'] = size_dict
        size_total = run_any_query(total_size)
        size_sentence_int = int(size_sentence[:-4])
        size_dict_int = int(size_dict[:-4])
        size_total_int = int(size_total[:-4])
        percentage = round(((size_sentence_int + size_dict_int) / (size_total_int + size_dict_int)) * 100, 2)
        sizes['total'] = percentage

    elif DBMS == 'MayBMS':
        size_setup_query = "SELECT pg_size_pretty(pg_total_relation_size('offers_setup'));"
        size_total_query = "SELECT pg_size_pretty(pg_total_relation_size('offers'));"
        duplicate_percentile_query = "SELECT (dist.ids::float / comp.ids::float) AS percentage FROM (SELECT COUNT(id) AS ids FROM offers_setup) AS comp, (SELECT COUNT(DISTINCT id) AS ids FROM offers_setup) AS dist;"
        size_setup = run_any_query(size_setup_query)
        size_total = run_any_query(size_total_query)
        duplicate_percentage = run_any_query(duplicate_percentile_query)
        size_total_int = int(size_total[:-4])
        size_total_quantity = size_total[-4:]
        size_setup_int = int(size_setup[:-4])
        size_setup_quantity = size_setup[-4:]
        duplicate_percentage_float = float(duplicate_percentage)
        if size_setup_quantity != size_total_quantity:
            print('The size metric displayed is incorrect. Sorry for the inconvenience.')
        prob_space_size = size_total_int - size_setup_int
        sizes['probability space is:'] = str(prob_space_size) + size_setup_quantity
        print()
        sizes['duplicate records is:'] = str(round((size_setup_int * duplicate_percentage_float), 2)) + size_setup_quantity
        percentage = round((size_setup_int * (1 - duplicate_percentage_float) + prob_space_size) / size_total_int * 100, 2)
        sizes['total'] = percentage
    else:
        sys.exit("Please input a valid DBMS in parameters.py. Choose either 'MayBMS' or 'DuBio'.")

    write_metric('size', sizes)


def digest_errors(errors):
    write_table(errors, [RUNTIME_TOTAL, RUNTIME_PLAN, RUNTIME_EXEC])
    if errors:
        write_errors(errors, QUERY_FUNCTIONALITY)


def get_metrics():
    char_count()
    error_rate()
    runtime()
    digest_errors(ERRORS)
