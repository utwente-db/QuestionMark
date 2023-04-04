from connect_db import execute_query, connect_pg, close_pg
from parameters import QUERIES
from output_tui import create_result_file, write_query_type


def run_benchmark():
    create_result_file()

    connect_pg(configname='database.ini')

    count = 0
    for query in QUERIES:
        count += 1
        write_query_type(query)
        execute_query(query)
        print(str(count) + " out of " + str(len(QUERIES)) + " queries done.")

    close_pg()


if __name__ == '__main__':
    pass
