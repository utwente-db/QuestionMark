# (Optional addition): Include performance measures uncertainty density and decisiveness.
import gzip
import json
import time

from aer_matcher import aer_matcher
from database_filler import get_attr_prob
from gold_standard_dataset import get_matches
from parameters import ITERS, DECIMAL_PLACES


# Used for basic performance measures.
# Generates a list of all clusters of type [[ids]].
def get_clusters(world_graph_clusters, certain_clusters):
    clusters = []
    for world_graph in world_graph_clusters:
        clusters.append(world_graph[0])
    clusters.extend(certain_clusters)
    return clusters


# Used for basic performance measures.
# Generates dict of type {offer_id:[matches]} from clusters with type [[offer_ids]] to compare with the gold standard.
def get_all_matches(clusters):
    all_matches = {}
    for cluster in clusters:
        for offer in cluster:
            if offer not in all_matches:
                all_matches[offer] = []
            for offer_id in cluster:
                if offer_id != offer and offer_id not in all_matches[offer]:
                    all_matches[offer].append(offer_id)
    return all_matches


# Used for probabilistic performance measures.
# Generate dict of type {offer_id:[(match, prob_match), ...]} to compare with the gold standard.
def get_probabilistic_matches(world_graph_clusters, certain_clusters):
    all_matches = {}

    with gzip.open('datasets/offers_gs_byID.json.gz', 'r') as id_file:
        offers = json.loads(id_file.read())

    for world_graph_cluster in world_graph_clusters:
        probabilities = get_attr_prob(offers, world_graph_cluster[0])
        for offer in world_graph_cluster[0]:
            if offer not in all_matches:
                all_matches[offer] = []
            for i in range(len(world_graph_cluster[0])):
                offer_id = world_graph_cluster[0][i]
                if offer_id != offer and offer_id not in all_matches[offer]:
                    all_matches[offer].append((offer_id, probabilities[i]))

    certain_matches = get_all_matches(certain_clusters)
    for offer, matches in certain_matches.items():
        match_prob = []
        for match in matches:  # add the probability of 1 to the certain matches.
            match_prob.append((match, 1))
        certain_matches[offer] = match_prob

    all_matches.update(certain_matches)  # merges the two dicts. Keys should not overlap.

    return all_matches


# Used for basic performance measures.
# Calculates the true positive (tp), true negative (tn), false positive (fp) and false negative (fn) matches.
def get_basic_dataset_measures(all_matches, tm, tnm):
    tp, tn, fp, fn = 0, 0, 0, 0

    for offer, matches in tm.items():
        if offer in all_matches.keys():
            for match in matches:
                if match in all_matches.get(offer):
                    tp += 1
                else:
                    fn += 1

    for offer, matches in tnm.items():
        if offer in all_matches.keys():
            for match in matches:
                if match in all_matches.get(offer):
                    fp += 1
                else:
                    tn += 1

    print('\ntp:', tp, 'tn:', tn, 'fp:', fp, 'fn:', fn)
    return tp, tn, fp, fn


# Used for probabilistic performance measures.
# Calculates the expected true positive (etp), expected true negative (etn),
#     expected false positive (efp) and expected false negative (efn) matches.
#     Obtained by the measure (tp/tn/fp/fn) x the probability of a world.
def get_expected_dataset_measures(all_matches, tm, tnm):
    etp, etn, efp, efn = 0, 0, 0, 0

    for offer, match_probs in all_matches.items():
        if offer in tm.keys():
            for (match, prob) in match_probs:
                if match in tm.get(offer):
                    etp += 1 * prob
                else:
                    efn += 1 * prob

    for offer, match_probs in all_matches.items():
        if offer in tnm.keys():
            for (match, prob) in match_probs:
                if match in tnm.get(offer):
                    etn += 1 * prob
                else:
                    efp += 1 * prob

    print('\netp:', etp, 'etn:', etn, 'efp:', efp, 'efn:', efn)
    return etp, etn, efp, efn


def get_precision(tp, fp):
    return tp / (tp + fp)


def get_recall(tp, fn):
    return tp / (tp + fn)


def get_expected_precision(etp, efp):
    return etp / (etp + efp)


def get_expected_recall(etp, tp, fn):
    return etp / (tp + fn)


def get_runtime(dataset):
    start_time = time.time()
    for run in range(ITERS):
        aer_matcher(dataset, performance=True)
    end_time = time.time()
    return ((end_time - start_time) * 10**3) / ITERS


def full_performance_scan(blocks):
    world_graph_clusters, certain_clusters = aer_matcher(blocks, performance=True)
    tm, tnm = get_matches('datasets/all_gs.json.gz')  # True Matches, True Non-Matches

    # To get the basic performance measures. Checks if the true representation exists in any possible world.
    clusters = get_clusters(world_graph_clusters, certain_clusters)
    matches = get_all_matches(clusters)
    tp, _, fp, fn = get_basic_dataset_measures(matches, tm, tnm)
    precision = round(get_precision(tp, fp), DECIMAL_PLACES)
    recall    = round(get_recall(tp, fn), DECIMAL_PLACES)
    runtime   = round(get_runtime(blocks), DECIMAL_PLACES)

    # To get the probabilistic performance measures.
    matches = get_probabilistic_matches(world_graph_clusters, certain_clusters)
    etp, _, efp, _ = get_expected_dataset_measures(matches, tm, tnm)
    expected_precision = round(get_expected_precision(etp, efp), DECIMAL_PLACES)
    expected_recall = round(get_expected_recall(etp, tp, fn), DECIMAL_PLACES)

    print('\nThe AER matching algorithm has the following performance:')
    print('  Precision:', precision)
    print('  Recall:', recall)
    print('  Expected precision:', expected_precision)
    print('  Expected recall:', expected_recall)
    print('  Average runtime over', ITERS, 'runs:', runtime, 'ms.')
