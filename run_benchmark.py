from execute_query import connect_pg, close_pg, execute_query
from parameters import QUERIES
from output_tui import create_result_file, create_metrics_file, write_query_type
from metrics import get_metrics


def test_connection():
    connect_pg(configname='database.ini')
    execute_query('test_1')
    print('\nIf no error is shown, the connection is working! :)')
    close_pg()


def run_benchmark():
    create_result_file()
    create_metrics_file()
    connect_pg(configname='database.ini')
    count = 0
    for query in QUERIES:
        count += 1
        write_query_type(query)
        execute_query(query)
        print(query + " finished. Currently " + str(count) + " out of " + str(len(QUERIES)) + " queries done.")

    get_metrics()
    close_pg()
