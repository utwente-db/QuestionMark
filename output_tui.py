from parameters import ITERATIONS, DBMS, QUERIES
from queries_dubio import DUBIO_QUERIES_DICT
from queries_maybms import MAYBMS_QUERIES_DICT

METRIC_TABLE_BREAK = " +--------------------------------------------------------------------------+-------------------------+\n"
QUERY_TABLE_BREAK = " +-----------------+------+---------+---------------+----------------+ \n"


def create_result_file():
    with open('results/QM_query_results.txt', 'w+') as file:
        file.write('\n      # ============================================= #'
                   '\n      # ==============   QuestionMark  ============== #'
                   '\n      # ============================================= #'
                   '\n      # The query results file.'
                   '\n      # Run on ' + str(DBMS) + '.\n\n'
                   'This file contains the query results and runtimes of this benchmark test.\n'
                   'The query plan and average run time are produced by PostgreSQL EXPLAIN ANALYSE.\n'
                   'Please see \'benchmark_results_metrics\' for the results of the metrics.')


def write_query_type(query_num):
    with open('results/QM_query_results.txt', 'a') as file:
        file.write("\n\n\n# ============== " + query_num + " ============== #")


def write_time(planning_time, execution_time, total_time):
    with open('results/QM_query_results.txt', 'a') as file:
        if planning_time:
            file.write("\nAverage planning time over " + str(ITERATIONS) + " iterations:  " + str(planning_time) + " ms.")
        if execution_time:
            file.write("\nAverage execution time over " + str(ITERATIONS) + " iterations: " + str(execution_time) + " ms.\n")
        if total_time:
            file.write("Average total time over " + str(ITERATIONS) + " iterations: " + str(total_time) + " ms.")


def write_explain_analyse(cur, result):
    with open('results/QM_query_results.txt', 'a') as file:
        file.write('\n' + format_result(cur, result) + '\n')


def write_error(error):
    with open('results/QM_query_results.txt', 'a') as file:
        file.write('\nThe following error occurred while executing this query:\n' + str(error))


def write_query(query):
    with open('results/QM_query_results.txt', 'a') as file:
        if DBMS == 'DuBio':
            file.write('\n' + DUBIO_QUERIES_DICT[query] + '\n')
        elif DBMS == 'MayBMS':
            file.write('\n' + MAYBMS_QUERIES_DICT[query] + '\n')


def write_results(printable_output):
    with open('results/QM_query_results.txt', 'a') as file:
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
        max_col_length = min(max(list(map(lambda x: len(str(x[index])), result))), 50)
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
    too_long = False
    for row in result:
        count += 1
        for col in row:
            if isinstance(col, str) and len(col) > 50:
                too_long = True
        if not too_long:
            if count < 20:
                printable_output += tavnit % row + '\n'

    printable_output += separator + '\n'
    if count >= 20:
        printable_output += 'The first 20 out of ' + str(count) + ' rows are shown. \n'
    if too_long:
        printable_output += 'Some returned records were too large to display. This query returned ' + str(count) + ' rows.\n'

    return printable_output


def get_raw_result(cur, result=None):
    if not result:
        result = cur.fetchall()

    if not result:
        return 'This query returned no records.'

    output = ''
    for row in result:
        for content in row:
            output += str(content) + ' '
    return output


def create_metrics_file():
    with open('results/QM_metrics_results.txt', 'w+') as file:
        file.write(
            '\n      # ============================================= #'
            '\n      # ==============   QuestionMark  ============== #'
            '\n      # ============================================= #'
            '\n      # The metrics file.'
            '\n      # Run on ' + str(DBMS) + '.\n\n'
            ' This file contains the metrics of this benchmark test.\n'
            ' Please see \'benchmark_results_queries.txt\' for the results and runtimes of the queries.\n\n'
            ' The included metrics produced the following results:\n'
            + METRIC_TABLE_BREAK +
            ' |        METRIC                                                            +        VALUE            |\n'
            + METRIC_TABLE_BREAK)


