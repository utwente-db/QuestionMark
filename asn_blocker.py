import gzip
import json
import sys

from window import Window
from offer_distance import *
from parameters import PHI, WS, DIST


def write_to_file(blocks, file):
    with open(file, 'w+') as f:
        for block in blocks:
            # if not block:
            #     pass
            # else:
            f.write(str(block))
            f.write('\n')


def get_distance(word1, word2):
    if DIST == 'levenshtein':
        return levenshtein(word1, word2)
    elif DIST == 'jarowinkler':
        return jarowinkler(word1, word2)
    elif DIST == 'hamming':
        return hamming(word1, word2)
    elif DIST == 'jaccard':
        return jaccard(word1, word2)
    else:
        sys.exit("Please input a valid value for DIST in parameters.py.")


# Based on the paper of Yan et al. (2007) Adaptive Sorted Neighborhood Methods for Efficient Record Linkage.
def asn_blocker(dataset):
    blocks = []
    offers = []

    window = Window(WS, 0)
    block = []
    index = 0

    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers.append(json.loads(offer.decode('utf-8')))

    while window.last < len(offers):
        # enlargement
        dist = get_distance(offers[window.first].get('title'), offers[window.last].get('title'))
        if dist <= PHI:
            if window.last + WS < len(offers):
                window.last += WS
            else:
                window.last = len(offers) - 1
        # retrenchment and create block
        else:
            for i in range(window.last, window.first - 1, -1):
                dist = get_distance(offers[window.first].get('title'), offers[i].get('title'))
                if dist <= PHI:
                    window.last = i
                    for offer in (offers[window.first:window.last + 1]):
                        block.append(offer.get('id'))
                    if not block:
                        pass
                        print(window.first, window.last)
                    blocks.append(block)
                    block = []
                    window.first = i + 1
                    window.last = window.first + WS - 1
                    break
    return blocks


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    bls = asn_blocker('datasets/offers_corpus_english_v2_gs_sorted.json.gz')  # normal execution.
    # bls = asn_blocker('datasets/offers_corpus_english_v2_sorted_small.json.gz')  # normal execution.
    write_to_file(bls, 'datasets/asn_gs_blocks')

    # To measure the performance of this blocking algorithm, use blocker_performance.py

    # Used to debug the code
    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    l5 = 0
    l6 = 0
    lengths = {}
    for blk in bls:
        if len(blk) == 1:
            l1 += 1
        elif len(blk) == 2:
            l2 += 1
        elif len(blk) == 3:
            l3 += 1
        elif len(blk) == 4:
            l4 += 1
        elif len(blk) == 5:
            l5 += 1
        else:
            l6 += 1
    print(l1, l2, l3, l4, l5, l6)



