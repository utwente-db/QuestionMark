import gzip
import json

from offer_distance import get_distance
from parameters import ATTRIBUTES, WEIGHTS, LOWER_PHI, UPPER_PHI

# TODO: allow for different similarity measure for each attribute.


def aer_matcher(blocks_file):
    # Get blocks from file.
    blocks = []
    with open(blocks_file) as file:
        for block in file:
            if block == '[]\n':
                continue
            else:
                block = block.strip('\n').strip('][').split(', ')
                block = list(map(int, block))
                blocks.append(block)

    # Get all offer information from file.
    dataset = 'datasets/offers_corpus_english_v2_gs_sorted.json.gz'
    offers_raw = []
    offers = {}
    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for offer in offers_file:
            offers_raw.append(json.loads(offer.decode('utf-8')))

    for offer in offers_raw:
        offers[offer.get('id')] = offer

    offers_raw.clear()  # For space efficiency. Could comment out when space is not a problem.

    # Get a distance measure for all attributes
    block_matches = []
    for block in blocks:
        matching_scores = {}
        if len(block) == 1:
            continue
        for i in range(len(block)):
            for j in range(i + 1, len(block)):
                matching_scores[(block[i], block[j])] = []
                offer_i, offer_j = offers.get(block[i]), offers.get(block[j])
                for k in range(len(ATTRIBUTES)):
                    distance = get_distance(offer_i.get(ATTRIBUTES[k]), offer_j.get(ATTRIBUTES[k]))
                    matching_scores[(block[i], block[j])].append(distance * WEIGHTS[k])

        block_matches.append(matching_scores)

    # Calculate the similarity phi between two records.
    block_scores = []
    for block in block_matches:
        block_score = {}
        for pair, scores in block.items():
            phi = 0
            count = 0
            for score in scores:
                if score == 1:  # Exclude scores from one or multiple NULL values.
                    pass
                else:
                    phi += score
                    count += 1
            if count == 0:
                phi = 1
            else:
                phi = round(phi / count, 2)
            block_score[pair] = phi
        block_scores.append(block_score)

    block_matches.clear()  # For space efficiency. Could comment out when space is not a problem.

    # Continue to probabilistic matching.


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    aer_matcher('datasets/asn_gs_blocks')  # normal execution.
