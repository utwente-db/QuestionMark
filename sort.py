import gzip
import json
import time

MAX_INSERT = 50000
ATTRS = ['description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent']  # non key-attributes


def sort_offers(dataset, write_to):
    with gzip.open(dataset) as data:
        offers = []
        total = 0
        for line in data:
            # print(line)
            total += 1
            if total > MAX_INSERT:
                break
            offer = json.loads(line)
            for attribute in ATTRS:  # Only keep BKVs, cluster_id and id of offer.
                offer.pop(attribute)
            offers.append(offer)
        sorted_offers = sorted(offers,
                               key=lambda k: (k['category'] is None, k['category'] == "", k['category'],
                                              k['brand'] is None, k['brand'] == "", k['brand'],
                                              k['title'] is None, k['title'] == "", k['title']))

    with open(write_to, 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, sorted_offers)))


def time_exec(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        sort_offers(dataset)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


if __name__ == '__main__':
    # # #  Sorting the dataset   --> 50 000 records in 710 ms over 50 runs average.
    # # #  The generated dataset should be manually gzipped before use.
    # sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_english_v2_sorted.json')
    sort_offers('datasets/offers_corpus_english_v2_gs.json.gz', 'datasets/offers_corpus_english_v2_gs_sorted.json')
    # time_exec('datasets/offers_corpus_english_v2.json.gz', 50)  # for a timed run.

