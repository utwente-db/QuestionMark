import gzip
import json
import math

from database_filler import execute_query, prepare_string_for_insert, load_content, get_attr_prob, connect_pg, close_pg

# Global Variables
bulk_dict_query = "'"
bulk_insert_query = ""

# This file creates the representation for easy upload in the database.
# This file is an extension of database_filler.py specialised for DuBio.


# Creates the offers database table.
def setup_database_maybms():
    sql = """
        DROP TABLE IF EXISTS offers_setup CASCADE;
        DROP TABLE IF EXISTS offers_rk_world CASCADE; 
        DROP TABLE IF EXISTS offers_rk_attrs CASCADE; 
        DROP TABLE IF EXISTS offers CASCADE;
        CREATE TABLE offers_setup (
            id               BIGINT,
            cluster_id       BIGINT,
            title            TEXT   DEFAULT NULL,
            brand            TEXT   DEFAULT NULL,
            category         TEXT   DEFAULT NULL,
            description      TEXT   DEFAULT NULL,
            price            TEXT   DEFAULT NULL,
            identifiers      TEXT   DEFAULT NULL,
            keyValuePairs    TEXT   DEFAULT NULL,
            specTableContent TEXT   DEFAULT NULL,
            world_prob       FLOAT DEFAULT 1,
            attribute_prob   FLOAT DEFAULT 1
        );
    """

    execute_query(sql)


# Bulk inserts multiple offers at once into the created offers table.
def bulk_insert_maybms():
    sql_insert = "INSERT INTO offers_setup (id, cluster_id, title, brand, category, description, price, " \
                 "identifiers, keyValuePairs, specTableContent, world_prob, attribute_prob) VALUES %s;"

    global bulk_insert_query
    bulk_insert_query = bulk_insert_query[:-2]  # as we insert each part with a ', '
    execute_query(sql_insert % bulk_insert_query)
    bulk_insert_query = ""


# Creates a single record to be put into the database from an offer.
def create_record_maybms(offers, offer, cluster_id, probability_world, probability_attribute):
    record = {}
    offer_info = offers.get(str(offer))
    record.update({
        'id': offer,
        'cluster_id': cluster_id,
        'title': prepare_string_for_insert(offer_info.get('title')),
        'brand': prepare_string_for_insert(offer_info.get('brand')),
        'category': prepare_string_for_insert(offer_info.get('category')),
        'description': prepare_string_for_insert(offer_info.get('description')),
        'price': prepare_string_for_insert(offer_info.get('price')),
        'identifiers': prepare_string_for_insert(offer_info.get('identifiers')),
        'keyValuePairs': prepare_string_for_insert(offer_info.get('keyValuePairs')),
        'specTableContent': prepare_string_for_insert(offer_info.get('specTableContent')),
        'world_prob': probability_world,
        'attribute_prob': probability_attribute,
    })
    return record


# Digests the clusters and puts the offers with the corresponding uncertainty into the database.
def transfer_to_maybms(prob_cluster_file, cert_cluster_file):
    connect_pg(configname='database.ini')  # Connect to the database
    setup_database_maybms()
    print('reading cluster file...')
    prob_clusters, cert_clusters = load_content(prob_cluster_file, cert_cluster_file)
    print('reading offers by ID file... \n')
    with gzip.open('datasets/offers_corpus_byID.json.gz', 'r') as id_file:
        offers = json.loads(id_file.read())
    records = []  # Each record becomes a row in the database.
    cluster_id_start = 1
    cluster_id_end = 1

    count = 0
    for prob_cluster in prob_clusters:  # type prob_cluster:  [ [offers], [(possible_world), ...], [probabilities] ]
        count += 1
        print(round((count / len(prob_clusters) * 100), 2), '% done with processing probabilistic clusters.')
        cluster_id = cluster_id_start
        possible_world_number = 0
        for possible_world in prob_cluster[1]:  # type possible_world: ([offer_id, offer_id], ...)
            possible_world_number += 1
            cluster = []
            for products in possible_world:  # only clustered offers are presented.
                for offer in products:
                    if offer in products:
                        if offer not in cluster:
                            cluster.append(offer)

            # Put all offers not present in the cluster of the possible world in a separate cluster.
            individual_offers = []
            for offer in prob_cluster[0]:
                if offer not in cluster:
                    individual_offers.append(offer)

            probability_attributes = get_attr_prob(offers, cluster)
            probability_world = str(math.floor(prob_cluster[2][possible_world_number - 1] * 100000) / 100000)
            for i in range(len(cluster)):
                record = create_record_maybms(offers, cluster[i], cluster_id, probability_world, probability_attributes[i])
                records.append(record)

            for i in range(len(individual_offers)):
                cluster_id += 1
                record = create_record_maybms(offers, individual_offers[i], cluster_id, 1, 1)
                records.append(record)

            if cluster_id > cluster_id_end:
                cluster_id_end = cluster_id

            cluster_id = cluster_id_start

        cluster_id_start = cluster_id_end + 1

    # Continue with certain clusters.
    cluster_id = cluster_id_end + 1
    cluster_count = 0
    print("\n Processing certain clusters for MayBMS \n")
    for cluster in cert_clusters:
        cluster_id += 1
        cluster_count += 1
        probability_attributes = get_attr_prob(offers, cluster)
        for i in range(len(cluster)):
            record = create_record_maybms(offers, cluster[i], cluster_id, 1, probability_attributes[i])
            records.append(record)

    record_count = 0
    count = 0
    for record in records:
        record_count += 1
        count += 1
        vals = list(record.values())
        global bulk_insert_query
        bulk_insert_query += '( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ), ' % tuple(vals)
        if record_count >= 1000:
            bulk_insert_maybms()
            print(round((count / len(records) * 100), 2), '% done with inserting offers in MayBMS.')
            record_count = 0

    # commit the remaining records
    bulk_insert_maybms()
    print('100 % done with inserting offers in MayBMS.')

    # To generate a probability space over two attributes, first two tables need to be created with each a probability
    #     space over a single attribute. Next, these tables can be merged.
    print('\n Making the offers table probabilistic ...')
    query = """ CREATE TABLE offers_rk_world AS REPAIR KEY cluster_id IN offers_setup WEIGHT BY world_prob;  """
    execute_query(query)
    print(' 40% done ...')
    query = """ CREATE TABLE offers_rk_attrs AS REPAIR KEY id IN offers_setup WEIGHT BY attribute_prob;  """
    execute_query(query)
    print(' 80% done ...')
    query = """ CREATE TABLE offers AS (
                    SELECT attrs.* 
                    FROM offers_rk_attrs AS attrs, offers_rk_world AS world
                    WHERE attrs.id = world.id 
                );
            """
    execute_query(query)
    print(' 100% done')

    close_pg()  # Close connection
