from src.execute_query import connect_pg, close_pg, execute_query, timeout
from parameters import QUERIES, TIMEOUT
from src.output_tui import create_result_file, create_metrics_file, write_query_type
from src.metrics import get_metrics, prob_size, add_failed


def test_connection():
    connect_pg(configname='database.ini')
    error = execute_query('test_1', test=True)
    if error:
        print('\n The connection is not working :('
              '\n See the error above for more information.')
    else:
        print('\n The connection is working! :)')
    close_pg()


def run_benchmark():
    create_result_file()
    create_metrics_file()
    prob_size()
    count = 0
    for query in QUERIES:
        connect_pg(configname='database.ini')
        count += 1
        write_query_type(query)
        if TIMEOUT == -1:  # no timeout will take place.
            execute_query(query)
        else:
            func = timeout(TIMEOUT)(execute_query)
            try:
                func(query)
            except TimeoutError as error:
                add_failed(error, 'RUNTIME')
        print(query + " finished. Currently " + str(count) + " out of " + str(len(QUERIES)) + " queries done.")
        close_pg()

    get_metrics()
