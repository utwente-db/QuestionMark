# Probabilistic-benchmark Manual

This file contains the roadmap on how this project is to be used. 
_Explanation is displayed in italics_. 

Note that you are allowed to make changes to this program. 
Please follow the rules as provided by the CC license. 

## 1 - Prepare the dataset
- In case no dataset has been prepared yet, go to 
[QuestionMark: The Dataset Generator](https://gitlab.utwente.nl/s1981951/prob-matcher) and follow the manual to 
prepare the dataset that is to be used for this benchmark.

## 2 - Prepare the benchmark
- It is expected that a functioning database connection is set up.
- Create a file called ```database.ini``` and fill in the credentials following the structure of ```database.ini.tmpl```.
Open ```parameters.py``` and change the present parameters to the desired values. The file provides information on what the parameters are used for. 
Also take a good look at what queries you want to include in the benchmark execution.
- Go to ```manual.py```.
- To test the connection, run ```test_connection```.

## 3 - Run the benchmark
- Go to ```manual.py``` and run ```run_benchmark```.

## 4 - Reading the results
- _The benchmark produces two result sheets: ```QuestionMark_metrics_results.txt``` and ```QuestionMark_query_results.txt```. The first file contains all information on the metric data collected. The second file provides an overview of all the query results and runtimes._
- The manual of QuestionMark: The Probabilistic Benchmark provides clear instructions on how to interpret the results. You can find this manual in the results folder.
- You have now finished the benchmarking procedure!

## Including a new DBMS.
In case you want to benchmark a DBMS that is not yet included in this program,
you need to de a couple of extra steps to prepare the program. For this, a distinction
is made between PostgreSQL-based Database Management Systems and non-PostgreSQL based
systems. For a non-PostgreSQL based system, please also follow the steps listed under 
the PostgreSQL based system.

### Including any new DBMS.
When including any new DBMS, the following simple changes need to be
made to this program. For ease, a placeholder NAME will be used, which 
denotes the name of the newly added DBMS. Please add the following 
functions and variables to prepare the benchmark:
- ```queries_NAME.py``` and ```queries_NAME_prepare.py```. To include a new DBMS, the first step is to include the queries in the corresponding dialect. To do this, create two new files. The first file, ```queries_NAME.py```, contains the benchmark queries. The second file, ```queries_NAME_prepare.py```, contains queries needed to prepare the benchmark. To see what queries should be included, ```queries_pseudo_code```, ```queries_MayBMS.py``` and ```queries_DuBio.py``` can be used as a translation guide. Please stick to the structure used in these files.
- ```connect_db.py```. This file is responsible for sending the queries to the DBMS. In this file, include ```from queries_NAME import NAME_QUERIES_DICT```. In ```execute_query()```, also include the DBMS in the first if-statement. Finally, check if the execution time returned by the DBMS follows the pattern from MayBMS or from DuBio. When the DBMS uses PostgreSQL 10 or higher, the default can be used.
- ```output_tui.py```. This file prints the benchmark output. In ```create_result_file()```, add the new DBMS in the if-statement. 
- ```parameters.py```. Include the new DBMS as an option of the DBMS variable.
- ```perpare_benchmark.py```. This file runs the preparatory queries. In this file, include ```from queries_NAME_prepare import NAME_PREPARE_DICT```. In ```prepare_benchmark()```, include the new DBMS in the if-statement. 

### Including a new non-PostgreSQL based DBMS. 
As the database connection is established using the psycopg2 library, 
additional changes to the code need to be made when wanting to use a 
non-PostgreSQL based system. The following adaptations to the code 
must be made:
- ```connect_db.py```. This file also establishes the connection with the database. Please read through all functions and change the code where needed. 
- ```database.ini.tmpl```.
- ```prepare_benchmark.py```. Also here psycopg2 is used for the database connection. Both functions need to be adapted.
- ```run_benchmark.py```. This is the main file to run the benchmark. Also here psycopg2 is used. The present function thus needs to be adapted.