def write_metric(metric, value):
    with open('results/QM_metrics_results.txt', 'a') as file:
        if metric == 'char':
            file.write(' | The total amount of characters needed for all queries:'.ljust(75) + ' | ' +
                       (str(value) + ' characters').ljust(23) + ' |\n' + METRIC_TABLE_BREAK)
        if metric == 'error':
            file.write(' | The percentage of successful queries is:'.ljust(75) + ' | ' +
                       (str(value) + '%').ljust(23) + ' |\n' +
                       ' |   (See below what functionality might be lacking) '.ljust(75) + ' | '.ljust(26) +
                       ' | \n' + METRIC_TABLE_BREAK)
        if metric == 'runtime':  # value is of type [total time, planning time, execution time]
            if value[0]:
                file.write(' | The total runtime of all queries is:'.ljust(75) + ' | ' +
                           (str(value[0]) + ' ms').ljust(23) + ' |\n' +
                           ' |   (The sum of all time averages over ' + str(ITERATIONS) + ' iterations) '.ljust(34) + ' | '.ljust(26) +
                           ' | \n' + METRIC_TABLE_BREAK)
            if value[1]:
                file.write(' | The total planning time of all queries is:'.ljust(75) + ' | ' +
                           (str(value[1]) + ' ms').ljust(23) + ' |\n' +
                           ' |   (The sum of all time averages over ' + str(ITERATIONS) + ' iterations) '.ljust(34) + ' | '.ljust(26) +
                           ' | \n' + METRIC_TABLE_BREAK)
            if value[2]:
                file.write(' | The total execution time of all queries is:'.ljust(75) + ' | ' +
                           (str(value[2]) + ' ms').ljust(23) + ' |\n' +
                           ' |   (The sum of all time averages over ' + str(ITERATIONS) + ' iterations) '.ljust(34) + ' | '.ljust(26) +
                           ' | \n' + METRIC_TABLE_BREAK)
        if metric == 'size':
            for relation, size in value.items():
                if relation == 'total':
                    file.write(' | The percentage of data used for probabilistic representation:'.ljust(75) + ' | ' +
                               (str(size) + '%').ljust(23) + ' |\n' + METRIC_TABLE_BREAK)
                else:
                    file.write((' | The total size of the ' + relation).ljust(75) + ' | ' +
                               size.ljust(23) + ' |\n' + METRIC_TABLE_BREAK)


def write_table(errors, runtimes):
    with open('results/QM_metrics_results.txt', 'a') as file:
        file.write("\n\n # An overview of the queries that finished with their execution time:\n"
                   + QUERY_TABLE_BREAK +
                   " |   QUERY NAME    | Done | Runtime | Planning Time | Execution Time | \n"
                   + QUERY_TABLE_BREAK)

        total_time = "-"
        plan_time = "-"
        exec_time = "-"
        for query in QUERIES:
            done = " x  "
            if query in errors.keys():
                done = "    "
            if DBMS == "MayBMS":
                total_time = runtimes[0].get(query) if runtimes[0].get(query) else "-"
            if DBMS == "DuBio":
                plan_time = runtimes[1].get(query) if runtimes[1].get(query) else "-"
                exec_time = runtimes[2].get(query) if runtimes[2].get(query) else "-"
            file.write(" | " + query.ljust(15) + " | " + done + " | " + str(total_time).ljust(7) + " | " +
                       str(plan_time).ljust(13) + " | " + str(exec_time).ljust(14) + " | \n" + QUERY_TABLE_BREAK)


def write_errors(errors, functionality):
    with open('results/QM_metrics_results.txt', 'a') as file:
        file.write("\n\n\n # ==== Overview of errors and possible missing functionality. ==== #\n"
                   " # Based on the errors thrown during benchmark testing, the batabase system might\n"
                   " # lack support for one or more functionalities. Please also verify the actual error\n"
                   " # thrown by the database manually, as that may provide a clearer indication of what\n"
                   " # went wrong during benchmarking. If a memory allocation error is thrown, you can\n"
                   " # alter the query to run it on the 'part' table to see if the functionality of the\n"
                   " # query is supported.\n\n")

        file.write(" # The following queries have raised an error:\n\n")

        for name, error in errors.items():
            file.write(' QUERY #:                ' + str(name) + '\n'
                       ' Functionality message:  ' + functionality[name] + '\n'
                       ' Error raised by DBMS: \n' + str(error) + '\n')
