# Manual

This file contains the roadmap on how QuestionMark: The Dataset Generator
 is to be used. 
_Explanation is displayed in italics_. 

Note that you are allowed to make changes to this program. 
Please follow the rules as provided by the CC license. 

## About QuestionMark: The Dataset Generator
QuestionMark: The Dataset Generator is the program that generates the dataset required to
run QuestionMark: The Probabilistic Benchmark. QuestionMark: The Dataset Generator creates an
adaptation of the WDC Product Data Corpus for Large-Scale Product Matching. 

<details>
<summary><b>Information on the WDC Dataset</b></summary>
This benchmark uses an adaptation of the WDC Product Data Corpus and Gold Standard for Large-Scale 
Product Matching, Version 2.0 as the dataset. From this data corpus, the normalised English offers dataset is adapted 
and used for this benchmark.

The WDC dataset is a large public training dataset for product matching. It is produced by extracting schema.org product 
descriptions from 79 thousand websites, which provides 26 million product offers. The English offers subset consists of 
16 million product offers. The dataset is provided with a clustering. The 16 million product offers in the English subset 
are categorized in 10 million clusters. Each cluster contains offers of the same product found on different websites. 
There are roughly 8.5 million clusters with size 1, one million clusters with size 2, and 400.000 clusters with size 3 or 4. 
Clusters of a size greater than 80 are filtered out of the dataset, as these are likely noise. Within the English offers 
dataset, each offer is represented as a JSON object. 

To obtain a dataset suited for use in this benchmark, the English offers subset from the WDC data corpus should be adapted. 
</details>

<details>
<summary><b>What QuestionMark: The Dataset Generator does</b></summary>
<ul><li>If it is indicated that a smaller dataset will be used, this new dataset is produced first. To do this, a pseudo-random selection of offers is chosen from the dataset. This ensures that the same dataset will be produced each time the benchmark is run on a specific size.</li>
    <li>Next, this dataset is sorted and a dictionary is created for easy lookup.</li>
    <li>The offers present in the dataset are then put in blocks. For this, two blocking algorithms are available. First creating blocks reduces the time required to evaluate if offers should be put in the same cluster.</li>
    <li>After the blocks are created, all offers in a block are matched and provided with a probability score. This probability indicates the likelihood that the offer belongs in a cluster, and whether its attributes are likely the correct ones.</li>
    <li>When the clusters are created, a database representation is created and the offers are added to a probabilistic DBMS.</li></ul>
</details>

<details>
<summary><b>Parameter explanation</b></summary>
The following parameters are included in QuestionMark: The Probabilistic Benchmark. Their value can be changes in
parameters.py.
<ul><li><i>DBMS.</i> Determines into which database management system the generated dataset should be loaded and what preparatory queries need to be run.</li>
    <li><i>Dataset Size.</i> Determines the amount of offers included in the dataset. A percentage of the dataset can be determined with up to two decimal places. The offers for the new smaller dataset are pseudo-randomly chosen, so that the same dataset is returned for multiple runs. This ensures reproducibility of the results. The full dataset contains 16451499 offers. The smallest dataset that can be generated is 0.01% of the full dataset, which produces an initial dataset of 1653 offers. The final probabilistic dataset that is generated from these offers contains 11\:807 records. This value should be carefully chosen, as this influences to what extent the produced dataset imitates the data being digested by the real-world application.</li>
    <li><i>Whole Clusters.</i> Determines whether the offers chosen from the larger dataset to include in the new smaller dataset are pulled from entire clusters or not. Including entire clusters increases the uncertainty of the data.</li>
    <li><i>Word Distance Measure.</i> Determines the way the distance between two words or sentences is calculated. This measure is used during the blocking phase on the attributes determined as Blocking Key Values and on all suitable attributes during the matching phase. The implemented distance measures are Levenshtein, Jaro, Jaro-Winkler, Hamming and Jaccard. </li>
    <li><i>Blocking Key Values.</i> Determines the attributes that are included to determine the similarity of two offers during the blocking phase. Including more attributes provides a better blocking performance, but at the cost of a higher run time.</li>
    <li><i>Blocking Similarity Threshold.</i> Value between 0 and 1 that represents the distance between two offers. Evaluated offers with a distance lower than the threshold are included in the same block.</li>
    <li><i>Blocking Window Size.</i> Determines the size of the sliding window. Within a window, the distance between the first and last offer is determined. This value influences the run time. </li>
    <li><i>Maximum Block Size.</i> Poses a restriction on the block size. Increasing this value improves the performance. As the matching phase includes a calculation with factorial time complexity, this size should not exceed seven. Six is advised.</li>
    <li><i>Matching Attributes.</i> Determines the attributes that are used to determine the distance between two offers during the matching phase. Including more attributes improves the performance, but increases the run time.</li>
    <li><i>Matching Attribute Weights.</i> Determines the weight of each attribute to calculate the final distance score. This can be tweaked to improve the performance. It has no effect on the run time. </li>
    <li><i>Upper Phi and Lower Phi.</i> Determines the upper and lower threshold of the distance measure. If the distance between two offers is greater than the upper phi, the two offers are certainly not the same product. If the distance is smaller than the lower phi, the two offers are certainly the same. Increasing the gap between the values ensures less false matches or non-matches, but increases the computational complexity in later phases and during querying. A smaller gap can be used to artificially reduce the uncertainty in the dataset. This value should be carefully chosen, as this influences to what extent the produced dataset imitates the data being digested by the real-world application.</li>
