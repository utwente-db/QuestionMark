# This file contains the benchmark queries in the dialect of DuBio.
# Go to queries_pseudo_code.txt for an overview of the queries available for this benchmark.


DUBIO_QUERIES_DICT = {

    # ====== TEST THE CONNECTION ==================================================================== #

    # Testing the connection
    'test_1': """
    SELECT *
    FROM offers
    LIMIT 10;
    """,

    # ====== INSIGHT QUERIES ========================================================================== #

    # Retrieve the full dataset, gain insight in data structure.
    'insight_1': """
    SELECT * 
    FROM offers;

    SELECT print(dict) FROM _dict WHERE name='mydict';
    """,

    # Provide insight into the dataset.
    'insight_2': """
    SELECT COUNT(*) as records, 
        COUNT(DISTINCT(id)) as offers, 
        COUNT(DISTINCT(cluster_id)) as clusters
    FROM offers;
    """,

    # Provide insight into the distribution of cluster volumes.
    'insight_3': """
    SELECT cluster_size, COUNT(cluster_size) as amount
    FROM (
        SELECT COUNT(DISTINCT(id)) as cluster_size
        FROM offers
        GROUP BY cluster_id
    ) as cluster_sizes
    GROUP BY cluster_size
    ORDER BY cluster_size ASC;
    """,

    # Gets the percentage of certain clusters.
    'insight_4': """
    WITH certain_count AS (
        SELECT COUNT(CASE WHEN istrue(_sentence) THEN 1 END) AS cnt
        FROM offers
    ), total_count AS (
        SELECT COUNT(*) AS cnt
        FROM offers 
    )
    SELECT ROUND(certain_count.cnt::decimal / total_count.cnt::decimal, 4) * 100 AS certain_percentage
    FROM certain_count, total_count; 
    """,

    # Get the id of the offers with sentence 'w8=1'.
    'insight_5': """
    WITH prob AS (
        SELECT prob(dict, 'w8=1') AS probability
        FROM _dict 
        WHERE name = 'mydict'
    )
    SELECT offers.id, prob.probability, hasrva(_sentence, 'w8=1')
    FROM offers, prob  
    WHERE hasrva(_sentence, 'w8=1');
    """,

    # Get the average probability of the dataset.
    'insight_6': """ 
    SELECT AVG(probability) AS certainty_of_the_dataset
    FROM (
        SELECT round(prob(d.dict, p._sentence)::NUMERIC, 4) AS probability
        FROM part p, _dict d
        WHERE d.name = 'mydict'
    ) AS probabilities;	
    """,



    # ====== PROBABILISTIC QUERIES ========================================================================== #

    # Get offers with the probability of their occurrence.
    'probabilistic_1': """
    SELECT round(prob(d.dict, p._sentence)::NUMERIC, 4) AS probability, p.*
    FROM part p, _dict d
    WHERE d.name = 'mydict'
    ORDER BY probability DESC;
    """,

    # Gets the expected count of the categories.
    'probabilistic_2': """
    SELECT category, SUM(prob(d.dict, p._sentence)) AS expected_count
    FROM part p, _dict d
    WHERE d.name = 'mydict'
    GROUP BY category
    ORDER BY expected_count DESC;
    """,

    # Gets the expected sum of the product ids per cluster
    'probabilistic_3': """
    SELECT cluster_id, ROUND(SUM(id * prob(d.dict, p._sentence))::NUMERIC, 2) AS expected_sum, COUNT(id) AS number_of_offers
    FROM part p, _dict d
    WHERE d.name = 'mydict'
    GROUP BY cluster_id
    ORDER BY number_of_offers;
    """,

    # Gets the sentence and probability for the categories
    'probabilistic_4': """
    WITH category_sentence AS (
        SELECT category, AGG_OR(_sentence) AS sentence
        FROM part
        GROUP BY category
    )
    SELECT cs.*, round(prob(d.dict, cs.sentence)::NUMERIC, 4) AS probability
    FROM category_sentence cs, _dict d
    WHERE d.name = 'mydict'
    ORDER BY probability DESC;
    """,

    # Search Ford of web shop, where most probable product should be returned
    'probabilistic_5': """ 
    SELECT p.*, round(prob(d.dict, _sentence)::NUMERIC, 4) AS probability
    FROM part p, _dict d
    WHERE cluster_id IN (
        SELECT cluster_id
        FROM part 
        WHERE title LIKE '%ford%' 
        OR description LIKE '%ford%'
    ) 
    ORDER BY probability DESC 
    LIMIT 1;
    """,

    # Returns all offers with high uncertainty for human check
    # TODO: still needs to be checked in DBeaver.
    'probabilistic_6': """
    SELECT p.id, p.cluster_id, p.brand, p.category, p.identifiers
    FROM part p, _dict d
    WHERE prob(d.dict, _sentence) > 0.45
    AND prob(d.dict, _sentence) < 0.55;
    """,



    # ====== INSERT, UPDATE, DELETE ================================================================= #

    'IUD_1_rollback': """
    INSERT INTO offers(id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, _sentence)
        VALUES(0, 543, 'david yurman 5mm sterling silver and citrine cable classics bracelet yoogi s closet', 'david yurman', 'Jewelry', 'this gorgeous david yurman 5mm sterling silver and citrine cable classics bracelet is an elegant classic that will never go out of style it features the signature cable design in sterling silver two dainty faceted citrine stones end caps and 14k gold details makes for a great everyday bracelet or a fabulous gift retail price is 625 the bracelet is clean and beautiful throughout with no visible signs of wear', 'cad 60 35 cad', '[{"/productID": "[11106896]"}]', 'None', 'shipping method estimated transit time fee per order standard ups ground 1 5 business days free expedited ups 2 day delivery on monday friday 2 business days 24 95 apo fpo alaska and hawaii usps priority insured 6 10 business days free canada usps priority insured 6 10 business days 19 95 canada usps express insured 3 5 business days 29 95 international usps priority insured 6 10 business days 29 95 international usps express insured 3 5 business days 39 95', Bdd('a88x3=1&w88=3') );
    """,

    'IUD_2_rollback': """
    INSERT INTO offers(id, cluster_id, title, brand, category, description, price, identifiers, keyvaluepairs, spectablecontent, _sentence)
        SELECT * FROM bulk_insert;	
    """,

    'IUD_3_rollback': """
    UPDATE _dict
    SET dict = add(dict, 't1=1:0.7; t1=2:0.2; t1=3:0.1; t2=1:0.3; t2=2:0.2; t2=3:0.5; t3=1:0.6; t3=2:0.4;')
    WHERE name='mydict';
    """,

    'IUD_4_rollback': """
        UPDATE offers 
        SET brand = 'Johnny Was',
            price = 'usd 15 95',
            description = 'johnny was women s besimo scarf country outfitter wear when cold one size fits all height 100 cm width 120 cm'
        WHERE id = 1001690;
    """,

    'IUD_5_rollback': """
        UPDATE offers 
        SET category = 'Clothing',
            identifiers = '[{"/sku": "[cwkbcw004]"}]',
            _sentence = Bdd('a468=0')
        WHERE cluster_id = 468;
        
        UPDATE offers 
        SET cluster_id = 468,
            brand = 'chef works',
            _sentence = Bdd('a468=1')
        WHERE cluster_id = 469;
    """,

    'IUD_6_rollback': """
    WITH max_cluster AS (
        SELECT (max(cluster_id) + 1) AS max_id
        FROM offers
    )
    UPDATE offers 
    SET cluster_id = max_cluster.max_id,
        _sentence = Bdd('1')
    FROM max_cluster
    WHERE id = 12071001;
    
    WITH max_cluster AS (
        SELECT max(cluster_id) + 2 AS max_id
        FROM offers
    )
    UPDATE offers 
    SET cluster_id = max_cluster.max_id,
        _sentence = Bdd('1')
    FROM max_cluster
    WHERE id = 16457529;
    
    UPDATE offers 
    SET _sentence = Bdd('a1471=0')
    WHERE id = 7339350;
    
    UPDATE offers 
    SET _sentence = Bdd('a1471=1')
    WHERE id = 12326926;
    """,

    'IUD_7_rollback': """
    UPDATE _dict
    SET dict = del(dict, 'w64=3, w64=4')
    WHERE name='mydict';
    
    UPDATE _dict
    SET dict = upd(dict, 'w64=1:0.4, w64=2:0.6')  
    WHERE name='mydict';
    
    UPDATE _dict
    SET dict = add(dict, 'a468=1:0.3, a468=2:0.7')
    WHERE name='mydict';
    """,

    'IUD_8_rollback': """
    DELETE FROM offers 
    WHERE cluster_id = 141;
    """,

    'IUD_9_rollback': """
    SELECT del(dict, 'a141x1=0, a141x2=0, a141x3=0, a141x4=0, a141x5=0, a141x6=0, a141x7=0, a141x8=0, a141x9=0, a141x10=0, a141x12=0, a141x14=0, w141=1, w141=2, w141=3, w141=4, w141=5, w141=6, w141=7, w141=8, w141=9, w141=10, w141=12, w141=14') 
    FROM _dict 
    WHERE name='mydict';
    """
}





