# This file contains the benchmark queries in the dialect of DuBio.
# Go to queries_pseudo_code.py for an overview of the queries available for this benchmark.


# ====== TEST THE CONNECTION ==================================================================== #

query_test_1 = """
SELECT *
FROM offers
LIMIT 10;
"""

query_test_2 = """
SELECT COUNT(*)
FROM offers;
"""

query_test_3 = """
SELECT COUNT(DISTINCT(id))
FROM offers;
"""


# ====== BASIC QUERIES ========================================================================== #