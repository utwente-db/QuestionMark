import time

from aer_matcher import aer_matcher
from gold_standard_dataset import get_matches
from parameters import ITERS


# Generate dict of type {offer_id:[matches]} from clusters with type [{[offer_ids]: probability}]  # TODO: check type.
#     to compare with the gold standard.
def get_all_matches(clusters_raw):
    all_matches = {}
    for cluster in clusters_raw:
        for offer in cluster:
            if offer not in all_matches:
                all_matches[offer] = []
            for offer_id in cluster:
                if offer_id != offer and offer_id not in all_matches[offer]:
                    all_matches[offer].append(offer_id)

    return all_matches


# Generate dict of type {offer_id:[matches]} from clusters with type [[offer_ids]] to compare with the gold standard.
def get_probabilistic_matches(clusters_raw):
    all_matches = {}
    for cluster in clusters_raw:
        for offer in cluster:
            pass

    return all_matches


def get_basic_dataset_measures(all_matches):
    tp = 0  # True Positive
    tn = 0  # True Negative
    fp = 0  # False Positive
    fn = 0  # False Negative
    tm, tnm = get_matches('datasets/all_gs.json.gz')  # True Matches, True Non-Matches

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

    print(tp, tn, fp, fn)
    return tp, tn, fp, fn


def get_expected_dataset_measures(all_matches):
    etp = 0  # True Positive x probability of a world
    etn = 0  # True Negative x probability of a world
    efp = 0  # False Positive x probability of a world
    efn = 0  # False Negative x probability of a world
    tm, tnm = get_matches('datasets/all_gs.json.gz')  # True Matches, True Non-Matches

    for offer, matches in tm.items():
        if offer in all_matches.keys():
            for match in matches:
                if match in all_matches.get(offer):
                    etp += 1
                else:
                    efn += 1

    for offer, matches in tnm.items():
        if offer in all_matches.keys():
            for match in matches:
                if match in all_matches.get(offer):
                    efp += 1
                else:
                    etn += 1

    print(etp, etn, efp, efn)
    return etp, etn, efp, efn


def get_precision(tp, fp):  # pair quality
    return tp / (tp + fp) if (tp + fp) > 0 else 2  # TODO remove 'else 2' when functioning properly.


def get_recall(tp, fn):  # pair completeness
    return tp / (tp + fn) if (tp + fn) > 0 else 2


def get_expected_precision(etp, efp):
    return etp / (etp + efp) if (etp + efp) else 2


def get_expected_recall(etp, tp, fn):
    return etp / (tp + fn) if (tp + fn) else 2


def get_uncertainty_density():
    return 0


def get_decisiveness():
    return 0


def get_runtime(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        aer_matcher(dataset)
    et = time.time()  # end time
    return ((et - st) * 10**3) / iterations


def full_performance_scan(blocks):
    iterations = ITERS
    clusters = aer_matcher(blocks)

    # To get the basic performance measures. Checks if the true representation exists in any possible world.
    matches = get_all_matches(clusters)
    tp, _, fp, fn = get_basic_dataset_measures(matches)
    precision = get_precision(tp, fp)
    recall    = get_recall(tp, fn)
    runtime   = get_runtime(blocks, iterations)

    # To get the probabilistic performance measures.
    matches = get_probabilistic_matches(clusters)
    etp, etn, efp, efn = get_expected_dataset_measures(matches)
    expected_precision = get_expected_precision(etp, efp)
    expected_recall = get_expected_recall(etp, tp, fn)
    uncertainty_density = get_uncertainty_density()
    decisiveness = get_decisiveness()

    print('The aer blocking algorithm has the following performance:')
    print('Precision:', precision)
    print('Recall:', recall)
    print('Expected precision:', expected_precision)
    print('Expected recall:', expected_recall)
    print('Uncertainty density:', uncertainty_density)
    print('Decisiveness:', decisiveness)
    print('Average runtime over', iterations, 'runs:', runtime)


if __name__ == '__main__':
    full_performance_scan('datasets/asn_gs_blocks')
    # full_performance_scan('datasets/asn_blocks')
