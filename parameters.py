# # GLOBAL VARIABLES

# # Choose the blocking algorithm to be applied. Uncomment one.
BLOCK = 'asn'
# BLOCK = 'isa'

# # Choose the distance algorithm to be applied. Uncomment one.
# # Valid values (in case of a delete): levenshtein, jarowinkler, hamming, jaccard, lcsstr.
# # Others can be added by defining a new function in offer_distance.py
# #     and adding the case to asn_blocker.py / isn_blocker.py in the function get_distance().
DIST = 'levenshtein'  # from the asn paper, fastest
# DIST = 'jarowinkler'  # from the isa paper
# DIST = 'hamming'  # relatively slow for longer words
# DIST = 'jaccard'

# # Choose the amount of iterations for a timed run
ITERS = 1

# # Change these variables to adjust the settings of the blocking algorithms.
WS = 2     # Window Size            (asn)
PHI = 0.2  # Similarity Threshold   (asn / isa)
MSL = 3    # Minimum Suffix Length  (isa)
MBS = 30   # Maximum Block Size     (isa)

# # Check runtimes.txt to see how the different parameters change the performance of the algorithm.
