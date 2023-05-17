# (optional addition) allow for different similarity measure for each attribute.

import gzip
import json
import pickle
from math import floor

from offer_distance import get_distance
from parameters import ATTRIBUTES, WEIGHTS, LOWER_PHI, UPPER_PHI
from world_graph import WorldGraph

progress_percentage = 0


def print_progress(count, length):
    global progress_percentage
    percentage_done = round((count / length * 100), 2)
    if floor(percentage_done) >= floor(progress_percentage) + 5:
        progress_percentage = floor(percentage_done)
        print(floor(percentage_done), '% done with creating world graphs for uncertain clusters...')


def write_clusters_to_file(prob_clusters, cert_clusters, write_to_prob, write_to_cert):
    print('clusters created, now writing...')
    with open(write_to_prob, 'wb') as file:
        pickle.dump(prob_clusters, file)
    with open(write_to_cert, 'wb') as file:
        pickle.dump(cert_clusters, file)


# Based on the paper of Bhattacharya and Getoor (2007). Collective entity resolution in relational data.
#       --> Attribute-Based Entity Resolution Matching Algorithm.
# Creates the final clustering for the dataset.
def aer_matcher(blocks_file, performance=False):  # Use different byID file for a performance run.
    # Get blocks from file. Type of blocks: [[offer_id, ...], ...]
    blocks = []
    print('reading blocks file...')
    with open(blocks_file) as file:
        for block in file:
            block = block.strip('\n').strip('][').split(', ')
            block = list(map(int, block))
            blocks.append(block)

    # Get all offer information from file. Type of offers: {offer_id: {'title': ..., 'id': ..., ...}, ...}
    print('reading offers by ID file...')
    if performance:
        with gzip.open('datasets/offers_gs_byID.json.gz', 'r') as id_file:
            offers = json.loads(id_file.read())
    else:
        with gzip.open('datasets/offers_corpus_byID.json.gz', 'r') as id_file:
            offers = json.loads(id_file.read())

    # Generate comparison vector. Type of block_matches: [{(offer_id_1, offer_id_2): [dist_float, ...], ...}, {...}]
    # For each offer combination in a block we return the distance per attribute. (from 0 to 1)
    cert_clusters = []
    block_matches = []
    count = 0
    print('Generating comparison vectors...')
    for block in blocks:
        count += 1
        matching_scores = {}
        if len(block) == 1:
            cert_clusters.append(block)
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
    # The individual distances get combined to a single distance score. The weight of each attribute can be changed.
    print('Putting vectors in decision model...')
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

    # Creation of World Graphs. Each block is fed to the WorldGraph class.
    world_graphs_clusters = []
    count = 0
    for matching_graph in block_scores:
        count += 1
        print_progress(count, len(block_scores))
        created_graph = False
        for probability in matching_graph.values():
            if 0 < probability < 1:  # If there is any tuple uncertain, create matching graph.
                world_graphs = WorldGraph(matching_graph)
                world_graphs_clusters.append(world_graphs.get_representation())

                # Include offers that might have been removed due to multiple invalid world-graphs.
                for offer in world_graphs.get_n():
                    included = False
                    for world in world_graphs.get_es():
                        if included:
                            break
                        for offer_duo in world:
                            if offer in offer_duo:
                                included = True
                                break
                    if not included:
                        cert_clusters.append([offer])
                created_graph = True
                break

        # If there are no uncertain tuples, add cluster separately.
        if not created_graph:
            cluster = []

            # Matching graphs is invalid, or there are no matching items. Put each item in separate cluster.
            # Could implement another solution for invalid M-graph.
            if (1 in matching_graph.values() and 0 in matching_graph.values())\
                    or 0 in matching_graph:
                offers = []
                for (offer1, offer2), probability in matching_graph.items():
                    if offer1 not in offers:
                        offers.append(offer1)
                    if offer2 not in offers:
                        offers.append(offer2)
                for offer in offers:
                    cert_clusters.append([offer])

            else:  # All offers in the graph are a definite match.
                for (offer1, offer2), probability in matching_graph.items():
                    if offer1 not in cluster:
                        cluster.append(offer1)
                    if offer2 not in cluster:
                        cluster.append(offer2)
                cert_clusters.append(cluster)

    return world_graphs_clusters, cert_clusters
