# This file contains all parameters that can be changed to tweak the behaviour of the benchmark.

# # ==========================
# # DATABASE MANAGEMENT SYSTEM
# # ==========================

# # Don't forget to change the database.ini as well!
# DBMS = 'MayBMS'
DBMS = 'DuBio'
# DBMS = 'PostgreSQL'


# # =============
# # QUERY RUNTIME
# # =============

# The amount of times a query is run to obtain the average run time.
ITERATIONS = 2


# # ================
# # OTHER PARAMETERS
# # ================

# If true, the query plan of each query is also provided with the benchmark results.
SHOW_QUERY_PLAN = True


# # =======
# # QUERIES
# # =======

# The list of queries to include. The following queries exist (see queries_pseudo_code.txt):
# Test queries:    query_test_1
# Basic queries:   query_basic_1, ...

# Queries that are grouped together should also be run together. Please uncomment full blocks.
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

    'IUD_5_rollback',

    'IUD_6_rollback',

    'IUD_7_rollback',

    'IUD_8_rollback',

    'IUD_9_rollback'
]


