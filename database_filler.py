# (optional addition) create multiple clusters if a possible world indicates this might be the case.
# (optional addition) allow for probabilities per attribute, creating new offers with a mix of attributes.

# Creates representation for easy upload in the database.
# This file contains functions shared by both MayBMS and DuBio.
# In case a new DBMS needs to be supported, please check what is of relevance and adapt where needed.

import pickle
from configparser import ConfigParser

import psycopg2

from offer_distance import get_distance
from parameters import ATTRIBUTES, WEIGHTS

conn_pg = None

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


# ======  General Functions =========================================================================================
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


# Do some data preparation, else PostgreSQL will throw errors.
def prepare_string_for_insert(value):
    if not value:
        return "'" + str(value) + "'"  # probably None, return this.
    else:  # For PostgreSQL to be able to read the strings, we escape the single quotes and remove double quotes.
        value = str(value)
        value = value.replace('"', "''")
        value = value.replace("'", "''")
        value = "'" + value + "'"  # And wrap it in a string.
    return value
