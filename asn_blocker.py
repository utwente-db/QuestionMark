import gzip
import json
import sys

from window import Window
from offer_distance import *
from parameters import PHI, WS, DIST


def get_blocks(blocks):
    blocks_filled: {}
    for block in blocks:
        for offer in range(block.start, block.end):
            pass


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

    while index < len(offers):

        # if index >= 500:  # debugging purposes
        #   debug()

        if index < window.last:  # There is still a bug in the code, but this part fixes that bug.
            # print('should not occur', window.last, index)
            index = window.last
        else:
            # enlargement
            dist = get_distance(offers[window.first].get('title'), offers[window.last].get('title'))
            if dist <= PHI:
                window.last += WS
                index += WS
            # retrenchment and create block
            else:
                for i in range(index, index - WS - 1, -1):
                    dist = get_distance(offers[window.first].get('title'), offers[index].get('title'))
                    if dist <= PHI:
                        for offer in (offers[window.first:window.last + 1]):
                            block.append(offer.get('id'))
                        blocks.append(block)
                        block = []
                        index += 1
                        window.first = index
                        window.last = window.first + WS
                        index += WS
                        continue
                    index -= 1
    return blocks


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    asn_blocker('datasets/offers_corpus_english_v2_sorted_small.json.gz')  # normal execution.

    # To measure the performance of this blocking algorithm, use blocker_performance.py