</ul>
</details>


## 1 - Downloading the WDC datasets
- Create an empty folder ```datasets``` in the main project repo.
- Go to the [WDC website](https://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page.
- Download ```offers_corpus_english_v2.json.gz``` and include this in the newly created datasets folder. Do not unzip this file.
- Optional: Download the samples to get an impression of the dataset structure.

## 2 - Preparing and running the dataset generator
- Open ```parameters.py``` and change the present parameters to the desired values. The file provides information on what the parameters are used for. Please check ```performance.txt``` to get an impression of how changing the parameters changes the performance.
- Create a file called ```database.ini``` and fill in the credentials following the structure of ```database.ini.tmpl```.
- Set up a functioning database connection to the probabilistic database management system of choice. 
- In case a new probabilistic DBMS will be benchmarked, please see the instructions on the bottom of this manual.
- Go to ```manual.py``` and run the script.

## 3 - Continue with benchmarking
- You now have your dataset prepared! You can continue with the benchmarking. Go to [QuestionMark: The Probabilistic Benchmark](https://gitlab.utwente.nl/s1981951/probabilistic-benchmark) and follow the indicated steps.
- You can also decide to measure the performance of QuestionMark: The Dataset Generator. In that case, please read the instructions below.

## Running performance tests
_To obtain a dataset that is nearing the specifications of any real-world dataset as much as possible, the parameters provided 
in this program should be tweaked. To obtain a first impression of the behaviour of the various parameters, several parameter settings
are already run and included in the ```performance``` folder. This step is thus not required for the
benchmarking process. If you desire to run such a test on the current parameter settings, 
please follow the following steps_:
- Go again to the [WDC website](http://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page.
- Download the normalized ```all_gs.json.gz``` and include this in the datasets folder.
- Go to ```parameters.py``` and set PERFORMANCE to True and set MEASURE to the correct value.
- Go to ```manual.py``` and run the script.
- Also here the execution is stopped to manually gzip the indicated file.
- The results of earlier performance tests can be found in ```performance.txt```.

## Including a new DBMS.
In case you want to benchmark a DBMS that is not yet included in this 
program, you need to do a couple of extra steps to prepare the program. 
When a non-PostgreSQL based DBMS is added, more steps are required.
For each option, the steps are listed below. Please also follow the
steps listed under 'any new DBMS' when including a non-PostgreSQL based
DBMS.

<details>
<summary><b>Included Database Management Systems</b></summary>
<ul><li>MayBMS</li>
    <li>DuBio</li></ul>
</details>

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


