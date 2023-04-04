# This file contains the benchmark queries in the dialect of MayBMS.
# Go to queries_pseudo_code.py for an overview of the queries available for this benchmark.


MAYBMS_QUERIES_DICT = {

    # ====== TEST THE CONNECTION ==================================================================== #

    # Testing the connection
    'test_1': """
            SELECT *
            FROM offers
            LIMIT 10;
        """,

    # ====== INSIGHT QUERIES ========================================================================== #

    # Provide insight into the dataset.
    'insight_1': """
            SELECT COUNT(*) as records, 
    	        COUNT(DISTINCT(id)) as offers, 
    	        COUNT(DISTINCT(cluster_id)) as clusters
            FROM offers;
        """,

    # TODO for yellow :) -> Done till here

    # Provide insight into the distribution of cluster volumes.
    'insight_2': """
            SELECT cluster_size, COUNT(cluster_size) as amount
            FROM (
                SELECT COUNT(DISTINCT(id)) as cluster_size
                FROM offers
                GROUP BY cluster_id
            ) as cluster_sizes
            GROUP BY cluster_size
            ORDER BY cluster_size ASC;
        """,

    # ====== BASIC QUERIES ========================================================================== #

    # (select):  Selects the full table
    'basic_1': """
            SELECT * 
            FROM offers;
        """,

    # (project):  Selects the id, cluster_id, title and sentence of all offers
    'basic_2': """
            SELECT id, cluster_id, title, _v0, _d0, _p0, _v1, _d1, _p1
            FROM offers;
        """,

    # (join):  Joins the cluster table with the partial table
    'basic_3': """
            SELECT os.id, os.cluster_id, b.brand, c.category
            FROM offers_stripped os
            INNER JOIN brand b 
                ON b.id = os.brand
            INNER JOIN category c 
                ON c.id = os.category;
        """,

    # (restrict):  Selects all offers from cluster 100.
    'basic_4': """
            SELECT *
            FROM offers
            WHERE cluster_id = 100;
        """,

    # (restrict with pattern matching):  Selects all offers containing 'ford' in the description.
    'basic_5': """
            SELECT *
            FROM offers
            WHERE description LIKE '%ford%';
        """,

    # (Group By):  Group by cluster ids.
    'basic_6': """
            SELECT cluster_id
            FROM offers 
            GROUP BY cluster_id;
        """,

    # (Order by):  Order by title.
    'basic_7': """
            SELECT *
            FROM offers 
            ORDER BY title;
        """,

    # (Count + Distinct):  Count the distinct cluster ids.
    'basic_8': """
            SELECT COUNT(DISTINCT(cluster_id))
            FROM offers;
        """,

    # (SUM + restrict):  Get the sum of all ids with a cluster_id < 1000.
    'basic_9': """
            SELECT SUM(id)
            FROM offers
            WHERE cluster_id < 1000;
        """,

    # (AVG + ROUND + restrict):  Get the average of all ids with a cluster_id < 1000.
    'basic_10': """
            SELECT ROUND(AVG(id))
            FROM offers
            WHERE cluster_id < 1000;
        """,

    # (Create View):  Creates a view of all items 'ford'.
    'basic_11_view_rollback': """
            CREATE MATERIALIZED VIEW fords AS 
                SELECT * 
                FROM offers
                WHERE title LIKE '%ford%'
                OR description LIKE '%ford%'
                OR brand LIKE '%ford%';
        """,

    # ====== COMPLEX QUERIES ======================================================================== #

    # (Simple Nested Query):  Gets all offers from the 'ford' clusters.
    'complex_1': """
            SELECT id, cluster_id, title, _v0, _d0, _p0, _v1, _d1, _p1
            FROM offers
            WHERE cluster_id IN (
                SELECT cluster_id
                FROM fords
            )
            ORDER BY id, cluster_id ASC; 
        """,

    # (Join):  Shows a comparison of the results of the prev 2 queries.
    'complex_2': """
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

    # ====== PROBABILISTIC QUERIES ================================================================== #


    # ====== INSERT, UPDATE, DELETE ================================================================= #

    'IUD_1_rollback': """
    
    """,

    'IUD_2_rollback': """

    """,

    'IUD_3_rollback': """

    """,

    'IUD_4_rollback': """

    """,

    'IUD_5_rollback': """

    """,

    'IUD_6_rollback': """

    """,

    'IUD_7_rollback': """

    """,

    'IUD_8_rollback': """

    """,

    'IUD_9_rollback': """

    """

}
