import gzip
import hashlib
import json

from aer_matcher import aer_matcher, write_clusters_to_file
from asn_blocker import asn_blocker, write_blocks_to_file
from database_filler import connect_pg, transfer_to_dubio, transfer_to_maybms, close_pg
from parameters import NON_BKV


def resize_insert():
    print('resizing the dataset...')
    all_lines = 0
    included_lines = 0
    with gzip.open('datasets/offers_corpus_english_v2.json.gz') as data:
        smaller_dataset = []
        for line in data:
            all_lines += 1
            offer = json.loads(line)
            id_hash = hashlib.sha256(('a' + str(offer.get('cluster_id'))).encode('utf-8')).hexdigest()
            include = int(id_hash, 16) % 10000
            if include < 1:
                smaller_dataset.append(offer)
                included_lines += 1
        print('total offers count:', all_lines)
        print('included offers count:', included_lines)
        print('Percentage:', (included_lines / all_lines) * 100)

    with open('datasets/insert_offers.json', 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, smaller_dataset)))


def update_ids():
    offers = []
    with open('datasets/insert_offers.json') as offers_file:
        for offer in offers_file:
            offers.append(json.loads(offer))

    for offer in offers:
        offer['id'] = offer.get('id') + 50000000

    with open('datasets/insert_offers.json', 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, offers)))


def offer_by_id():
    print('generating offers by ID dictionary...')
    offers_raw = []
    offers = {}
    with open('datasets/insert_offers.json') as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers_raw.append(json.loads(offer))

    for offer in offers_raw:
        offers[offer.get('id')] = offer

    offers_raw.clear()  # For memory efficiency. Could comment out when space is not an issue.

    # write one line with the whole dict.
    with open('datasets/insert_offers_byID.json', 'w', encoding='utf-8') as file:
        for chunk in json.JSONEncoder().iterencode(offers):
            file.write(chunk)


def sort_offers():
    print('sorting offers...')
    with open('datasets/insert_offers.json') as data:
        offers = []
        total = 0
        for line in data:
            # print(line)
            total += 1
            offer = json.loads(line)
            for attribute in NON_BKV:  # Only keep BKVs, cluster_id and id of offer.
                offer.pop(attribute)
            offers.append(offer)
        sorted_offers = sorted(offers,
                               key=lambda k: (k['title'] is None, k['title'] == "", k['title'],
                                              k['brand'] is None, k['brand'] == "", k['brand'],
                                              k['category'] is None, k['category'] == "", k['category']))

    with open('datasets/insert_offers_sorted.json', 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, sorted_offers)))


def block():
    blocks = asn_blocker('datasets/insert_offers_sorted.json.gz')
    write_blocks_to_file(blocks, 'datasets/asn_blocks_insert')


def match():
    # Need to change the part in aer_matcher where the byID file is read.
    prob_clust, cert_clust = aer_matcher('datasets/asn_blocks_insert')
    write_clusters_to_file(prob_clust, cert_clust, 'datasets/aer_prob_insert', 'datasets/aer_cert_insert')


def create():
    # The following changes were made to transfer_to_x before running:
    # renamed all table instances of 'offer' to 'offer_insert'
    # renamed all table instances of '_dict' to '_dict_insert'
    # cluster_id_start = 2000
    # cluster_id_end = 2000
    # byID dataset changed, removed the gzip part around it.

    connect_pg(configname='database.ini')
    # transfer_to_maybms('datasets/aer_prob_insert', 'datasets/aer_cert_insert')
    transfer_to_dubio('datasets/aer_prob_insert', 'datasets/aer_cert_insert')
    close_pg()


if __name__ == '__main__':
    # resize_insert()
    # update_ids()
    # offer_by_id()
    # sort_offers()
    # block()
    # match()
    create()
