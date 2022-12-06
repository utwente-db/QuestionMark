import queries_dubio
from queries_dubio import *
from queries_maybms import *
from connect_db import execute_query, connect_pg, close_pg
from parameters import QUERIES, ITERATIONS, TIMED


def create_result_file():
    with open('benchmark_results.txt', 'w+') as file:
        file.write('This file contains the results of the benchmark test. \n\n')


def write_results(query_num, runtime, printable_output, query):
    with open('benchmark_results.txt', 'a') as file:
        file.write("# ========== " + query_num + " ========== #")
        file.write(query)
        file.write('\n')
        file.write(printable_output)
        file.write('\n')
        file.write("Runtime over " + str(ITERATIONS) + " iterations: " + str(runtime) + " seconds.")
        file.write('\n\n\n')


def test_connection():
    execute_query(queries_dubio.query_test_1)


def run_benchmark():
    create_result_file()

    for query in QUERIES:
        print("running benchmark test for", query)
        if query == "query_test_1":
            runtime, result = execute_query(queries_dubio.query_test_1)
            write_results(query, runtime, result, queries_dubio.query_test_1)
        if query == "query_test_2":
            runtime, result = execute_query(queries_dubio.query_test_2)
            write_results(query, runtime, result, queries_dubio.query_test_2)
        if query == "query_test_3":
            runtime, result = execute_query(queries_dubio.query_test_3)
            write_results(query, runtime, result, queries_dubio.query_test_3)
        # where the value from query = query_test_1
        # see test_connection()


if __name__ == '__main__':
    connect_pg(configname='database.ini')

    # test_connection()
    run_benchmark()

    close_pg()
