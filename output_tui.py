from parameters import ITERATIONS, DBMS
from queries_dubio import DUBIO_QUERIES_DICT


def create_result_file():
    with open('benchmark_results_query.txt', 'w+') as file:
        file.write('\n      # ============================================= #'
                   '\n      # ==============   QuestionMark  ============== #'
                   '\n      # ============================================= #'
                   '\n      # The query results file.'
                   '\n      # Run on ' + str(DBMS) + '.\n\n'
                   'This file contains the query results and runtimes of this benchmark test.\n'
                   'The query plan and average run time are produced by PostgreSQL EXPLAIN ANALYSE.\n'
                   'Please see \'benchmark_results_metrics\' for the results of the metrics.')


def write_query_type(query_num):
    with open('benchmark_results_query.txt', 'a') as file:
        file.write("\n\n\n# ============== " + query_num + " ============== #")


def write_time(planning_time, execution_time, total_time):
    with open('benchmark_results_query.txt', 'a') as file:
        if planning_time:
            file.write("Average planning time over " + str(ITERATIONS) + " iterations:  " + str(planning_time) + " ms.")
        if execution_time:
            file.write("\nAverage execution time over " + str(ITERATIONS) + " iterations: " + str(execution_time) + " ms.")
        if total_time:
            file.write("Average total time over " + str(ITERATIONS) + " iterations: " + str(total_time) + " ms.")


def write_explain_analyse(cur, result):
    with open('benchmark_results_query.txt', 'a') as file:
        file.write('\n' + format_result(cur, result) + '\n')


def write_error(error):
    with open('benchmark_results_query.txt', 'a') as file:
        file.write('\nThe following error occurred while executing this query:\n' + str(error))


def write_query(query):
    with open('benchmark_results_query.txt', 'a') as file:
        file.write('\n' + DUBIO_QUERIES_DICT[query] + '\n')


def write_results(printable_output):
    with open('benchmark_results_query.txt', 'a') as file:
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


def get_raw_result(cur, result=None):
    if not result:
        result = cur.fetchall()

    if not result:
        return 'This query returned no records.'

    output = ''
    for row in result:
        for content in row:
            output += content + ' '
    return output


def create_metrics_file():
    with open('benchmark_results_metrics.txt', 'w+') as file:
        file.write('\n      # ============================================= #'
                   '\n      # ==============   QuestionMark  ============== #'
                   '\n      # ============================================= #'
                   '\n      # The metrics file.'
                   '\n      # Run on ' + str(DBMS) + '.\n\n'
                   'This file contains the metrics of this benchmark test.\n'
                   'Please see \'benchmark_results_queries.txt\' for the results and runtimes of the queries.\n\n')


def write_metric(metric, value):
    with open('benchmark_results_metrics.txt', 'a') as file:
        if metric == 'char':
            file.write('\nThe total amount of characters needed for all queries:         ' + str(value) + ' characters')
        if metric == 'error':
            file.write('\nThe percentage of successful queries is:                       ' + str(value) + '%')
        if metric == 'runtime':  # value is of type [total time, planning time, execution time]
            if value[0]:
                file.write('\nThe total average runtime of all queries is:                   ' + str(value[0]) + ' ms')
            if value[1]:
                file.write('\nThe total average planning time of all queries is:             ' + str(value[1]) + ' ms')
            if value[2]:
                file.write('\nThe total average execution time of all queries is:            ' + str(value[2]) + ' ms')
        if metric == 'size':
            for relation, size in value.items():
                if relation == 'total':
                    file.write('\nThe percentage of data used for probabilistic representation:  ' + str(size) + '%')
                else:
                    file.write('\nThe total size of the ' + relation + size)


def write_errors(errors):
    with open('benchmark_results_metrics.txt', 'a') as file:
        file.write('\n\n\n\n# ==== Overview of all errors thrown ==== #\n'
                   "# If a memory allocation error is thrown, you can alter the query to run it \n"
                   "# on the 'part' table to see if the functionality of the query is supported.")
        for name, error in errors.items():
            file.write('\n' + str(name) + '\n' + str(error))
