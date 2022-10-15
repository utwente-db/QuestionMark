import time

from asn_blocker import asn_blocker


def get_precision(dataset):
    asn_blocker(dataset)
    return 5


def time_exec(dataset, iterations):
    st = time.time()  # start time
    for run in range(iterations):
        get_precision(dataset)
    et = time.time()  # end time
    print("program duration: ", (et - st) * 10**3, "ms")
    print("average duration: ", ((et - st) * 10**3) / iterations, "ms")


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking   --> 50 000 records in 320 ms over 50 runs average.
    time_exec('datasets/offers_corpus_english_v2_sorted.json.gz', 50)  # for a timed run.
    