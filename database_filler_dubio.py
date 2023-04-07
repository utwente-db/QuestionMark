import gzip
import json
import math
import sys

from database_filler import execute_query, get_attr_prob, prepare_string_for_insert, load_content, connect_pg, close_pg

# Global Variables
bulk_dict_query = "'"
bulk_insert_query = ""

# This file creates the representation for easy upload in the database.
# This file is an extension of database_filler.py specialised for DuBio.


# Creates the offers database table.
def setup_database_dubio():
    sql = """
        DROP TABLE IF EXISTS _dict; -- must be first, before drop extension
        DROP EXTENSION IF EXISTS pgbdd CASCADE;
        CREATE EXTENSION pgbdd;

        -- create the offers table
        DROP TABLE IF EXISTS offers CASCADE;
        CREATE TABLE offers (
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
            _sentence        BDD 
        );  

        -- create the main dictionary table
        DROP TABLE IF EXISTS _dict CASCADE;
        CREATE TABLE _dict (
            name    VARCHAR(20), 
            dict    dictionary
        );  

        -- create the 'mydict' dictionary
        INSERT INTO _dict(name, dict) VALUES ('mydict', dictionary(''));
        """

    execute_query(sql)


# Bulk inserts multiple offers at once into the created offers table.
def bulk_insert_dubio(query_type):
    sql_dict = "UPDATE _dict SET dict = add(dict, %s) WHERE name = 'mydict';"
    sql_insert = "INSERT INTO offers (id, cluster_id, title, brand, category, description, " \
                 "price, identifiers, keyValuePairs, specTableContent, _sentence) VALUES %s;"

    if query_type == 'dict':
        global bulk_dict_query
        bulk_dict_query += "'"
        execute_query(sql_dict % bulk_dict_query)
        bulk_dict_query = "'"
    elif query_type == 'insert':
        global bulk_insert_query
        bulk_insert_query = bulk_insert_query[:-2]  # as we insert each part with a ', '
        execute_query(sql_insert % bulk_insert_query)
        bulk_insert_query = ""
    else:
        sys.exit("Please input a valid parameter in bulk_insert_dubio(). This is either 'dict' or 'insert'.")


# Returns the Bdd of all offers in a cluster and includes its probability in the dictionary.
def get_bdd_certain(offers, cluster, cluster_id):
    # For now, we assume that one full offer is correct. One could implement a variation where the attributes are
    #    weighted separately resulting in more variables.
    attribute_probabilities = get_attr_prob(offers, cluster)
    bdds = []
    global bulk_dict_query
    if len(cluster) == 1:
        bdds.append("('1')")
    else:
        for i in range(len(cluster)):
            a = 'a%s=%s' % (cluster_id, i)
            bdd = "('%s')" % a
            bdds.append(bdd)
            prob = str(math.floor(attribute_probabilities[i] * 100000) / 100000)  # To floor to 5 decimal places.
            add = a + ':' + prob + ';'  # Otherwise when sum(prob) > 1
            bulk_dict_query += add  # DuBio might crash.

    return bdds


# Generates the values to be put in the dictionary.
def get_bdd_possible(offers, cluster, cluster_id, probabilities, possible_world_number):
    attribute_probabilities = get_attr_prob(offers, cluster)
    bdds = []
    w = 'w%s=%s' % (cluster_id, possible_world_number)
    prob_w = str(math.floor(probabilities[possible_world_number - 1] * 100000) / 100000)
    add = w + ':' + prob_w + ';'
    global bulk_dict_query
    bulk_dict_query += add
    for i in range(len(cluster)):
        a = 'a%sx%s=%s' % (cluster_id, possible_world_number, i)
        bdd = "('%s&%s')" % (w, a)
        bdds.append(bdd)
        prob_a = str(math.floor(attribute_probabilities[i] * 100000) / 100000)
        add = a + ':' + prob_a + ';'
        bulk_dict_query += add
    return bdds


# Creates a single record to be put into the database from an offer.
def create_record_dubio(offers, offer, cluster_id, bdd):
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
        '_sentence': str(bdd)
    })
    return record


# Digests the clusters and puts the offers with the corresponding uncertainty into the database.
def transfer_to_dubio(prob_cluster_file, cert_cluster_file):
    connect_pg(configname='database.ini')  # Connect to the database
    setup_database_dubio()
    print('reading cluster files...')
    prob_clusters, cert_clusters = load_content(prob_cluster_file, cert_cluster_file)
    print('reading offers by ID file...')
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
                    if offer not in cluster:
                        cluster.append(offer)

            # Put all offers not present in the cluster of the possible world in a separate cluster.
            individual_offers = []
            for offer in prob_cluster[0]:
                if offer not in cluster:
                    individual_offers.append(offer)

            bdds = get_bdd_possible(offers, cluster, cluster_id_start, prob_cluster[2], possible_world_number)
            for i in range(len(cluster)):
                record = create_record_dubio(offers, cluster[i], cluster_id, bdds[i])
                records.append(record)

            for i in range(len(individual_offers)):
                cluster_id += 1
                bdd = get_bdd_possible(offers, [individual_offers[i]], cluster_id, prob_cluster[2],
                                       possible_world_number)
                record = create_record_dubio(offers, individual_offers[i], cluster_id, bdd[0])
                records.append(record)

            bulk_insert_dubio('dict')

            if cluster_id > cluster_id_end:
                cluster_id_end = cluster_id

            cluster_id = cluster_id_start

        cluster_id_start = cluster_id_end + 1

    # Continue with the certain clusters.
    cluster_id = cluster_id_end + 1
    cluster_count = 0
    print("\n Processing certain clusters for DuBio \n")
    for cluster in cert_clusters:
        cluster_id += 1
        cluster_count += 1
        bdds = get_bdd_certain(offers, cluster, cluster_id)
        for i in range(len(cluster)):
            record = create_record_dubio(offers, cluster[i], cluster_id, bdds[i])
            records.append(record)
        if cluster_count >= 200:
            bulk_insert_dubio('dict')
            cluster_count = 0

    record_count = 0
    count = 0
    for record in records:
        record_count += 1
        count += 1
        vals = list(record.values())
        global bulk_insert_query
        bulk_insert_query += '( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, Bdd%s ), ' % tuple(vals)
        if record_count >= 1000:
            bulk_insert_dubio('insert')
            print(round((count / len(records) * 100), 2), '% done with inserting offers in DuBio.')
            record_count = 0

    # commit the remaining records
    bulk_insert_dubio('insert')
    print('100 % done with inserting offers in DuBio.')

    close_pg()  # Close connection
