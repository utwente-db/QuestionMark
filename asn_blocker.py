import gzip
import json

from window import Window
from offer_distance import get_distance
from parameters import PHI, WS


def write_to_file(blocks, file):
    with open(file, 'w+') as f:
        for block in blocks:
            f.write(str(block))
            f.write('\n')


# Based on the paper of Yan et al. (2007) Adaptive Sorted Neighborhood Methods for Efficient Record Linkage.
def asn_blocker(dataset):
    blocks = []
    offers = []

    window = Window(WS, 0)
    block = []

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
    bls = asn_blocker('datasets/offers_corpus_english_v2_gs.json.gz')
    # write_to_file(bls, 'datasets/asn_blocks')
    write_to_file(bls, 'datasets/asn_gs_blocks')

    # To measure the performance of this blocking algorithm, use blocker_performance.py
