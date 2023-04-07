import sys
import time

from Levenshtein import distance
import textdistance  # pip install textdistance

from parameters import DIST


# Used in asn_blocker.py, isa_blocker.py and aer_matcher.py.
def get_distance(word1, word2):
    if DIST == 'levenshtein':
        return levenshtein(word1, word2)
    elif DIST == 'jarowinkler':
        return jarowinkler(word1, word2)
    elif DIST == 'hamming':
        return hamming(word1, word2)
    elif DIST == 'jaccard':
        return jaccard(word1, word2)
    else:
        sys.exit("Please input a valid value for DIST in parameters.py.")


# Retrieves the distance percentile based on the Levenshtein distance between two words.
# The levenshtein algorithm from this library is faster than the one from textdistance.
# Used in the paper of Yan et al. (2007) Adaptive Sorted Neighborhood Methods for Efficient Record Linkage.
def levenshtein(word1, word2):
    if (not word1 and not word2) or (word1 == 'None' and word2 == 'None'):
        return 1  # could change to 0.
    elif not word1 or word1 == 'None':
        return 1
    elif not word2 or word2 == 'None':
        return 1
    else:
        dist = distance(word1, word2)
        length = (len(word1) + len(word2)) / 2
        dist_percent = (dist / length)
        return dist_percent


# Retrieves the distance percentile based on the Jaro or Jaro-Winkler distance between two words.
# Used in the paper of De Vries et al. (2011) Robust Record Linkage Blocking Using Suffix Arrays and Bloom Filters.
def jarowinkler(word1, word2):
    if (not word1 and not word2) or (word1 == 'None' and word2 == 'None'):
        return 0
    elif not word1 or word1 == 'None':
        return 1
    elif not word2 or word2 == 'None':
        return 1
    else:
        sim = textdistance.jaro(word1, word2)  # Provides a similarity score from 0 to 1.
        # sim = textdistance.jaro_winkler(word1, word2)
        dist_percent = 1 - sim
        # print('dist: ', dist_percent)
        return dist_percent


# Other word distance measures from: https://pypi.org/project/textdistance/
def hamming(word1, word2):
    if (not word1 and not word2) or (word1 == 'None' and word2 == 'None'):
        return 0
    elif not word1 or word1 == 'None':
        return 1
    elif not word2 or word2 == 'None':
        return 1
    else:
        dist = textdistance.hamming(word1, word2)
        length = (len(word1) + len(word2)) / 2
        dist_percent = (dist / length)
        # print('dist: ', dist_percent)
        return dist_percent


def jaccard(word1, word2):
    if (not word1 and not word2) or (word1 == 'None' and word2 == 'None'):
        return 0
    elif not word1 or word1 == 'None':
        return 1
    elif not word2 or word2 == 'None':
        return 1
    else:
        sim = textdistance.jaccard(word1, word2)  # Provides a similarity score from 0 to 1.
        dist_percent = 1 - sim
        # print('dist: ', dist_percent)
        return dist_percent


# used for comparing the speed of various algorithms.
def timed(word1, word2):
    st = time.time()  # start time
    for run in range(5000):
        levenshtein(word1, word2)
    et = time.time()  # end time
    print('algorithm 1:')
    print(((et - st) * 10**3) / 50000)

    st = time.time()  # start time
    for run in range(5000):
        jaccard(word1, word2)
    et = time.time()  # end time
    print('algorithm 2:')
    print(((et - st) * 10**3) / 50000)


# Can be used to test the functions here. Not used by another function.
def test():
    print(hamming('somethinginthisworldthatIhaveneverseen', 'somethingcompletelydifferentnobodyhaswitnessed'))
    print(hamming('hello', 'hello'))
    print(hamming('bla', 'ewo'))

    timed('somethinginthisworldthatIhaveneverseen', 'somethingcompletelydifferentnobodyhaswitnessed')
    timed('blabla', 'ewoewo')


if __name__ == '__main__':
    # Can be used for testing
    test()
