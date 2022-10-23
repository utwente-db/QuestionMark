import sys
import time

from asn_blocker import asn_blocker
from gold_standard_dataset import get_matches
from isa_blocker import isa_blocker
from parameters import BLOCK, ITERS


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


def get_dataset_measures(blocks):
    tp = 0  # True Positive
    tn = 0  # True Negative
    fp = 0  # False Positive
    fn = 0  # False Negative
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

    print(tp, tn, fp, fn)
    return tp, tn, fp, fn


def get_precision(tp, fp):  # pair quality
    return tp / (tp + fp) if (tp + fp) > 0 else 2


def get_recall(tp, fn):  # pair completeness
    return tp / (tp + fn) if (tp + fn) > 0 else 2


def get_runtime(dataset, blocker, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        get_blocks(dataset, blocker)
    et = time.time()  # end time
    return ((et - st) * 10**3) / iterations


def full_performance_scan(dataset):
    blocker = BLOCK
    iterations = ITERS
    blocks = get_blocks(dataset, blocker)
    tp, _, fp, fn = get_dataset_measures(blocks)
    precision = get_precision(tp, fp)
    recall    = get_recall(tp, fn)
    runtime   = get_runtime(dataset, blocker, iterations)
    print('The', blocker, 'blocking algorithm has the following performance:')
    print('Precision:', precision)
    print('Recall:', recall)
    print('Average runtime over', iterations, 'runs:', runtime)


if __name__ == '__main__':
    # full_performance_scan('datasets/offers_corpus_english_v2_gs.json.gz')
    full_performance_scan('datasets/offers_corpus_english_v2_999k_sorted.json.gz')

    