# Prob-Matcher Manual

This file contains the roadmap on how this project is to be used. 
_Optional steps are displayed in italic_. 

Note that you are allowed to make changes to this program where it is deemed necessary. 
Please follow the rules as provided by the CC license. 

## 1 - Downloading the WDC datasets
- Create an empty folder ```datasets``` in the main project repo.
- Go to the [WDC website](http://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page.
- Download ```offers_corpus_english_v2.json.gz``` and ```all_gs.json.gz```, and include these in the empty datasets folder.
- _Download the samples to get an impression of the dataset structure._

## 2 - Preparing the dataset
- Open ```parameters.py``` and change the present parameters to the desired values. The file provides information on what the parameters are used for. Please check ```performance.txt``` to get an impression of how changing the parameters change the performance.
- Go to ```manual.py```. 
- _If a smaller dataset will be used:_ Run ```resize_dataset```. 
- _If a smaller dataset will be used:_ Open a terminal, ```cd``` to the datasets directory and run <nobr>```gzip offers_corpus_english_v2_resized.json```.</nobr>
- Uncomment and run ```sort_offers``` and ```offer_by_id```.
- Open a terminal and ```cd``` to the datasets directory. Run <nobr>```gzip offers_corpus_english_v2_sorted.json```.</nobr> and <nobr>```gzip offers_corpus_english_v2_byID.json```.</nobr>

## 3 - Running the blocking algorithm
- Verify the parameters set in ```parameters.py```.
- Depending on the choice of blocking algorithm, run ```asn_blocker``` or ```isa_blocker```.
- Run ```write_to_file```.

## 4 - Running the matching algorithm
- Verify the parameters set in ```parameters.py```.
- Run ```aer_matcher```.

## 5 - Writing to a database
- It is expected that a functioning database connection is set up.
- To implement...

## 6 - Running performance tests
- _Run ```create_dataset``` with the Golden Standard dataset._
- _Open a terminal, ```cd``` to the datasets directory and run <nobr>```gzip offers_corpus_gs.json```.</nobr>_
- _Run ```sort_offers```_with the newly created dataset.
- _To get the performance of the selected blocking algorithm, run ```blocker_performance.full_performance_scan```._
- _To get the performance of the matching algorithm, run ```asn_blocker``` with the newly created dataset and write the blocks to a file with ```write_to_file```.
- _Next, run ```blocker_performance.full_performance_scan```._