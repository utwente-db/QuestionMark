# Manual

This file contains the roadmap on how QuestionMark: The Dataset Generator
 is to be used. 
_Optional steps are displayed in italic_. 

Note that you are allowed to make changes to this program. 
Please follow the rules as provided by the CC license. 

## 1 - Downloading the WDC datasets
- Create an empty folder ```datasets``` in the main project repo.
- Go to the [WDC website](http://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page.
- Download ```offers_corpus_english_v2.json.gz``` and include this in the newly created datasets folder.
- _Download the samples to get an impression of the dataset structure._

## 2 - Preparing the dataset
- Open ```parameters.py``` and change the present parameters to the desired values. The file provides information on what the parameters are used for. Please check ```performance.txt``` to get an impression of how changing the parameters changes the performance.
- Go to ```manual.py```. 
- _If a smaller dataset will be used:_ Run ```resize_dataset```. 
- _If a smaller dataset will be used:_ Open a terminal, ```cd``` to the datasets directory and run <nobr>```gzip offers_corpus_resized.json```.</nobr>
- Uncomment and run ```sort_offers``` and ```offer_by_id```.
- Open a terminal and ```cd``` to the datasets directory. Run <nobr>```gzip offers_corpus_sorted.json```</nobr> and <nobr>```gzip offers_corpus_byID.json```.</nobr>

## 3 - Running the blocking algorithm
- Run ```asn_blocker``` and ```write_to_file```.

## 4 - Running the matching algorithm
- Run ```aer_matcher``` and ```write_to_file```.

## 5 - Writing to a database
- It is expected that a functioning database connection is set up. _In case a probabilistic DBMS will be benchmarked that is non-PostgreSQL based, please see the instructions on the bottom of this manual._
- Create a file called ```database.ini``` and fill in the credentials following the structure of ```database.ini.tmpl```.
- For MayBMS, run ```transfer_to_maybms```. For DuBio, run ```transfer_to_dubio```.
- You now have your dataset prepared! You can continue with the benchmarking. Go to [QuestionMark: The Probabilistic Benchmark](https://gitlab.utwente.nl/s1981951/probabilistic-benchmark) and follow the indicated steps.

## 6 - Running performance tests
- _Go again to the [WDC website](http://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page._
- _Download the normalized ```all_gs.json.gz``` and include this in the datasets folder._
- _Run ```create_dataset``` with the Golden Standard dataset._
- _Open a terminal, ```cd``` to the datasets directory and run <nobr>```gzip offers_gs.json```.</nobr>_
- _Run ```sort_offers``` with the newly created dataset.
- _Return to the terminal and run <nobr>```gzip offers_gs_sorted.json```.</nobr>_
- _To get the performance of the selected blocking algorithm, run ```blocker_performance.full_performance_scan```._
- _To get the performance of the matching algorithm, run the blocking algorithm again with the newly created dataset and write the blocks to a file with ```write_to_file```.
- _Next, run ```matcher_performance.full_performance_scan```._

## Including a new DBMS.
In case you want to benchmark a DBMS that is not yet included in this 
program, you need to do a couple of extra steps to prepare the program. 
When a non-PostgreSQL based DBMS is added, more steps are required.
For each option, the steps are listed below. Please also follow the
steps listed under 'any new DBMS' when including a non-PostgreSQL based
DBMS.

### Including any new DBMS.
As this program was written with PostgreSQL based systems in mind, 
no additional changes need to be made to the existing code base. For ease, a
placeholder NAME will be used, which denotes the name of the newly added DBMS.
Please add the following python file to prepare the dataset generation:
- ```database_filler_NAME.py```. The new probabilistic DBMS probably has its own unique structure when it comes to representing the probabilities and/or sentences of the possible worlds. As the dataset needs to be properly prepared for the new DBMS, functions need to be designed to tailor the produced dataset to the needs of the DBMS. For guidance, take a look at the functions in ```database_filler_dubio.py``` and ```database_filler_maybms.py``` to see what should be included in the newly created Python file.

### Including a new non-PostgreSQL based DBMS. 
As the database connection is established using the psycopg2 library, additional changes
to the code need to be made when wanting to use a non-PostgreSQL based system. 
The following adaptations to the code must be made:
- ```database.ini.tmpl```.
- ```database_filler.py```. Please read through the code and adapt the methods that do not support the other DMBS.
- ```instert_query.py```. The ```create()``` method also uses psycopg2 to connect to the database. This method should thus be adapted.


