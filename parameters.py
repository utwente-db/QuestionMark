# Check runtimes_matcher.txt to see how the different parameters change the performance of the algorithm.

# # ================
# # GLOBAL VARIABLES
# # ================

# # This file contains all parameters that can be changed to tweak the performance of the algorithms.
# # This section contains parameters used for both blocking and matching algorithms.

# # Across the different files, different datasets get used. As this is not truly a parameter, and it is difficult
# #   to keep track of all these datasets in one variable, it was chosen to keep these in the corresponding files
# #   as hardcode variables. Please check the files for the dataset and change it when needed.

# # Choose the amount of iterations for a timed run
ITERS = 1

# # Choose the distance algorithm to be applied. Uncomment one.
# # Valid values (in case of a delete): levenshtein, jarowinkler, hamming, jaccard, lcsstr.
# # Others can be added by defining a new function in offer_distance.py
# #   and adding the case to asn_blocker.py / isn_blocker.py in the function get_distance().
DIST = 'levenshtein'  # from the asn paper, fastest
# DIST = 'jarowinkler'  # from the isa paper
# DIST = 'hamming'  # relatively slow for longer words
# DIST = 'jaccard'


# # ===================
# # DATASET PREPARATION
# # ===================

# The percentage of the dataset to be used. The full size is around 16 million offers / 2.9 GB zipped.
# For approximately 50% of the dataset, assign value 50.
DATASET_SIZE = 0.01  # Works with up to two decimal points
# All attributes that are NOT a BKV (blocking key value). All attributes of an offer: ['brand', 'category',
#   'cluster_id', 'description', 'id', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']
NON_BKV = ['description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent']  # also keep id and cluster_id.


# # ===================
# # BLOCKING ALGORITHMS
# # ===================

# # Check performance.txt.txt to see how the different parameters change the performance of the algorithms.

# # Choose the blocking algorithm to be applied. Uncomment one.
BLOCK = 'asn'
# BLOCK = 'isa'  # DO NOT USE. See isa_blocker.py for more info.

# # Change these variables to adjust the settings of the blocking algorithms.
WS = 2     # Window Size            (asn)
PHI = 0.7  # similarity Threshold   (asn / isa)  # Distance!
MBS = 6    # Maximum Block Size     (asn / isa)
MSL = 3    # Minimum Suffix Length  (isa)


# # ==================
# # MATCHING ALGORITHM
# # ==================

# List of attributes that are used to obtain a matching score. All attributes of an offer: ['brand', 'category',
#   'cluster_id', 'description', 'id', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']
ATTRIBUTES = ['brand', 'category', 'description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']

# The weight associated to the similarity score of an attribute.
# Values from 0 to 1.  0 = exclude. len(WEIGHTS) = len(ATTRIBUTES).
WEIGHTS = [0.8, 0.7, 1, 1, 1, 1, 1, 1]

# Distance < LOWER_PHI? Definitely the same product. Increase value to obtain a more certain dataset.
LOWER_PHI = 0.35

# Distance > UPPER_PHI? Definitely not the same product. Decrease value to obtain a more certain dataset.
UPPER_PHI = 0.5
