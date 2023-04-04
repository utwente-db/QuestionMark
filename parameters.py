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
    # 'test_1',

    # 'insight_1',  # fails with MayBMS

    # 'insight_2',  # fails with MayBMS

    # 'basic_1',

    # 'basic_2',

    # 'basic_3',  ## fails with MayBMS

    # 'basic_4',

    # 'basic_5',

    # 'basic_6',  # fails with MayBMS

    # 'basic_7',

    # 'basic_8',  # fails with MayBMS

    # 'basic_9',  # fails with MayBMS

    # 'basic_10',  # fails with MayBMS

    # 'basic_11_view',  # fails with MayBMS

    # 'complex_1',

    # 'complex_2',

    # 'probabilistic_1',  # fails with MayBMS
    #
    # 'probabilistic_2',  # fails with MayBMS

    # TODO: next queries
    # 'probabilistic_3',  # fails with MayBMS
    #
    # 'probabilistic_4',  # fails with MayBMS

    # 'IUD_1_rollback',

    # 'IUD_2_rollback',

    # 'IUD_3_rollback',

    # 'IUD_4_rollback',

    # 'IUD_5_rollback',

    'IUD_6_rollback',

    # 'IUD_7_rollback',  # Does not work in DuBio yet.

    # 'IUD_8_rollback',

    # 'IUD_9_rollback'
]


