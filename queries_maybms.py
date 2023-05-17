# This file contains the benchmark queries in the dialect of MayBMS.
# Go to queries_pseudocode.py for an overview of the queries available for this benchmark.


MAYBMS_QUERIES_DICT = {

    # ====== TEST THE CONNECTION ==================================================================== #

    # Testing the connection
    'test_1': """
    SELECT id
    FROM offers
    LIMIT 10;
    """,

    # ====== INSIGHT QUERIES ========================================================================== #

    # Retrieve the full dataset, gain insight in data structure.
    'insight_1': """
    SELECT * 
    FROM offers;
    """,

    # Provide insight into the dataset.
    'insight_2': """
    SELECT COUNT(*) as records, 
        COUNT(DISTINCT(id)) as offers, 
        COUNT(DISTINCT(cluster_id)) as clusters
    FROM offers_setup;
    """,

    # Provide insight into the distribution of cluster volumes.
    'insight_3': """
    SELECT cluster_size, COUNT(cluster_size) as amount
    FROM (
        SELECT COUNT(DISTINCT(id)) as cluster_size
        FROM offers_setup
        GROUP BY cluster_id
    ) as cluster_sizes
    GROUP BY cluster_size
    ORDER BY cluster_size ASC;
    """,

    # Gets the percentage of certain clusters.
    'insight_4': """
    SELECT ROUND(all_certain::decimal / all_offers::decimal, 4) * 100 AS certain_percentage
    FROM (
        SELECT COUNT(id) AS all_offers
        FROM offers_setup
    ) AS count_all, (
        SELECT COUNT(id) AS all_certain
        FROM (
            SELECT id, tconf() AS confidence
            FROM offers
        ) AS confidences
        WHERE confidence = 1
    ) AS count_cert;
    """,

    # Get the id of the offers with sentence 'w8=1'.
    'insight_5': """
    SELECT id, tconf(*), _v0
    FROM offers
    WHERE _v1 = 52379
    AND _d1 = 548185;
    """,

    # Get the average probability of the dataset.
    'insight_6': """ 
    SELECT AVG(tconf()) * 100 AS certainty_of_the_dataset
    FROM offers;
    """,



    # ====== PROBABILISTIC QUERIES ========================================================================== #

    # Get offers with the probability of their occurrence.
    'probabilistic_1': """
    SELECT round(conf()::NUMERIC, 4) AS probability, *
    FROM offers
    GROUP BY id
    ORDER BY probability DESC;
    """,

    # Gets the expected count of the categories.
    'probabilistic_2': """
    SELECT category, ECOUNT() AS expected_count
    FROM offers
    GROUP BY category
    ORDER BY expected_count DESC;
    """,

    # Gets the expected sum of the product ids per cluster
    'probabilistic_3': """
    SELECT cluster_id, esum(id), COUNT(id) AS number_of_offers
    FROM offers
    GROUP BY cluster_id
    ORDER BY number_of_offers DESC;
    """,

    # Gets the sentence and probability for the categories
    'probabilistic_4': """
    SELECT category, conf() AS probability
    FROM part
    GROUP BY category
    ORDER BY probability DESC;
    """,

    # Search Ford of web shop, where most probable product should be returned
    'probabilistic_5': """ 
    SELECT *, round(tconf()::NUMERIC, 4) AS probability
    FROM offers
    WHERE cluster_id IN (
        SELECT cluster_id
        FROM offers_setup 
        WHERE title LIKE '%ford%' 
        OR description LIKE '%ford%'
    ) 
    ORDER BY probability DESC 
    LIMIT 1;
    """,

    # Returns all offers with high uncertainty for human check
    'probabilistic_6': """
    SELESELECT id, cluster_id, brand, category, identifiers
    FROM offers
    WHERE title LIKE '%ford%' 
    OR description LIKE '%ford%'
    AND tconf() > 0.45
    AND tconf() < 0.55;ict, _sentence) < 0.55;
    """,



    # ====== INSERT, UPDATE, DELETE ================================================================= #

    'IUD_1_rollback': """
    INSERT INTO offers(id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, world_prob, attribute_prob)
	VALUES(0, 543, 'david yurman 5mm sterling silver and citrine cable classics bracelet yoogi s closet', 'david yurman', 'Jewelry', 'this gorgeous david yurman 5mm sterling silver and citrine cable classics bracelet is an elegant classic that will never go out of style it features the signature cable design in sterling silver two dainty faceted citrine stones end caps and 14k gold details makes for a great everyday bracelet or a fabulous gift retail price is 625 the bracelet is clean and beautiful throughout with no visible signs of wear', 'cad 60 35 cad', '[{"/productID": "[11106896]"}]', 'None', 'shipping method estimated transit time fee per order standard ups ground 1 5 business days free expedited ups 2 day delivery on monday friday 2 business days 24 95 apo fpo alaska and hawaii usps priority insured 6 10 business days free canada usps priority insured 6 10 business days 19 95 canada usps express insured 3 5 business days 29 95 international usps priority insured 6 10 business days 29 95 international usps express insured 3 5 business days 39 95', 0.55, 0.45),
		  (-1, 543, 'david yurman cable classics bracelet yoogi s closet', 'david yurman', 'Jewelry', 'with no visible signs of wear', 'cad 60 35 cad', '[{"/productID": "[11106896]"}]', 'None', 'shipping method estimated transit time fee per order standard ups ground 1 5 business days free expedited ups 2 day delivery on monday friday 2 business days 39 95', 0.55, 0.35),
		  (-2, 543, 'yoogi s closet', 'david yurman', 'Jewelry', 'None', 'cad 60 35 cad', '[{"/productID": "[11106896]"}]', 'None', 'None', 0.55, 0.2);
    """,

    'IUD_2_rollback': """
    INSERT INTO offers(id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, world_prob, attribute_prob)
    SELECT * FROM bulk_insert;	
    """,

    'IUD_3_rollback': """
    UPDATE offers 
    SET category = 'Clothing',
        identifiers = '[{"/sku": "[cwkbcw004]"}]',
        -- Verify how to set a new probability and update probability space
    WHERE cluster_id = 103
    AND id = 3283478;
    
    UPDATE offers 
    SET cluster_id = 468,
        brand = 'chef works',
            -- Verify how to set a new probability and update probability space
    WHERE cluster_id = 103
    and id = 13989780;
    """,

    'IUD_4_rollback': """
    UPDATE offers 
    SET cluster_id = max_cluster.max_id,
        -- verify how to set the probability to certain
    FROM (
        SELECT max(cluster_id) + 1 AS max_id
        FROM offers
    ) as max_cluster
    WHERE id = 12071001;
    
    UPDATE offers 
    SET cluster_id = max_cluster.max_id,
        -- verify how to set the probability to certain
    FROM (
        SELECT max(cluster_id) + 1 AS max_id
        FROM offers
    ) as max_cluster
    WHERE id = 16457529;
    
    UPDATE offers 
    SET -- verify how to set the right probability
    WHERE id = 7339350;
    
    UPDATE offers 
    SET -- verify how to set the right probability
    WHERE id = 12326926;
    """,

    'IUD_5_rollback': """
    DELETE FROM offers 
    WHERE cluster_id = 190;
    """
}

