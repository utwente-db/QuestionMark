# GLOBAL VARIABLES
# Change these variables to adjust the settings of the blocking algorithms.
WS = 2     # Window Size            (asn)
PHI = 0.5  # Similarity Threshold   (asn / isa)
MSL = 3    # Minimum Suffix Length  (isa)
MBS = 30   # Maximum Block Size     (isa)

# Choose the blocking algorithm to be applied. Uncomment one (asn / isa)
BLOCK = 'asn'
# BLOCK = 'isa'

# Choose the distance algorithm to be applied. Uncomment one. (asn / isa)
DIST = 'levenshtein'
# DIST = 'jarowinkler'

# Choose the amount of iterations for a timed run (asn / isa)
ITERS = 2
