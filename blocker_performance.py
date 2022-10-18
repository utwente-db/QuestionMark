import time

from asn_blocker import asn_blocker
from isa_blocker import isa_blocker

# include from ISA paper: pairs completeness   -> recall.
#                         pairs quality        -> precision.


def get_precision(dataset, blocker):

    if blocker == 'asn':
        asn_blocker(dataset)
    elif blocker == 'isa':
        isa_blocker(dataset)
    else:
        print("Please input as second parameter 'asn' for Adaptive Sorted Neighborhood blocking, or 'isa' for "
              "Improved Suffix Array blocking .")
    return 5


def time_exec(dataset, blocker, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        get_precision(dataset, blocker)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    time_exec('datasets/offers_corpus_english_v2_gs.json.gz', 'asn', 50)
    