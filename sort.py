import gzip
import json

from parameters import MAX_INSERT, NON_BKV


# Sort offers, keep the original data structure.
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
            for attribute in NON_BKV:  # Only keep BKVs, cluster_id and id of offer.
                offer.pop(attribute)
            offers.append(offer)
        sorted_offers = sorted(offers,
                               key=lambda k: (  # k['category'] is None, k['category'] == "", k['category'],
                                                # k['brand'] is None, k['brand'] == "", k['brand'],
                                              k['title'] is None, k['title'] == "", k['title']))

    with open(write_to, 'w', encoding='utf-8') as file:
        file.write('%s' % '\n'.join(map(json.dumps, sorted_offers)))


# For improved lookup speed. Type of offers: {offer_id: {'title': ..., 'id': ..., ...}, ...}.
def sort_offer_by_id(dataset, write_to):
    offers_raw = []
    offers = {}
    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers_raw.append(json.loads(offer.decode('utf-8')))

    for offer in offers_raw:
        offers[offer.get('id')] = offer

    offers_raw.clear()  # For memory efficiency. Could comment out when space is not an issue.

    # write one line with the whole dict.
    with open(write_to, 'w', encoding='utf-8') as file:
        file.write('%s' % ''.join(map(json.dumps, offers)))
    # with open(write_to, 'w', encoding='utf-8') as file:
    #     for chunk in json.JSONEncoder().iterencode(offers):
    #         file.write(chunk)


if __name__ == '__main__':
    # # #  Sorting the dataset   --> 50 000 records in 710 ms over 50 runs average.
    # # #  NOTE: The generated dataset should be manually gzipped before use.

    sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_english_v2_sorted.json')
    # sort_offers('datasets/offers_corpus_english_v2_gs.json.gz',
    #             'datasets/offers_corpus_english_v2_gs_sorted_test.json')
    # sort_offers('datasets/offers_corpus_english_v2_gs_50p.json.gz',
    #             'datasets/offers_corpus_english_v2_gs_50p_sorted.json')
    # sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_english_v2_20k_sorted.json')

    # sort_offer_by_id('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_english_v2_byID.json')

