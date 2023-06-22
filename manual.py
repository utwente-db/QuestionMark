# =================================================================================================== #
# ========== MANUAL ================================================================================= #
# This file is a supplement to the MANUAL.md roadmap. This file contains easy access to the functions #
# present in this project and follows the steps as explained in the roadmap.                          #
# =================================================================================================== #
from src.dataset_preparation import resize_dataset
from src.dataset_preparation import sort_offers
from src.dataset_preparation import offer_by_id
from src.asn_blocker import asn_blocker
from src.asn_blocker import write_blocks_to_file
from src.isa_blocker import isa_blocker  # This could be used, but is not recommended.
from src.aer_matcher import aer_matcher
from src.aer_matcher import write_clusters_to_file
from src.database_filler_dubio import transfer_to_dubio
from src.database_filler_maybms import transfer_to_maybms
from src.gold_standard_dataset import create_dataset
from src import matcher_performance, blocker_performance
from parameters import BLOCK, SMALLER_DATASET, DBMS, PERFORMANCE, MEASURE

if __name__ == '__main__':
    if not PERFORMANCE:
        # # ====== SETUP  ================================================================================= #
        # In a terminal, run: pip install textdistance

        # # ====== DATASET GENERATION ===================================================================== #
        print("\n == Welcome to QuestionMark: The Dataset Generator. == \n")

        if SMALLER_DATASET:
            print(" Creating a smaller dataset...")
            resize_dataset('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_resized.json.gz')

        print(" Sorting the dataset and creating an index...")
        if SMALLER_DATASET:
            sort_offers('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_sorted.json.gz')
            offer_by_id('datasets/offers_corpus_resized.json.gz', 'datasets/offers_corpus_byID.json.gz')
        else:
            sort_offers('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_sorted.json.gz')
            offer_by_id('datasets/offers_corpus_english_v2.json.gz', 'datasets/offers_corpus_byID.json.gz')

        print(" Creating the blocks...")
        if BLOCK == 'asn':
            blocks = asn_blocker('datasets/offers_corpus_sorted.json.gz')
        elif BLOCK == 'isa':
            blocks = isa_blocker('datasets/offers_corpus_sorted.json.gz')
        else:
            raise Exception(" Please input either 'asn' or 'isa' as value of BLOCK in parameters.py")
        write_blocks_to_file(blocks, 'datasets/blocks')

        print(" Creating the clusters...")
        prob_clust, cert_clust = aer_matcher('datasets/blocks')
        write_clusters_to_file(prob_clust, cert_clust, 'datasets/clusters_prob', 'datasets/clusters_cert')

        print(" Inserting the clusters in " + DBMS + "...")
        if DBMS == 'MayBMS':
            transfer_to_maybms('datasets/clusters_prob', 'datasets/clusters_cert')
        elif DBMS == 'DuBio':
            transfer_to_dubio('datasets/clusters_prob', 'datasets/clusters_cert')
        else:
            raise Exception(" Please choose a valid value of DBMS in parameters.py")

        print('\n +---------------------------------------------------------------------------------+'
              '\n | Hurray! The dataset generation is finished!                                     |'
              '\n | Go to QuestionMark: The Dataset Generator to continue the benchmarking process. |'
              '\n +---------------------------------------------------------------------------------+')

    else:
        # # ====== PERFORMANCE MEASURES =================================================================== #
        # # Only executes when you want to measure the performance of the dataset generation.
        create_dataset('datasets/all_gs.json.gz', 'datasets/offers_gs.json.gz')
        sort_offers('datasets/offers_gs.json.gz', 'datasets/offers_gs_sorted.json.gz')

        if MEASURE == 'block':
            blocker_performance.full_performance_scan('datasets/offers_gs_sorted.json.gz')

        if MEASURE == 'match':
            offer_by_id('datasets/offers_gs_sorted.json.gz', 'datasets/offers_gs_byID.json.gz')

            if BLOCK == 'asn':
                gs_blocks = asn_blocker('datasets/offers_gs_sorted.json.gz')
            elif BLOCK == 'isa':
                gs_blocks = isa_blocker('datasets/offers_gs_sorted.json.gz')
            else:
                raise Exception(" Please input either 'asn' or 'isa' as value of BLOCK in parameters.py")
            write_blocks_to_file(gs_blocks, 'datasets/gs_blocks')

            matcher_performance.full_performance_scan('datasets/gs_blocks')
