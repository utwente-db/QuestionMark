# This file contains all parameters that can be changed to tweak the behaviour of the benchmark.

# # ==========================
# # DATABASE MANAGEMENT SYSTEM
# # ==========================

# DBMS = 'MayBMS'
DBMS = 'DuBio'
# DBMS = 'PostgreSQL'


# # =============
# # QUERY RUNTIME
# # =============

# The amount of times a query is run to obtain the average run time.
ITERATIONS = 5


# # =======
# # QUERIES
# # =======

# The list of queries to include. The following queries exist (see queries_pseudo_code.py):
# Test queries:    query_test_1
# Basic queries:   query_basic_1, ...

# Queries that are grouped together should also be run together. Please uncomment full blocks.
QUERIES = [
    'query_test_1',

    # 'query_basic_1',
    #
    # 'query_basic_2',
    #
    # 'query_condition_1_view',
    # 'query_condition_1',
    # 'query_condition_1_insights',
    #
    # 'query_condition_2',

    # 'query_something_1',
]


