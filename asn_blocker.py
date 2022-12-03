import gzip
import json

from window import Window
from offer_distance import get_distance
from parameters import PHI, WS, MBS


def write_blocks_to_file(blocks, write_to):
    print('blocks created, now writing.')
    with open(write_to, 'w+') as f:
        for block in blocks:
            f.write(str(block))
            f.write('\n')


# Based on the paper of Yan et al. (2007) Adaptive Sorted Neighborhood Methods for Efficient Record Linkage.
def asn_blocker(dataset):
    blocks = []
    offers = []

    window = Window(WS, 0)
    block = []

    print('reading offers file...')

    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers.append(json.loads(offer.decode('utf-8')))

    while window.last < len(offers):
        # enlargement
        dist = get_distance(offers[window.first].get('title'), offers[window.last].get('title'))
        if dist <= PHI:
            if window.last + WS < len(offers):
                window.last += WS
                continue
            else:
                window.last = len(offers)
        if window.last - window.first >= MBS:
            window.last = window.first + MBS - 1
        # retrenchment and create block
        # else:
        for i in range(window.last, window.first - 1, -1):
            dist = get_distance(offers[window.first].get('title'), offers[i].get('title'))
            if dist <= PHI or offers[window.first].get('id') == offers[i].get('id'):
                window.last = i
                for offer in (offers[window.first:window.last + 1]):
                    block.append(offer.get('id'))
                if not block:
                    pass
                    print(window.first, window.last)
                blocks.append(block)
                block = []
                print(round(window.last/(len(offers)) * 100, 2), '% done')
                window.first = i + 1
                window.last = window.first + WS - 1
                break
    return blocks


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    bls = asn_blocker('datasets/offers_corpus_english_v2_gs.json.gz')
    # write_to_file(bls, 'datasets/asn_blocks')
    # write_blocks_to_file(bls, 'datasets/asn_gs_blocks')

    # To measure the performance of this blocking algorithm, use blocker_performance.py
