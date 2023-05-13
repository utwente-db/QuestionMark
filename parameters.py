# Check runtimes_matcher.txt to see how the different parameters change the performance of the algorithm.

# This file contains all parameters that can be changed to tweak the performance of the algorithms.

# # ================
# # GLOBAL VARIABLES
# # ================

# # This section contains parameters used for both blocking and matching algorithms.

# # Choose the distance algorithm to be applied. Uncomment one.
# # Valid values (in case of a delete): levenshtein, jarowinkler, hamming, jaccard.
# # Others can be added by defining a new function in offer_distance.py
# #   and adding the case to asn_blocker.py / isn_blocker.py in the function get_distance().
# DIST = 'levenshtein'  # from the asn paper, fastest
DIST = 'jarowinkler'  # from the isa paper
# DIST = 'hamming'  # relatively slow for longer words
# DIST = 'jaccard'


# # ===================
# # DATASET PREPARATION
# # ===================

# Uncomment below when you wish to include more certainty / have smaller clusters.
# Uncomment below when you wish to include higher uncertainty / have larger clusters.

# # The percentage of the dataset to be used. The full size is around 16 million offers / 2.9 GB zipped.
# # For approximately 50% of the dataset, assign value 50.
DATASET_SIZE = 0.01  # Works up to two decimal points
# # For a resized dataset, indicate if whole clusters need to be picked from the dataset or individual offers.
WHOLE_CLUSTERS = False
# # All attributes that are NOT a BKV (blocking key value). All attributes of an offer: ['brand', 'category',
# #   'cluster_id', 'description', 'id', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']
NON_BKV = ['description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent']  # also keep id and cluster_id.


# # ===================
# # BLOCKING ALGORITHMS
# # ===================

# # Check performance.txt.txt to see how the different parameters change the performance of the algorithms.

# # Choose the blocking algorithm to be applied. Uncomment one.
# BLOCK = 'asn'
BLOCK = 'isa'  # is very slow

# # Change these variables to adjust the settings of the blocking algorithms.
WS = 2      # Window Size            (asn)                      # Default 2
PHI = 0.36  # similarity Threshold   (asn / isa)  # Distance!   # Default 0.36
MBS = 6     # Maximum Block Size     (asn / isa)                # Default 6
MSL = 3     # Minimum Suffix Length  (isa)                      # Default 3


# # ==================
# # MATCHING ALGORITHM
# # ==================

# # List of attributes that are used to obtain a matching score. All attributes of an offer: ['brand', 'category',
# #   'cluster_id', 'description', 'id', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']
ATTRIBUTES = ['brand', 'category', 'cluster_id', 'description', 'identifiers', 'keyValuePairs', 'price', 'specTableContent', 'title']

# # The weight associated to the similarity score of an attribute.
# # Values from 0 to 1.  0 = exclude. len(WEIGHTS) = len(ATTRIBUTES).
WEIGHTS = [1, 0.7, 1, 0.8, 0.8, 0.8, 1, 0.7, 1]

# # Distance < LOWER_PHI? Definitely the same product. Increase value to obtain a more certain dataset.
LOWER_PHI = 0.12  # Default 0.12

# # Distance > UPPER_PHI? Definitely not the same product. Decrease value to obtain a more certain dataset.
UPPER_PHI = 0.36  # Default 0.36


# # ===========
# # PERFORMANCE
# # ===========

# # Choose the amount of iterations for a timed run.
ITERS = 10

# # Choose the precision the performance results are displayed in.
DECIMAL_PLACES = 3
