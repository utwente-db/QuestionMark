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
# Creates blocks with possible clusters from the dataset.
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
        # enlargement phase
        dist = get_distance(offers[window.first].get('title'), offers[window.last].get('title'))
        if dist <= PHI:
            if window.last + WS < len(offers):
                window.last += WS
                continue
            else:
                window.last = len(offers) - 1
        if window.last - window.first >= MBS:
            window.last = window.first + MBS - 1
        # retrenchment phase and create block
        for i in range(window.last, window.first - 1, -1):
            print('len:', len(offers), 'index window:', window.first, 'index i', i)
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
