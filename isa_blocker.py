import gzip
import json
import time
import collections

from offer_distance import *

MSL = 3    # Minimum Suffix Length
MBS = 30   # Maximum Block Size
PHI = 0.4  # Suffix Comparison Threshold.


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
        if levenshtein(prev_suffix, suffix) < PHI:
            block = fill_block(block, offers)
        else:
            blocks.append(block)
            block = []
            block = fill_block(block, offers)
        prev_suffix = suffix

    print(blocks)
    return blocks


def time_exec(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        isa_blocker(dataset)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


def debug():
    pass


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking   --> 50 000 records in x ms over 50 runs average.
    isa_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')  # normal execution.
    # time_exec('datasets/offers_corpus_english_v2_sorted.json.gz', 50)  # for a timed run.

    # blocks = isa_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')  # normal execution.
    # print(blocks)

    # debug()

    # print(get_distance('hello', 'hella'))
    # print(get_distance('blabla', 'something'))
