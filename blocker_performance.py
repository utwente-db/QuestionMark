import sys
import time

from asn_blocker import asn_blocker
from gold_standard_dataset import get_matches
from isa_blocker import isa_blocker
from parameters import BLOCK, ITERS, DECIMAL_PLACES


def run_blocker(dataset, blocker):
    if blocker == 'asn':
        asn_blocker(dataset)
    elif blocker == 'isa':
        isa_blocker(dataset)
    else:
        sys.exit("Please input as second parameter 'asn' for Adaptive Sorted Neighborhood blocking, or 'isa' for "
                 "Improved Suffix Array blocking.")


def get_blocks(dataset, blocker):
    if blocker == 'asn':
        blocks_raw = asn_blocker(dataset)
    elif blocker == 'isa':
        blocks_raw = isa_blocker(dataset)
    else:
        sys.exit("Please input as second parameter 'asn' for Adaptive Sorted Neighborhood blocking, or 'isa' for "
                 "Improved Suffix Array blocking.")

    # generate dict of type {offer_id:[matches]} from blocks with type [[offer_ids]] to compare with the gold standard.
    blocks = {}
    for block in blocks_raw:
        for offer in block:
            if offer not in blocks:
                blocks[offer] = []
            for offer_id in block:
                if offer_id != offer and offer_id not in blocks[offer]:
                    blocks[offer].append(offer_id)

    return blocks


# Calculates the true positive (tp), true negative (tn), false positive (fp) and false negative (fn) matches.
def get_dataset_measures(blocks):
    tp, tn, fp, fn = 0, 0, 0, 0
    tm, tnm = get_matches('datasets/all_gs.json.gz')  # True Matches, True Non-Matches

    for offer, matches in tm.items():
        if offer in blocks.keys():
            for match in matches:
                if match in blocks.get(offer):
                    tp += 1
                else:
                    fn += 1

    for offer, matches in tnm.items():
        if offer in blocks.keys():
            for match in matches:
                if match in blocks.get(offer):
                    fp += 1
                else:
                    tn += 1

    print('\ntp:', tp, 'tn:', tn, 'fp:', fp, 'fn:', fn)
    return tp, tn, fp, fn


def get_precision(tp, fp):  # pair quality
    return tp / (tp + fp)


def get_recall(tp, fn):  # pair completeness
    return tp / (tp + fn)


def get_runtime(dataset):
    start_time = time.time()
    for run in range(ITERS):
        run_blocker(dataset, BLOCK)
    end_time = time.time()
    return ((end_time - start_time) * 10**3) / ITERS


def full_performance_scan(dataset):
    blocks = get_blocks(dataset, BLOCK)
    tp, _, fp, fn = get_dataset_measures(blocks)
    precision = round(get_precision(tp, fp), DECIMAL_PLACES)
    recall    = round(get_recall(tp, fn), DECIMAL_PLACES)
    runtime   = round(get_runtime(dataset), DECIMAL_PLACES)
    print('\nThe', BLOCK.upper(), 'blocking algorithm has the following performance:')
    print('  Precision:', precision)
    print('  Recall:', recall)
    print('  Average runtime over', ITERS, 'runs:', runtime, 'ms.')
