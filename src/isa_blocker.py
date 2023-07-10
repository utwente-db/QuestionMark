import gzip
import json
import collections

from src.offer_distance import *
from parameters import MSL, MBS, PHI


def get_suffixes(bkv):
    suffixes = []
    if bkv:
        for i in range(len(bkv) - MSL + 1):
            suffixes.append(bkv[i:])
    return suffixes


def fill_block(block, offers):
    for offer in offers:
        if offer not in block:
            block.append(offer)
    return block


# Based on the paper of De Vries et al. (2011) Robust Record Linkage Blocking Using Suffix Arrays and Bloom Filters.
def isa_blocker(dataset):
    blocks = []
    ii = {}  # inverted index

    # index construction
    with gzip.open(dataset) as offers_file:  # Open the sorted dataset
        for line in offers_file:
            offer = json.loads(line.decode('utf-8'))
            bkv = (  # (offer.get('category') if offer.get('category') else '') +
                     # (offer.get('brand') if offer.get('brand') else '') +
                   (offer.get('title') if offer.get('title') else ''))  # blocking key value
            suffixes = get_suffixes(bkv)
            for suffix in suffixes:
                if suffix not in ii:
                    ii[suffix] = []
                ii[suffix].append(offer.get('id'))

    # large block removal
    to_delete = []
    for suffix in ii:
        if len(ii[suffix]) > MBS:
            to_delete.append(suffix)
    for suffix in to_delete:
        del ii[suffix]

    # suffix grouping
    ord_ii = collections.OrderedDict(sorted(ii.items()))
    prev_suffix = ''
    block = []
    for suffix, offers in ord_ii.items():
        dist = get_distance(prev_suffix, suffix)
        if dist < PHI:
            block = fill_block(block, offers)
        else:
            if block:
                blocks.append(block)
            block = []
            block = fill_block(block, offers)
        prev_suffix = suffix

    # Currently, the blocks are merged from neighboring suffixes that have a high similarity. As one word can produce
    # suffixes that are not much alike (e.g. 'Hello' produces 'ello' and 'llo', which are alphabetically far apart),
    # one offer will occur in multiple blocks. The original idea from the paper is that one can query the blocks for
    # one specific offer, and retrieve all matches by looping through all blocks. This is computationally very
    # expensive to do for all offers and implementing this is deemed out of scope for this research.

    return blocks