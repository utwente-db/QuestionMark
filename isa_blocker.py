import gzip
import json
import time

from Levenshtein import distance


def isa_blocker(jsonzip):
    offers = []

    with gzip.open(jsonzip) as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers.append(json.loads(offer.decode('utf-8')))


def time_exec(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        isa_blocker(dataset)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking   --> 50 000 records in x ms over 50 runs average.
    isa_blocker('datasets/offers_corpus_english_v2_sorted.json.gz')  # normal execution.
    # time_exec('datasets/offers_corpus_english_v2_sorted.json.gz', 50)  # for a timed run.

    # debug(blocks)
    # print(get_distance('hello', 'hella'))
    # print(get_distance('blabla', 'something'))
