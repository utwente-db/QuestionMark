# This file contains all parameters that can be changed to tweak the behaviour of the benchmark.

# # ================
# # OTHER PARAMETERS
# # ================

# If true, a simple query will be run to test the connection to the database.
TEST = False

# If true, the query plan of each query is also provided with the benchmark results.
SHOW_QUERY_PLAN = True


# # ==========================
# # DATABASE MANAGEMENT SYSTEM
# # ==========================

# # Don't forget to change the database.ini as well!
# DBMS = 'MayBMS'
DBMS = 'DuBio'


# # =============
# # QUERY RUNTIME
# # =============

# The number of times a query is run to obtain the average run time.
ITERATIONS = 5

# The maximum time a query may run before it is aborted. Increase drastically to enforce 'no' timeout.
# Not yet in use.
TIMEOUT = 60


# # =======
# # QUERIES
# # =======

# For the purpose of each query, please see queries_pseudocode.txt
QUERIES = [
    'test_1',       # Simple query to test the connection.

    'insight_1',    # Retrieves the full dataset, gain insight in data structure and load handling.

    'insight_2',    # Provides insight into the dataset and probability handling.

    'insight_3',    # Provides insight into the distribution of cluster volumes.

    'insight_4',    # Gets the percentage of certain clusters.

    'insight_5',    # Gets the id and probability of the offers with a specific variable value or sentence.

    'insight_6',    # Gets the average probability of the dataset.

    'probabilistic_1',  # Gets offers with the probability of their occurrence.

    'probabilistic_2',  # Gets the expected count of the categories.

    'probabilistic_3',  # Gets the expected sum of the product ids per cluster.

    'probabilistic_4',  # Gets the sentence and probability per category.

    'probabilistic_5',   # Returns the most probable offer that is related to 'ford'.

    'probabilistic_6',  # Returns all offers containing 'Ford' with a high uncertainty so they can be classified by human inspection.

    'IUD_1_rollback',   # Inserting a single row.

    'IUD_2_rollback',   # Inserting bulk.

    'IUD_3_rollback',   # Updates uncertainty.

    'IUD_4_rollback',   # Removes uncertainty.

    'IUD_5_rollback',   # Deletes a cluster.

    # Run query below only with MayBMS!
    # 'IUD_repairkey',  # Repairs the probability space after an IUD query. Still crashes.
]


