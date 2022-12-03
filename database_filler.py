# TODO: (optional) create multiple clusters if a possible world indicates this might be the case.
# TODO: (optional) allow for probabilities per attribute, creating new offers with a mix of attributes.

# Create representation for easy upload in the database.

import gzip
import json
import math
import pickle
import sys
from configparser import ConfigParser

import psycopg2

from offer_distance import get_distance
from parameters import ATTRIBUTES, WEIGHTS

conn_pg = None
bulk_dict_query = "'"
bulk_insert_query = ""


def load_content(prob_cluster_file, cert_cluster_file):
    with open(prob_cluster_file, 'rb') as file:
        prob_clusters = pickle.load(file)
    with open(cert_cluster_file, 'rb') as file:
        cert_clusters = pickle.load(file)
    return prob_clusters, cert_clusters


# ======  Connect to Database =======================================================================================
# This part is copied and adapted from https://github.com/utwente-dmb/wdc_pdb

def config(configname='database.ini', section='postgresql'):
    parser = ConfigParser()  # create a parser
    parser.read(configname)  # read config file

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, configname))

    return db


def connect_pg(configname='database.ini'):
    # Connect to the PostgreSQL database server
    try:
        # read connection parameters
        params = config(configname=configname)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        global conn_pg
        conn_pg = psycopg2.connect(**params)

        # create a cursor
        cur = conn_pg.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)
        exit()  # pretty fatal


def close_pg():
    """ Close connection to the PostgreSQL database server """
    global conn_pg
    try:
        if conn_pg is not None:
            conn_pg.close()
            print('\n Database connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)


def execute_query(query):
    global conn_pg
    try:
        cur = conn_pg.cursor()
        cur.execute(query)
        cur.close()
        conn_pg.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error:', error)


# ======  MayBMS  ===================================================================================================

def transfer_to_maybms(prob_cluster_file, cert_cluster_file):
    prob_clusters, cert_clusters = load_content(prob_cluster_file, cert_cluster_file)
    print('reading offers by ID file... \n')
    with gzip.open('datasets/offers_corpus_english_v2_gs_byID.json.gz', 'r') as id_file:
        offers = json.loads(id_file.read())
    records = []  # Each record becomes a row in the database.
    cluster_id = 0
    for cluster in prob_clusters:
        cluster_id += 1
        # This cluster is a probabilistic one, as it contains a world_graph representation.
        if isinstance(cluster[0], list):
            pass

        # This cluster is a certain one.
        else:
            pass


# ======  DuBio  ====================================================================================================

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


# Get some kind of measure on the likelihood of each attribute value combination.
# Gets the list of offers in a cluster, returns their attribute probability.
def get_attr_prob(offers, cluster):
    if len(cluster) == 1:
        return [1]
    elif len(cluster) == 2:  # We assume that we have no additional information when there are only two products.
        return [0.5, 0.5]
    else:  # A probability is defined based on the distance of the offers within the cluster.
        # First, as with the matching phase, create a comparison vector
        matching_scores = {}
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                offer_i, offer_j = offers.get(str(cluster[i])), offers.get(str(cluster[j]))
                matching_scores[(cluster[i], cluster[j])] = []
                for k in range(len(ATTRIBUTES)):
                    distance = get_distance(str(offer_i.get(ATTRIBUTES[k])),
                                            str(offer_j.get(ATTRIBUTES[k])))
                    matching_scores[(cluster[i], cluster[j])].append(distance * WEIGHTS[k])

        # Then we obtain a single score from combining the vector.
        block_score = {}
        for pair, scores in matching_scores.items():
            phi = 0
            count = 0
            for score in scores:
                if score == 1:  # Exclude scores from one or multiple NULL values.
                    pass
                else:
                    phi += score
                    count += 1
            if count == 0:
                phi = 1
            else:
                phi = round(phi / count, 2)

            block_score[pair] = phi

        # Finally, a probability is calculated using the average distance of an offer to all other offers
        #     and normalising this.
        probabilities = []
        for offer in cluster:
            offer_probability_raw = 0
            count = 0
            for key, value in block_score.items():
                if offer in key:
                    count += 1
                    offer_probability_raw += value
            offer_probability_raw = 1 - (offer_probability_raw / count)  # Low distance = high probability.
            probabilities.append(offer_probability_raw)

        raw_prob_sum = sum(probabilities)
        for i in range(len(probabilities)):
            probabilities[i] = probabilities[i] / raw_prob_sum

        return probabilities


# Returns the Bdd of all offers in a cluster and includes its probability in the dictionary.
def get_bdd_certain(offers, cluster, cluster_id):
    # For now, we assume that one full offer is correct. One could implement a variation where the attributes are
    #    weighted separately resulting in more variables.
    attribute_probabilities = get_attr_prob(offers, cluster)
    bdds = []
    w = 'w%s=1' % cluster_id
    add = w + ':1;'
    global bulk_dict_query
    bulk_dict_query += add
    for i in range(len(cluster)):
        a = 'a%s=%s' % (cluster_id, i)
        bdd = "('%s&%s')" % (w, a)
        bdds.append(bdd)
        prob = str(math.floor(attribute_probabilities[i] * 100000) / 100000)    # To floor to 5 decimal places.
        add = a + ':' + prob + ';'                                              # Otherwise when sum(prob) > 1
        bulk_dict_query += add                                                  # DuBio might crash.

    return bdds


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


def prepare_string_for_insert(value):
    if not value:
        return "'" + str(value) + "'"  # probably None, return this.
    else:  # For PostgreSQL to be able to read the strings, we escape the single quotes and remove double quotes.
        value = str(value)
        value = value.replace('"', "''")
        value = value.replace("'", "''")
        value = "'" + value + "'"  # And wrap it in a string.
    return value


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


def transfer_to_dubio(prob_cluster_file, cert_cluster_file):
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
        print(round((count / len(prob_clusters)*100), 2), '% done with processing probabilistic clusters.')
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
                bdd = get_bdd_possible(offers, [individual_offers[i]], cluster_id, prob_cluster[2], possible_world_number)
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
    print("\n Inserting dictionary values to DuBio... \n")
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


def debug():
    pass


if __name__ == '__main__':
    # connect_pg(configname='database.ini')
    # # transfer_to_maybms('datasets/aer_clusters_prob', 'datasets/aer_clusters_cert')
    # transfer_to_dubio('datasets/aer_clusters_prob', 'datasets/aer_clusters_cert')
    # close_pg()

    debug()
