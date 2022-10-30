
# # ================
# # GLOBAL VARIABLES
# # ================

# # This file contains all parameters that can be changed to tweak the performance of the algorithms.
# # This section contains parameters used for both blocking and matching algorithms.

# # Choose the amount of iterations for a timed run
ITERS = 1

# # Choose the distance algorithm to be applied. Uncomment one.
# # Valid values (in case of a delete): levenshtein, jarowinkler, hamming, jaccard, lcsstr.
# # Others can be added by defining a new function in offer_distance.py
# #     and adding the case to asn_blocker.py / isn_blocker.py in the function get_distance().
DIST = 'levenshtein'  # from the asn paper, fastest
# DIST = 'jarowinkler'  # from the isa paper
# DIST = 'hamming'  # relatively slow for longer words
# DIST = 'jaccard'


# # ===================
# # BLOCKING ALGORITHMS
# # ===================

# # Check runtimes_blocker.txt to see how the different parameters change the performance of the algorithms.

# # Choose the blocking algorithm to be applied. Uncomment one.
BLOCK = 'asn'
# BLOCK = 'isa'  # DO NOT USE. See isa_blocker.py for more info.

# # Change these variables to adjust the settings of the blocking algorithms.
WS = 3     # Window Size            (asn)
PHI = 0.5  # Similarity Threshold   (asn / isa)
MSL = 3    # Minimum Suffix Length  (isa)
MBS = 20   # Maximum Block Size     (isa)


# # ==================
# # MATCHING ALGORITHM
# # ==================

# # Check runtimes_matcher.txt to see how the different parameters change the performance of the algorithm.
