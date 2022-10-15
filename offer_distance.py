
from Levenshtein import distance


# Retrieves the distance percentile based on the Levenshtein distance between two words.
def levenshtein(word1, word2):
    if not word1 and not word2:
        dist = 0
        length = 1
    elif not word1:
        dist = len(word2)
        length = len(word2)
    elif not word2:
        dist = len(word1)
        length = len(word1)
    else:
        dist = distance(word1, word2)
        length = (len(word1) + len(word2)) / 2
    dist_percent = (dist / length)
    # print('dist: ', dist_percent)
    return dist_percent
