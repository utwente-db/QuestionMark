# =================================================================================================== #
# ========== MANUAL ================================================================================= #
# This file is a supplement to the MANUAL.md roadmap. This file contains easy access to the functions #
# present in this project and follows the steps as explained in the roadmap.                          #
# =================================================================================================== #
from dataset_preparation import resize_dataset
from dataset_preparation import sort_offers
from dataset_preparation import offer_by_id
from asn_blocker import asn_blocker
from asn_blocker import write_blocks_to_file
from isa_blocker import isa_blocker  # This could be used, but is not recommended.
from aer_matcher import aer_matcher
from aer_matcher import write_clusters_to_file
from database_filler_dubio import transfer_to_dubio
from database_filler_maybms import transfer_to_maybms
from gold_standard_dataset import create_dataset
import blocker_performance
import matcher_performance
from parameters import BLOCK

if __name__ == '__main__':
    # # Uncomment and run whole blocks in order.
    # # ====== SETUP  ================================================================================= #
    # In a terminal, run: pip install textdistance

    # # ====== STEP 1 ================================================================================= #
    # # No functions required.

    # # ====== STEP 2 ================================================================================= #
    # # Steps to take if a smaller dataset will be used.
    resize_dataset('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_resized.json')
    # # Gzip offers_corpus_resized.json.

    # sort_offers('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_sorted.json')
    # offer_by_id('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_byID.json')
    # # Gzip offers_corpus_sorted.json and offers_corpus_byID.json.

    # # Steps to take if the full dataset will be used.
    # sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_sorted.json')
    # offer_by_id('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_byID.json')
    # # Gzip offers_corpus_sorted.json and offers_corpus_byID.json.

    # # ====== STEP 3 ================================================================================= #
    # if BLOCK == 'asn':
    #     blocks = asn_blocker('datasets/offers_corpus_sorted.json.gz')
    # elif BLOCK == 'isa':
    #     blocks = isa_blocker('datasets/offers_corpus_sorted.json.gz')
    # else:
    #     raise Exception("Please input either 'asn' or 'isa' as value of BLOCK in parameters.py")
    # write_blocks_to_file(blocks, 'datasets/blocks')

    # # ====== STEP 4 ================================================================================= #
    # # Creating the clusters
    # prob_clust, cert_clust = aer_matcher('datasets/blocks')
    # write_clusters_to_file(prob_clust, cert_clust, 'datasets/clusters_prob', 'datasets/clusters_cert')

    # # ====== STEP 5 ================================================================================= #
    # # Write to MayBMS
    # transfer_to_maybms('datasets/clusters_prob', 'datasets/clusters_cert')

    # # Write to DuBio
    # transfer_to_dubio('datasets/clusters_prob', 'datasets/clusters_cert')

    # # ====== STEP 6 ================================================================================= #
    # # Only execute when you want to measure the performance of the dataset generation.

    # create_dataset('datasets/all_gs.json.gz', 'datasets/offers_gs.json')
    # # gzip file.
    # sort_offers('datasets/offers_gs.json.gz', 'datasets/offers_gs_sorted.json')
    # # gzip file.

    # # To get the performance of the blocking algorithm
    # blocker_performance.full_performance_scan('datasets/offers_gs_sorted.json.gz')

    # # To get the performance of the matching algorithm.
    # offer_by_id('datasets/offers_gs_sorted.json.gz', 'datasets/offers_gs_byID.json')
    # gzip file
    # if BLOCK == 'asn':
    #     gs_blocks = asn_blocker('datasets/offers_gs_sorted.json.gz')
    # elif BLOCK == 'isa':
    #     gs_blocks = isa_blocker('datasets/offers_gs_sorted.json.gz')
    # else:
    #     raise Exception("Please input either 'asn' or 'isa' as value of BLOCK in parameters.py")
    # write_blocks_to_file(gs_blocks, 'datasets/gs_blocks')

    # matcher_performance.full_performance_scan('datasets/gs_blocks')
