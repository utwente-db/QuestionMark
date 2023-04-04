# This file contains the preparatory queries in the dialect of DuBio.
# Go to queries_pseudo_code_prepare.txt for an overview of the queries available for this benchmark.

DUBIO_PREPARE_DICT = {

    'basic_3_1': """
        CREATE TABLE brand AS
            WITH brands AS (
                SELECT DISTINCT brand
                FROM offers
                ORDER BY brand
            ) SELECT ROW_NUMBER() OVER (ORDER BY brand) AS id, brand
            FROM brands;
    """,

    'basic_3_2': """
        ALTER TABLE brand 
        ADD PRIMARY KEY (id);
    """,

    'basic_3_3': """
        CREATE TABLE category AS
            WITH categories AS (
                SELECT DISTINCT category
                FROM offers
                ORDER BY category
            ) SELECT ROW_NUMBER() OVER (ORDER BY category) AS id, category
            FROM categories;
    """,

    'basic_3_4': """
        ALTER TABLE category 
        ADD PRIMARY KEY (id);
    """,

    'basic_3_5': """
        CREATE TABLE offers_stripped AS
            SELECT id, cluster_id, title, brand, category, description, _sentence
            FROM offers;
    """,

    'basic_3_6': """
        UPDATE offers_stripped os 
        SET category = c.id
        FROM category c
        WHERE os.category = c.category;
    """,

    'basic_3_7': """
        UPDATE offers_stripped os 
        SET brand = b.id
        FROM brand b
        WHERE os.brand = b.brand;
    """,

    'basic_3_8': """
        ALTER TABLE offers_stripped
        ALTER COLUMN brand TYPE bigint USING brand::bigint,
        ALTER COLUMN category TYPE bigint USING category::bigint,
        ADD CONSTRAINT fk_brand FOREIGN KEY (brand) REFERENCES brand(id),
        ADD CONSTRAINT fk_category FOREIGN KEY (category) REFERENCES category(id);
    """,

    'complex_1_1': """
        CREATE OR REPLACE VIEW fords AS 
            SELECT * 
            FROM offers
            WHERE title LIKE '%ford%'
            OR description LIKE '%ford%'
            OR brand LIKE '%ford%';
    """,

    'probabilistic_3_1': """
        CREATE TABLE part_table AS
        SELECT *
        FROM offers 
        LIMIT 100;
    """,

    'probabilistic_4_1': """
        CREATE OR REPLACE VIEW aggregated_sentence AS
            WITH offer_clusters AS (
                SELECT id, cluster_id, title, AGG_OR(_sentence) AS _sentence
                FROM part
                GROUP BY id, cluster_id, title )
            SELECT id, STRING_AGG(CAST(cluster_id AS VARCHAR), ', ') AS occurs_in_clusters, 
                MAX(title) AS title, AGG_OR(_sentence) AS _sentence
            FROM offer_clusters
            GROUP BY id;
    """,

    'probabilistic_5_1': """
        CREATE OR REPLACE VIEW probabilities AS
            SELECT round(prob(d.dict, a._sentence)::NUMERIC, 4) AS probability, a.*
            FROM aggregated_sentence a, _dict d
            WHERE d.name = 'mydict'
            ORDER BY probability DESC; 
    """,

    # TODO: Include the queries for Insert, Update, Delete.

}
