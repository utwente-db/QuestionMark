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
from database_filler import transfer_to_maybms, connect_pg, close_pg
from database_filler import transfer_to_dubio
from gold_standard_dataset import create_dataset
import blocker_performance
import matcher_performance


if __name__ == '__main__':
    # ====== STEP 1 ================================================================================= #
    # # No functions required.

    # ====== STEP 2 ================================================================================= #
    # # Uncomment and run in order.
    # # The generated datasets should be manually gzipped before running the next function.

    # # Steps to take if a smaller dataset will be used.
    # resize_dataset('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_resized.json')
    # sort_offers('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_sorted.json')
    # offer_by_id('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_byID.json')

    # # Steps to take if the full dataset will be used.
    # sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_sorted.json')
    # offer_by_id('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_byID.json')

    # ====== STEP 3 ================================================================================= #
    # # When using the Incrementally Adaptive Sorted Neighborhood (asn) blocker.
    # blocks = asn_blocker('datasets/offers_corpus_sorted.json.gz')
    # write_blocks_to_file(blocks, 'datasets/asn_blocks')  # Writing the blocks to file.

    # ====== STEP 4 ================================================================================= #
    # # Creating the clusters
    # prob_clust, cert_clust = aer_matcher('datasets/asn_blocks')
    # # Writing clusters to file.
    # write_clusters_to_file(prob_clust, cert_clust, 'datasets/aer_clusters_prob', 'datasets/aer_clusters_cert')

    # ====== STEP 5 ================================================================================= #
    # # Connect to the database
    connect_pg(configname='database.ini')

    # # Write to MayBMS
    # transfer_to_maybms('datasets/aer_clusters_prob', 'datasets/aer_clusters_cert')

    # # Write to DuBio
    transfer_to_dubio('datasets/aer_clusters_prob', 'datasets/aer_clusters_cert')

    # # Close connection
    close_pg()

    # ====== STEP 6 ================================================================================= #
    # create_dataset('datasets/all_gs.json.gz')
    # # gzip file.
    # sort_offers('datasets/offers_corpus_gs.json.gz', 'datasets/offers_corpus_gs_sorted.json')

    # # To get the performance of the blocking algorithm
    # blocker_performance.full_performance_scan('datasets/offers_corpus_gs_sorted.json.gz')

    # # To get the performance of the matching algorithm.
    # gs_blocks = asn_blocker('datasets/offers_corpus_gs_sorted.json.gz')
    # write_blocks_to_file(gs_blocks, 'datasets/asn_gs_blocks')
    # matcher_performance.full_performance_scan('datasets/asn_gs_blocks')
