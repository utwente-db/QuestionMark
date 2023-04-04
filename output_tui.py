from parameters import ITERATIONS, DBMS
from queries_dubio import DUBIO_QUERIES_DICT


def create_result_file():
    with open('benchmark_results.txt', 'w+') as file:
        if DBMS == 'MayBMS':
            file.write('The QUESTION MARK benchmark test. Run on MayBMS.\n')
        elif DBMS == 'DuBio':
            file.write('The QUESTION MARK benchmark test. Run on DuBio.\n')
        elif DBMS == 'PostgreSQL':
            file.write('The QUESTION MARK benchmark test. Run on PostgreSQL.\n')
        file.write('This file contains the results of this benchmark test. \n'
                   'The query plan and average run time are produced by PostgreSQL EXPLAIN ANALYSE.')


def write_query_type(query_num):
    with open('benchmark_results.txt', 'a') as file:
        file.write("\n\n\n# ============== " + query_num + " ============== #")


def write_time(planning_time, execution_time, total_time):
    with open('benchmark_results.txt', 'a') as file:
        if planning_time:
            file.write("Average planning time over " + str(ITERATIONS) + " iterations:  " + str(planning_time) + " ms.")
        if execution_time:
            file.write("\nAverage execution time over " + str(ITERATIONS) + " iterations: " + str(execution_time) + " ms.")
        if total_time:
            file.write("Average total time over " + str(ITERATIONS) + " iterations: " + str(total_time) + " ms.")


def write_explain_analyse(cur, result):
    with open('benchmark_results.txt', 'a') as file:
        file.write('\n' + format_result(cur, result) + '\n')


def write_query(query):
    with open('benchmark_results.txt', 'a') as file:
        file.write('\n' + DUBIO_QUERIES_DICT[query] + '\n')


def write_results(printable_output):
    with open('benchmark_results.txt', 'a') as file:
        file.write(str(printable_output) + '\n')


def format_result(cur, result=None):
    if not result:
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

    count = 0
    for row in result:
        count += 1
        if count < 20:
            printable_output += tavnit % row + '\n'
    printable_output += separator + '\n'
    if count >= 20:
        printable_output += 'The first 20 out of ' + str(count) + ' rows are shown. \n'

    return printable_output
