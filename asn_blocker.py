import gzip
import json
import time

from block import Block
from window import Window
from offer_distance import levenshtein

WZ = 2  # window size
PHI = 0.5  # similarity threshold


# TODO: determine value phi and wz
def asn_blocker(jsonzip):
    blocks = []
    offers = []

    window = Window(WZ, 0)
    block = Block()
    index = 0

    with gzip.open(jsonzip) as offers_file:  # Open the sorted dataset
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
            if levenshtein(offers[block.start].get('title'), offers[window.last].get('title')) <= PHI:
                window.last += WZ
                index += WZ
            # retrenchment and create block
            else:
                for i in range(index, index - WZ - 1, -1):
                    if levenshtein(offers[block.start].get('title'), offers[index].get('title')) <= PHI:
                        block.end = index
                        blocks.append(block)
                        # print(block.start, block.end)
                        block = Block()
                        index += 1
                        window.first = index
                        window.last = window.first + WZ
                        block.start = window.first
                        index += WZ
                        continue
                    index -= 1
    return blocks


def debug(block_s):
    count = 0
    for b in block_s:
        if not b.end == b.start:
            print('block: ', b.start, b.end)
        else:
            count += 1
    print('number of single blocks: ', count)
    return


def time_exec(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        asn_blocker(dataset)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking   --> 50 000 records in 320 ms over 50 runs average.
    asn_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')  # normal execution.
    # time_exec('datasets/offers_corpus_english_v2_sorted.json.gz', 50)  # for a timed run.

    # debug(blocks)
    # print(get_distance('hello', 'hella'))
    # print(get_distance('blabla', 'something'))
