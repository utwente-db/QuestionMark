# QuestionMark: The Probabilistic Benchmark


QuestionMark: The Probabilistic Benchmark is the Python program to benchmark any
probabilistic database management system. It currently provides support for 
[DuBio](https://github.com/utwente-db/DuBio) and [MayBMS](http://maybms.sourceforge.net/), but it can easily be
adapted to support any other probabilistic DBMS.

To run this benchmark, a dataset should be generated using
[QuestionMark: The Dataset Generator](https://gitlab.utwente.nl/s1981951/prob-matcher).
This program alters the WDC data corpus to include a probabilistic clustering. If no dataset 
has been created yet, please go to 
[QuestionMark: The Dataset Generator](https://gitlab.utwente.nl/s1981951/prob-matcher) and follow
the steps as indicated.


## About
QuestionMark: The Probabilistic Benchmark is the program that executes the benchmark test for any probabilistic database management system.
It contains a total of 17 benchmark queries and provides insights using 5 main metrics. 

<details>
<summary><b>What QuestionMark: The Probabilistic Benchmark does</b></summary>
<ul><li>For each query selected for the benchmarking process, the program first runs the query once to retrieve the results or catch any errors thrown. This first run also creates a warm start.</li>
    <li>Next, the query is run over the indicated number of iterations, to obtain an average runtime. The results retrieved per query are instantly written to QuestionMark_query_results.txt.</li>
    <li>When all queries have run, overarching metrics are calculated. The results of these are written to QuestionMark_metrics_results.txt.</li>
    <li>To digest the produced data to useful insights, the manual provided in the results section should be consulted.</li></ul>
</details>

<details>
<summary><b>Why use probabilistic database technology?</b></summary>
Having uncertain data treated in a deterministic manner ignores the many opportunities that treating that data in an indeterministic manner offers, and it might even lead to incorrect decisions due to incorrect data displaying. Probabilistic data processing can aid decisions in more scientific areas, such as bio-informatics and healthcare, but also adds value in various business processes, which rely on decisions based on data from different sources. 

To get uncertain data ready for deterministic decision-making, data cleaning is performed to remove inconsistencies in the data. This process consumes significant time, while the risk of making wrong decisions due to badly cleaned data is still present. Probabilistic data querying solves this issue. Being able to query raw business data in a probabilistic manner provides an improved information representation to base business intelligence decisions on. 

It is thus not the case that the availability of good quality probabilistic databases only aids the scientific world; on the contrary. A wide range of sectors could benefit from the use of probabilistic database management systems.
</details>

<details>
<summary><b>Parameter explanation</b></summary>
The following parameters are included in QuestionMark: The Probabilistic Benchmark. Their value can be changes in
parameters.py.
<ul><li><i>DBMS.</i> Determines the Database Management System that will be used for the execution of the benchmark. Additional systems can be added when support for them is also added to the benchmark program.</li>
    <li><i>Iterations.</i> Denotes the number of times a query is run to obtain a run time average from the queries. This is a global variable that is used for all queries. Increasing this number will provide a more precise outcome of the average run time, but at the cost of a longer benchmark execution time. The total number of iterations is always +1 to create a warm start.</li>
    <li><i>Show Query Plan.</i> Boolean value. If true, the query plan for each query is also provided with the benchmark result. Enabling this variable does not influence the execution time of the queries.</li>
    <li><i>Timeout.</i> Ensures that queries that take too long to return an answer will be aborted. Once a query times out, this will be noted in the benchmark result and the next query is started. </li>
    <li><i>Queries.</i> A list that contains all queries from the benchmark. Depending on the goal with which the benchmark is run, queries that are not relevant can be removed from the benchmark run. Removing queries lowers the total time required to run the benchmark.</li>
</ul>
</details>

<details>
<summary><b>Metric explanation</b></summary>
The following metrics are included in QuestionMark:
<ul><li><i>Brevity of the query dialect.</i>This metric gives insights into the succinctness of the query language. A more succinct query dialect often requires less time to write queries with and is often easier to understand. This metric value is obtained by iterating over all queries and adding their character count. Spaces are removed from the calculation. Optionally, characters can be removed from specific queries. For example in query IUD_1_rollback offers are added to the database. As the data the that represents the offer is not indicative of the complexity of the query language, the number of characters used for that representation is subtracted from the total character count for that query.</li>
    <li><i>Query functionality coverage.</i> This metric provides insight into the functionality coverage of the database system and is determined by multiple sub-metrics. When running the queries to obtain their results and runtime, it can happen that a specific functionality is not supported or the database system cannot handle the load required to execute the query. In these cases, the system returns an error. The error raised during execution are stored and printed as the query result. After the benchmark execution has finished, an overview table is created that indicates what queries finished execution and which threw an error. The percentage of successful queries is then also determined. For each query that threw an error, it also indicates what query functionality might be lacking. In each case, a critical look is needed to verify whether the error is thrown due to an actual lack of functionality support or due to another reason, for example a typo. With the gathered knowledge, the functionality coverage table can be manually filled in. In this table, a distinction is made between functionality that is natively supported and functionality that can be implemented with a workaround method. </li>
    <li><i>Runtime of queries.</i> This metric provides insight into the speed of query execution. A lower runtime is required to obtain higher query throughput rates and improves the flow of business processes relying on the query results. This metric is also obtained by a combination of sub-metrics. To obtain the runtime of a query, the PostgreSQL explain analyse statement is used. This statement returns the execution plan of various queries or statements and tracks its runtime. When available, it differentiates between the planning time and execution time of a query. In this distinction is not supported by the DBMS, only a total runtime is returned. For each query, the average runtime over the specified iterations is printed. Each query is run with a warm start. After all benchmark queries have run, a total average planning time and execution time, or total average runtime is calculated. This is the sum of all time averages of all queries. The total time provides a quick idea of the speed of the tested DBMS. For each application scenario, the acceptable runtime of a query differs. It is thus advised to verify the significance of the queries and per query determine the acceptable runtime. </li>
    <li><i>Probabilistic data overhead.</i> This metric represents the additional storage space required to store the probabilistic representation of the data. When processing large volumes of data, needing additional storage space to store the probabilistic representation of the data could get costly. As each probabilistic DBMS stores their probabilistic representation in a unique way, the probabilistic data overload is calculated for each DBMS differently. For both systems, the storage space used is determined by the pg_size_pretty statement of PostgreSQL. </li>
    <li><i>User friendliness.</i> User friendliness is another metric that is composed from several sub-metrics. As user friendliness is something of a more personal taste and cannot be measures from a benchmark run, all sub-metrics are in the form of statements that should be rated on a scale from 1 to 5. The statements can be found in the manual included in the results folder.</li>
</ul>
</details>


## Use
This project can be downloaded for use. Please check ```MANUAL.md``` for a roadmap on how
to run the benchmark tests.

This project may be adapted for own use. It is planned to release this work under a CC license.

Additional dialects could be added to wish. The queries in ```queries-pseudo-code.txt``` can be used for convenient 
translation to any other dialect. Currently, QuestionMark is built with PostgreSQL-based databases in mind. 
Additional changes need to be made to this program in case another database system needs to be supported.

## Contributors
This project is written by Nikki Zandbergen as part of her M.Sc. Computer Science thesis
at the University of Twente.
This project was supervised by Maurice van Keulen, Tom van Dijk and Jan Flokstra.

The thesis can be downloaded [here](#). (not yet published).