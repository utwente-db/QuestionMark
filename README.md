# QuestionMark: The Dataset Generator

QuestionMark: The Dataset Generator is a Python program to create 
a dataset for probabilistic product matching. This dataset is required to run the benchmark 
test with [QuestionMark: The Probabilistic Benchmark](https://gitlab.utwente.nl/s1981951/probabilistic-benchmark).
For more information on the added value of probabilistic databases, please also consult this
other program.

The dataset created by this program is an adaptation of the 
[WDC Product Data Corpus for Large-Scale Product Matching](https://webdatacommons.org/largescaleproductcorpus/v2/index.html) 
dataset. The clustering provided by this original dataset is removed and a new probabilistic
clustering is introduced.

## About
QuestionMark: The Dataset Generator is the program that generates the dataset required to
run QuestionMark: The Probabilistic Benchmark. QuestionMark: The Dataset Generator creates an
adaptation of the WDC Product Data Corpus for Large-Scale Product Matching. 

<details>
<summary><b>What QuestionMark: The Dataset Generator does</b></summary>
<ul><li>If it is indicated that a smaller dataset will be used, this new dataset is produced first. To do this, a pseudo-random selection of offers is chosen from the dataset. This ensures that the same dataset will be produced each time the benchmark is run on a specific size.</li>
    <li>Next, this dataset is sorted and a dictionary is created for easy lookup.</li>
    <li>The offers present in the dataset are then put in blocks. For this, two blocking algorithms are available. First creating blocks reduces the time required to evaluate if offers should be put in the same cluster.</li>
    <li>After the blocks are created, all offers in a block are matched and provided with a probability score. This probability indicates the likelihood that the offer belongs in a cluster, and whether its attributes are likely the correct ones.</li>
    <li>When the clusters are created, a database representation is created and the offers are added to a probabilistic DBMS.</li></ul>
</details>

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
<summary><b>Parameter explanation</b></summary>
The following parameters are included in QuestionMark: The Dataset Generator. Their value can be changes in
parameters.py.
<ul><li><i>DBMS.</i> Determines into which database management system the generated dataset should be loaded and what preparatory queries need to be run.</li>
    <li><i>Dataset Size.</i> Determines the number of offers included in the dataset. A percentage of the dataset can be determined with up to two decimal places. The offers for the new smaller dataset are pseudo-randomly chosen, so that the same dataset is returned for multiple runs. This ensures reproducibility of the results. The full dataset contains 16451499 offers. The smallest dataset that can be generated is 0.01% of the full dataset, which produces an initial dataset of 1653 offers. The final probabilistic dataset that is generated from these offers contains 11\:807 records. This value should be carefully chosen, as this influences to what extent the produced dataset imitates the data being digested by the real-world application.</li>
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

## Use
This project can be downloaded for use. Please check ```MANUAL.md``` for a roadmap on how
to generate the datasets with the desired size and amount of uncertainty.

QuestionMark © 2023 by the University of Twente is licensed under CC BY 4.0 (Attribution 4.0 International).

## Contributors
This project is written by Nikki Zandbergen as part of her M.Sc. Computer Science thesis
at the University of Twente.
This project was supervised by Maurice van Keulen, Tom van Dijk and Jan Flokstra.

The thesis can be downloaded [here](#). (not yet published).
