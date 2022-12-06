# This file contains all parameters that can be changed to tweak the behaviour of the benchmark.


# # =============
# # QUERY RUNTIME
# # =============

# Indicates whether the execution is timed or not. Boolean value.
TIMED = True

# The amount of times a query is run to obtain the average run time.
ITERATIONS = 100


# # =======
# # QUERIES
# # =======

# The list of queries to include. The following queries exist (see queries_pseudo_code.py):
# Test queries:    query_test_1
# Basic queries:   query_basic_1, ...

QUERIES = ['query_test_1', 'query_test_2', 'query_test_3']
