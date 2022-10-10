import gzip
import json
import time

from block import Block
from window import Window

ATTRS = ['description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent']  # non key-attributes
WZ = 5  # window size
MAX_INSERT = 50000


def offer_dist(first, last):
    return 0.5


def binary_comparison():
    return 0.6


def sort_offers(jsonzip):

    with gzip.open(jsonzip) as data:
        offers = []
        total = 0
        for line in data:
            total += 1
            if total > 50000:
                break
            offer = json.loads(line)
            for attribute in ATTRS:  # Only keep BKV, cluster_id and id of offer.
                offer.pop(attribute)
            offers.append(offer)
        sorted_offers = sorted(offers,
                               key=lambda k: (k['title'] is None, k['title'] == "", k['title'],
                                              k['brand'] is None, k['brand'] == "", k['brand'],
                                              k['category'] is None, k['category'] == "", k['category'],))

    with open('offers_corpus_english_v2_sorted_title.json', 'w') as file:
        file.write('%s' % '\n'.join(map(json.dumps, sorted_offers)))


def get_sorted_offers(jsonzip):
    with gzip.open(jsonzip) as data:
        return data


# TODO: implement offer_dist()
# TODO: implement binary_comparison()
# TODO: determine value phi
def blocker(jsonzip):
    offers = get_sorted_offers(jsonzip)

    window = Window(WZ, 0)
    block = Block()

    n       = block.length  # number of record in our block
    phi     = 0.75          # similarity threshold

    while (window.last()) < n:
        block = offers[window.current]

        # enlargement phase
        while offer_dist(offers[window.current], offers[window.last()]) <= phi:
            window.current += window.size

        # retrenchment phase
        while window.size > WZ:
            binary_comparison()

        block.save_end(window.last())
        window.size = WZ
        window.current += (window.size + 1)

    # block.content =


if __name__ == '__main__':
    st = time.time()  # start time
    sort_offers('./offers_corpus_english_v2.json.gz')
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
