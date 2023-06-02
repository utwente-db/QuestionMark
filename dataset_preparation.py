import gzip
import hashlib
import json

from parameters import DATASET_SIZE, NON_BKV, WHOLE_CLUSTERS


# Resize the dataset pseudo-randomly.
def resize_dataset(dataset, write_to):
    print(' Resizing the dataset...')
    all_lines = 0
    included_lines = 0
    with gzip.open(dataset) as data:
        smaller_dataset = []
        for line in data:
            all_lines += 1
            offer = json.loads(line)
            # Create a hash of the offer_id, so we can pseudo-randomly include an offer or exclude it.
            # This ensures that the same 'random' selection is made each time this function is run.
            if WHOLE_CLUSTERS:
                id_hash = hashlib.sha256(str(offer.get('cluster_id')).encode('utf-8')).hexdigest()
            else:
                id_hash = hashlib.sha256(str(offer.get('id')).encode('utf-8')).hexdigest()
            include = int(id_hash, 16) % 10000
            if include < (DATASET_SIZE * 100):
                smaller_dataset.append(offer)
                included_lines += 1
        print(' Total offers count:', all_lines)
        print(' Included offers count:', included_lines)
        print(' Percentage:', (included_lines / all_lines) * 100)

    with open(write_to, 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, smaller_dataset)))


# Sort offers, keep the original data structure.
def sort_offers(dataset, write_to):
    print('\n Sorting offers...')
    with gzip.open(dataset) as data:
        offers = []
        total = 0
        for line in data:
            total += 1
            offer = json.loads(line)
            for attribute in NON_BKV:  # Only keep BKVs, cluster_id and id of offer.
                offer.pop(attribute)
            offers.append(offer)
        sorted_offers = sorted(offers,  # Changing the order of sorting impacts the performance.
                               key=lambda k: (k['title'] is None, k['title'] == "", k['title'],
                                              k['brand'] is None, k['brand'] == "", k['brand'],
                                              k['category'] is None, k['category'] == "", k['category']))

    with open(write_to, 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, sorted_offers)))


# For improved lookup speed. Type of offers: {offer_id: {'title': ..., 'id': ..., ...}, ...}.
def offer_by_id(dataset, write_to):
    print(' Generating offers by ID dictionary...')
    offers_raw = []
    offers = {}
    with gzip.open(dataset) as offers_file:
        for offer in offers_file:
            offers_raw.append(json.loads(offer.decode('utf-8')))

    for offer in offers_raw:
        offers[offer.get('id')] = offer

    offers_raw.clear()  # For memory efficiency. Could comment out when space is not an issue.

    # write one line with the whole dict.
    with open(write_to, 'w', encoding='utf-8') as file:
        for chunk in json.JSONEncoder().iterencode(offers):
            file.write(chunk)
