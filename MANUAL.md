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
<summary<b>Parameter explanation</b></summary>
The following parameters are included in QuestionMark: The Dataset Generator. Their value can be changes in
parameters.py.
<ul><li><i>DBMS.</i> Determines the Database Management System that will be used for the execution of the benchmark. Additional systems can be added when support for them is also added to the benchmark program.</li>
    <li><i>Iterations.</i> Denotes the amount of times a query is run to obtain a run time average from the queries. This is a global variable that is used for all queries. Increasing this number will provide a more precise outcome of the average run time, but at the cost of a longer benchmark execution time. The total amount of iterations is always +1 to create a warm start.</li>
    <li><i>Show Query Plan.</i> Boolean value. If true, the query plan for each query is also provided with the benchmark result. Enabling this variable does not influence the execution time of the queries.</li>
    <li><i>Timeout.</i> Ensures that queries that take too long to return an answer will be aborted. Once a query times out, this will be noted in the benchmark result and the next query is started. </li>
    <li><i>Queries.</i> A list that contains all queries from the benchmark. Depending on the goal with which the benchmark is run, queries that are not relevant can be removed from the benchmark run. Removing queries lowers the total time required to run the benchmark.</li>
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
- You can also decide to measure the performance of QuestionMark: The Dataset Generator. In that case, go to step 5.

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


