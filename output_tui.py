from parameters import ITERATIONS
from queries_dubio import DUBIO_QUERIES_DICT


def create_result_file():
    with open('benchmark_results.txt', 'w+') as file:
        file.write('This file contains the results of the benchmark test. \n\n')


def write_query_type(query_num):
    with open('benchmark_results.txt', 'a') as file:
        file.write("\n\n\n# ============== " + query_num + " ============== #")


def write_time(planning_time, execution_time):
    with open('benchmark_results.txt', 'a') as file:
        file.write("\n\nAverage planning time over " + str(ITERATIONS) + " iterations: " + str(planning_time) + " ms.")
        file.write("\nAverage execution time over " + str(ITERATIONS) + " iterations: " + str(execution_time) + " ms.")


def write_results(printable_output, query):
    with open('benchmark_results.txt', 'a') as file:
        file.write('\n')
        file.write(DUBIO_QUERIES_DICT[query])
        file.write('\n')
        file.write(printable_output)
        file.write('\n')


def format_result(cur):
    result = cur.fetchall()

    if not result:
        return '+---------------------------------+\n' \
               '| This query returned no records. |\n' \
               '+---------------------------------+\n'

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
