#
# This file creates two new datasets from the golden standard dataset all_gs.json:
# -- A dataset in the structure of offers_corpus_english_v2.json. This is written to a file.
# -- A dataset containing an easy-to-access list of all matches and non-matches of the included product offers.
# This way, the golden standard can be processed and the performance of the blocking and matching can be determined.
#

import gzip
import json


def create_dataset(gold_standard):
    offers = []
    with gzip.open(gold_standard) as gs_file:  # Open the sorted dataset
        for line in gs_file:
            offer_duo = json.loads(line)
            offer_left = {}
            offer_right = {}
            for key in offer_duo:
                if 'left' in key:
                    offer_left[key.rstrip("left").rstrip("_")] = offer_duo[key]
                if 'right' in key:
                    offer_right[key.rstrip('right').rstrip('_')] = offer_duo[key]
            offers.append(offer_left)
            offers.append(offer_right)

    # There is a total of 4113 duplicates in the raw offers list. These get removed here.
    offers_unique = []
    ids = []
    for offer in offers:
        if offer['id'] not in ids:
            offers_unique.append(offer)
            ids.append(offer['id'])

    # Write unique offers in the golden standard to file.
    with open('datasets/offers_corpus_gs.json', 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, offers_unique)))


def get_matches(gold_standard):
    matches = {}
    mismatches = {}

    with gzip.open(gold_standard) as gs_file:  # Open the sorted dataset
        for line in gs_file:
            offer_duo = json.loads(line)

            if offer_duo.get('label') == '1':  # label == 1 means the two offers represent the same real-world entity.
                if offer_duo.get('id_left') not in matches:
                    matches[offer_duo.get('id_left')] = []
                matches[offer_duo.get('id_left')].append(offer_duo.get('id_right'))
                if offer_duo.get('id_right') not in matches:
                    matches[offer_duo.get('id_right')] = []
                matches[offer_duo.get('id_right')].append(offer_duo.get('id_left'))
            else:  # label == 0. No other case exists. No failsafe required.
                if offer_duo.get('id_left') not in mismatches:
                    mismatches[offer_duo.get('id_left')] = []
                mismatches[offer_duo.get('id_left')].append(offer_duo.get('id_right'))
                if offer_duo.get('id_right') not in mismatches:
                    mismatches[offer_duo.get('id_right')] = []
                mismatches[offer_duo.get('id_right')].append(offer_duo.get('id_left'))
    return matches, mismatches
