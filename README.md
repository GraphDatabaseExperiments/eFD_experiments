# Normalizing Graph Data

## Introduction: 

This Github repository complements our research on property graph normalization with graph-tailored uniqueness contraints (gUC) and graph-tailored functional dependencies (gFD) as foundation.

In particular, this repository is comprised of the following:

- experiment results on synthetic and real world datasets
- links to dump files (Neo4j format) containing the real world datasets used to conduct experiments
- source code (written in Python) that outlines how experiments on synthetic datasets have been conducted
- images illustrating the experiments on graph datasets
- files and instructions on how to replicate experiments



## Preliminaries:

The software used to perform the experiments carried out in our research are:

- Neo4j Desktop 1.5.0

- Neo4j Browser 5.0.0

- Neo4j Python Driver 5.1.0

- Python 3.9.13


The real world graph datasets (Northwind and Offshore Leaks) provided as dump files for import in Neo4j that we use in our experiments can be found in the following Github repositories:


- https://github.com/neo4j-graph-examples/northwind/blob/main/data/northwind-43.dump

- https://github.com/ICIJ/offshoreleaks-data-packages/blob/main/data/icij-offshoreleaks-42.dump


To reproduce the experiments in our research the user will need to download the dump files for the datasets used and obtain the software as outlined above which is available for free through official websites. For detailed instructions on how to reproduce the experiment results on synthetic and real world datasets we refer to the experiments folder in this repository.


## Experiments:

The experiments in our research on gFDs/gUCs and graph databse normalization are subsummed in the following sections providing answers to the corresponding questions:

- 1.) [What gFDs do graphs exhibit?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/1_What_gFDs_do_graphs_exhibit)
- 2.) [What gFDs cause much data redundancy?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/2_What_gFDs_cause_much_data_redundancy)
- 3.) [How much inconsistency can gFDs avoid?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/3_How_much_inconsistency_can_gFDs_avoid)
- 4.) [What does graph normalization look like?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/4_What_does_graph_normalization_look_like)
- 5.) [How does integrity management improve?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/5_How_does_integrity_management_improve)
- 6.) [How do aggregate queries improve?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/6_How_do_aggregate_queries_improve)
- 7.) [How do benefits of normalization scale?](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/7_How_do_benefits_of_normalization_scale)


Detailed information on the results of these experiments and instructions on how to replicate them can be found in this repository in the experiments folder or by clicking on the links above. In what follows we like to provide an overview on the different experiments.

### 1.) What gFDs do graphs exhibit?

In these experiments we mined the gFDs L:P:X -> Y present in the datasets and listed them with information on the additional properties P\XY in the embedding P, the properties on the left hand side X as well as the right hand side Y. In addition, we gave insight into the redundancy they cause as well as the maximum inconsistency each gFD exhibits.

### 2.) What gFDs cause much data redundancy?

In the context of normalization an important goal is to minimize redundancy and in order to achieve this we are interested in gFDs that cause high levels of redundancy. For our experiments we ordered gFDs in the datasets with respect to the redundancy they cause and further analyzed those that appar to be meaningful.

### 3.) How much inconsistency can gFDs avoid?

In order to determine how much inconsistency gFDs avoid we investigated gFDs causing high redundancy and used the following approach in our experiments. While these gFDs L:P:X -> Y are satisfied there appear to be gFDs that are meaningful and might represent business rules that are violated, but by adding properties to P or X these result in gFDs that are among those that are satisfied and cause many occurences of redundant property values. Here we could interpret the additional properties to add to X or P to transform a violated gFD into one that is satisfied as a filter with respect to nodes carrying dirty data. Further analysis of these nodes that cause the violations gives insight into whether these gFDs don't represent business rules or if these are sources of inconsistency.   

### 4.) What does graph normalization look like?

To illustrate what graph normalization looks like we used three different property sets P1, P2 as well as their union (denoted by P3) and looked at the gFDs that hold with respect to a given label set L and each of these property sets Pi. Next, we transformed each time the set of gFDs that cause high redundancy into gUCs that avoid redundancy. This approach garantees the set of constraints to be in L:Pi:BCNF with all redundancy eliminated. In our experiments we performed the proposed graph transformations and meassured the amount of database hits and time required.

### 5.) How does integrity management improve?

The benefits of normalization become obvious when updating properties on the right hand side of gFDs L:P:X -> Y with many redundant property occurences. To highlight how integrity management improves through normalization of property graphs we executed update queries on instances of the original property graph in our datasets and the corresponding queries on the normalized instances of these graphs where the gFD has been transormed into the gUC L:XY:X. In our experiments we performed update queries for property values that present minimal, average and maximum inconsistency. In addition we performed these queries on the original and normalized instances each time with and without an index on the property set X. 

### 6.) How do aggregate queries improve?

To show how the performance of aggregate queries improves through the proposed normalization approach we conducted the following experiments. We performed aggregate queries on the original graphs in our datasets and the resulting normalized graph and compared their performance each time with and without and index on the property set X.

### 7.) How do benefits of normalization scale?

To answer the question of how the benefits of normalization scale we conducted experiments on synthetic datasets. Here we looked at proptery graphs that exhibit a gFD that is satisfied. By increasing the amount of nodes by a given factor we scaled these graphs and analyzed each time the original graph as well as the normalized counterpart. In each experiment we performed queries to validate that the given gFD holds in the original graph and that the resulting gUC is satisfied in the corresponding normalized graph. In addtion, we performed these queries where we changed parameters such as the label set L, the size of the embedding P and the ratio of P-complete nodes. Moreover, we analyzed how the performance of update and aggreation queries scales. 



