
from Levenshtein import distance
import jaro  # pip install jaro-winkler


# Retrieves the distance percentile based on the Levenshtein distance between two words. Also called Edit distance.
# Used in the paper of Yan et al. (2007) Adaptive Sorted Neighborhood Methods for Efficient Record Linkage.
def levenshtein(word1, word2):
    if not word1 and not word2:
        return 0
    elif not word1:
        return 1
    elif not word2:
        return 1
    else:
        dist = distance(word1, word2)
        length = (len(word1) + len(word2)) / 2
        dist_percent = (dist / length)
        # print('dist: ', dist_percent)
        return dist_percent


# Retrieves the distance percentile based on the Jaro-Winkler distance between two words.
# Used in the paper of De Vries et al. (2011) Robust Record Linkage Blocking Using Suffix Arrays and Bloom Filters.
def jarowinkler(word1, word2):
    if not word1 and not word2:
        return 0
    elif not word1:
        return 1
    elif not word2:
        return 1
    else:
        sim = jaro.jaro_metric(word1, word2)  # Provides a similarity score from 0 to 1.
        # dist = jaro.jaro_winkler_metric(word1, word2)
        dist_percent = 1 - sim
        # print('dist: ', dist_percent)
        return dist_percent


if __name__ == '__main__':
    # print(distance('hello', 'hella'))
    # print(distance('blabla', 'something'))
    print(levenshtein('hello', 'hella'))
    print(levenshtein('blabla', 'something'))

    # print(jaro.jaro_metric('hello', 'hello'))
    # print(jaro.jaro_metric('blabla', 'something'))
    # print(jarowinkler('hello', 'hella'))
    # print(jarowinkler('blabla', 'something'))




