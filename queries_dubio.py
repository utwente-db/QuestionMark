# This file contains the benchmark queries in the dialect of DuBio.
# Go to queries_pseudo_code.py for an overview of the queries available for this benchmark.


DUBIO_QUERIES_DICT = {

    # ====== TEST THE CONNECTION ==================================================================== #

    'query_test_1': """
        SELECT *
        FROM offers
        LIMIT 10;
        """,

    # ====== BASIC QUERIES ========================================================================== #

    'query_basic_1': """
        SELECT COUNT(*) as records, COUNT(DISTINCT(id)) as offers, COUNT(DISTINCT(cluster_id)) as clusters
        FROM offers;
        """,

    'query_basic_2': """
        SELECT cluster_size, COUNT(cluster_size) as amount
        FROM (
            SELECT COUNT(DISTINCT(id)) as cluster_size
            FROM offers
            GROUP BY cluster_id
        ) as cluster_sizes
        GROUP BY cluster_size
        ORDER BY cluster_size ASC;
        """,

    # ====== CONDITIONAL QUERIES ==================================================================== #

    'query_condition_1_view': """
        CREATE OR REPLACE VIEW fords AS 
            SELECT * 
            FROM offers
            WHERE title LIKE '%ford%'
            OR description LIKE '%ford%'
            OR brand LIKE '%ford%';
        """,

    'query_condition_1': """
        SELECT *
        FROM offers
        WHERE cluster_id IN (
            SELECT cluster_id
            FROM fords
        )
        ORDER BY cluster_id ASC;
        """,

    'query_condition_1_insights': """
        SELECT 
            (SELECT COUNT(*) FROM fords) AS ford_count, 
            COUNT(*) AS total_cluster_count
        FROM fords
        LEFT JOIN (
            SELECT cluster_id, id
            FROM offers
            WHERE cluster_id IN (
                SELECT cluster_id
                FROM fords
            ) 
        ) AS joined_table
        ON fords.id = joined_table.id;
        """,

    'query_condition_2': """
        SELECT id, cluster_id, title, _sentence
        FROM offers
        WHERE cluster_id IN (
            SELECT cluster_id
            FROM fords
        )
        ORDER BY cluster_id ASC;
        """,

    # ====== PROBABILITY CENTERED QUERIES =========================================================== #

    # ====== AGGREGATE QUERIES ====================================================================== #

    # ====== EVIDENCE ADDITION ====================================================================== #

    # ====== INSERT, UPDATE, DELETE ================================================================= #

    # To analyse INERT UPDATE DELETE without it actually affecting the data.
    # BEGIN;
    # EXPLAIN ANALYZE ...;
    # ROLLBACK;

    'query_insert_1': 'insert_offers.sql',  # Doesn't work yet.

    'query_insert_2': 'insert_dict.sql',    # Doesn't work yet.

    'query_update_1': """
        bla
        """,

    'query_update_2': """
        bla
        """,

    'query_delete_1': """
        bla
        """,


    # ====== Some queries that could be included ================================================================= #

    # Use case Bol.com

    # Get the product categories and how many products you sell of each.
    'query_something_1': """
        SELECT category, COUNT(category) AS offers_count
        FROM offers
        GROUP BY category
        ORDER BY offers_count DESC;
        """
    # Need expected COUNT

    # Get the certainty per product category

}





