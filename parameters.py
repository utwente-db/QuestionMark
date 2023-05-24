# This file contains all parameters that can be changed to tweak the behaviour of the benchmark.

# # ==========================
# # DATABASE MANAGEMENT SYSTEM
# # ==========================

# # Don't forget to change the database.ini as well!
DBMS = 'MayBMS'
# DBMS = 'DuBio'


# # =============
# # QUERY RUNTIME
# # =============

# The amount of times a query is run to obtain the average run time.
ITERATIONS = 2

# The maximum time a query may run before it is aborted. Increase drastically to enforce 'no' timeout.
# Not yet in use.
TIMEOUT = 60


# # ================
# # OTHER PARAMETERS
# # ================

# If true, the query plan of each query is also provided with the benchmark results.
SHOW_QUERY_PLAN = False


# # =======
# # QUERIES
# # =======

# For the purpose of each query, please see queries_pseudocode.txt
QUERIES = [
    'test_1',

    'insight_1',

    'insight_2',

    'insight_3',

    'insight_4',

    'insight_5',

    'insight_6',

    'probabilistic_1',

    'probabilistic_2',

    'probabilistic_3',

    'probabilistic_4',

    'probabilistic_5',

    'probabilistic_6',

    'IUD_1_rollback',

    'IUD_2_rollback',

    'IUD_3_rollback',

    'IUD_4_rollback',

    'IUD_5_rollback'
]


