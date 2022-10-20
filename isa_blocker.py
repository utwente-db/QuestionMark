import gzip
import json
import collections
import sys

from offer_distance import levenshtein
from offer_distance import jarowinkler
from parameters import MSL, MBS, PHI, DIST


def get_suffixes(bkv):
    suffixes = []
    if bkv:
        for i in range(len(bkv) - MSL + 1):
            suffixes.append(bkv[i:])
    return suffixes


def fill_block(block, offers):
    for offer in offers:
        if offer not in block:
            block.append(offer)
    return block


# Apply Bloom filters?
# Based on the paper of De Vries et al. (2011) Robust Record Linkage Blocking Using Suffix Arrays and Bloom Filters.
def isa_blocker(dataset):
    blocks = []
    ii = {}  # inverted index

    # index construction
    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for line in offers_file:
            offer = json.loads(line.decode('utf-8'))
            bkv = ((offer.get('category') if offer.get('category') else '') +
                   (offer.get('brand') if offer.get('brand') else '') +
                   (offer.get('title') if offer.get('title') else ''))  # blocking key value
            suffixes = get_suffixes(bkv)
            for suffix in suffixes:
                if suffix not in ii:
                    ii[suffix] = []
                ii[suffix].append(offer.get('id'))

    # large block removal
    to_delete = []
    for suffix in ii:
        if len(ii[suffix]) > MBS:
            to_delete.append(suffix)
    for suffix in to_delete:
        del ii[suffix]

    # suffix grouping
    ord_ii = collections.OrderedDict(sorted(ii.items()))
    prev_suffix = ''
    block = []
    for suffix, offers in ord_ii.items():
        if DIST == 'levenshtein':
            distance = levenshtein(prev_suffix, suffix)
        elif DIST == 'jarowinkler':
            distance = jarowinkler(prev_suffix, suffix)
        else:
            sys.exit("Please input for the parameter DIST in parameters.py either 'levenshtein' or 'jarowinkler'.")
        if distance < PHI:
            block = fill_block(block, offers)
        else:
            blocks.append(block)
            block = []
            block = fill_block(block, offers)
        prev_suffix = suffix

    print(blocks)
    return blocks


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    isa_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')

    # To measure the performance of this blocking algorithm, use blocker_performance.py

    # blocks = isa_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')  # normal execution.
    # print(blocks)
