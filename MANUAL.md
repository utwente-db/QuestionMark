# Manual

This file contains the roadmap on how QuestionMark: The Dataset Generator
 is to be used. 
_Explanation is displayed in italics_. 

Note that you are allowed to make changes to this program. 
Please follow the rules as provided by the CC license.

## 1 - Downloading the WDC datasets
- Create an empty folder ```datasets``` in the main project repo.
- Go to the [WDC website](https://webdatacommons.org/largescaleproductcorpus/v2/index.html) and scroll to the bottom of the page.
- Download ```offers_corpus_english_v2.json.gz``` and include this in the newly created datasets folder. Do not unzip this file.
- Optional: Download the samples to get an impression of the dataset structure.

## 2 - Preparing and running the dataset generator
- Open ```parameters.py``` and change the present parameters to the desired values. The file provides information on what the parameters are used for. Please check ```performance/performance.txt``` to get an impression of how changing the parameters changes the performance.
- Create a file called ```database.ini``` and fill in the credentials following the structure of ```database.ini.tmpl```.
- Make sure the database management system of choice is running and is accepting connections.
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


