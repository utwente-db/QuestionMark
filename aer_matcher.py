import gzip
import json

from offer_distance import get_distance
from parameters import ATTRIBUTES, WEIGHTS, LOWER_PHI, UPPER_PHI
from world_graph import WorldGraph


# TODO: allow for different similarity measure for each attribute.


def aer_matcher(blocks_file):
    # Get blocks from file. Type of blocks: [[offer_id, ...], ...]
    blocks = []
    with open(blocks_file) as file:
        count = 0
        for block in file:
            count += 1
            block = block.strip('\n').strip('][').split(', ')
            block = list(map(int, block))
            blocks.append(block)
            if count > 5:
                break

    # Get all offer information from file. Type of offers: {offer_id: {'title': ..., 'id': ..., ...}, ...}
    with gzip.open('datasets/offers_corpus_english_v2_gs_byID.json.gz', 'r') as id_file:
        offers = json.loads(id_file.read())

    # Generate comparison vector. Type of block_matches: [{(offer_id_1, offer_id_2): [dist_float, ...], ...}, {...}]
    clusters = []
    block_matches = []
    for block in blocks:
        matching_scores = {}
        if len(block) == 1:
            clusters.append(block)
            continue
        for i in range(len(block)):
            for j in range(i + 1, len(block)):
                if block[i] < block[j]:
                    matching_scores[(block[i], block[j])] = []
                else:
                    matching_scores[(block[j], block[i])] = []
                offer_i, offer_j = offers.get(str(block[i])), offers.get(str(block[j]))
                for k in range(len(ATTRIBUTES)):
                    distance = get_distance(str(offer_i.get(ATTRIBUTES[k])), str(offer_j.get(ATTRIBUTES[k])))
                    if block[i] < block[j]:
                        matching_scores[(block[i], block[j])].append(distance * WEIGHTS[k])
                    else:
                        matching_scores[(block[j], block[i])].append(distance * WEIGHTS[k])

        block_matches.append(matching_scores)

    # Input vector into decision model. Type of block_scores: [{(offer_id_1, offer_id_2): float, ...}, ...]
    block_scores = []  # matching graph?
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

            # Give full certainty to edges above/below the upper/lower phi.
            if phi <= LOWER_PHI:
                phi = 0
            elif phi >= UPPER_PHI:
                phi = 1
            block_score[pair] = phi
        block_scores.append(block_score)

    block_matches.clear()  # For space efficiency. Could comment out when space is not a problem.

    # Creation of World Graphs.
    world_graphs_clusters = []
    for matching_graph in block_scores:
        tuple_count = 0
        for probability in matching_graph.values():
            tuple_count += 1
            if 0 < probability < 1:
                world_graphs = WorldGraph(matching_graph)
                world_graphs_clusters.append(world_graphs.get_representation())
                break
            if tuple_count == len(matching_graph):
                cluster = []
                for (offer1, offer2) in matching_graph.keys():
                    if offer1 not in cluster:
                        cluster.append(offer1)
                    if offer2 not in cluster:
                        cluster.append(offer2)
                clusters.append(cluster)
                print('clusters', clusters)

    print(world_graphs_clusters)
    return world_graphs_clusters


if __name__ == '__main__':
    # # #  Attribute-based Entity Resolution
    aer_matcher('datasets/asn_gs_blocks')  # normal execution.
