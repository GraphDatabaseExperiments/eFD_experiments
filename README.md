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








## Experiments:

The experiments in our research on gFDs/gUCs and graph databse normalization are subsummed in the following sections providing answers to the corresponding questions:

- 1.) What gFDs do graphs exhibit?
- 2.) What gFDs cause much data redundancy?
- 3.) How much inconsistency can gFDs avoid?
- 4.) What does graph normalization look like?
- 5.) How does integrity management improve?
- 6.) How do aggregate queries improve?
- 7.) How do benefits of normalization scale?


Detailed information on the results of these experiments and instructions on how to replicate them can be found in this repository in the experiments folder. In what follows we like to provide an overview on the different experiments.

### 1.) What gFDs do graphs exhibit?

In these experiments we mined the gFDs L:P:X -> Y present in the datasets and listed them with information on the additional properties P\XY in the embedding P, the properties on the left hand side X as well as the right hand side Y. In addition, we gave insight into the redundancy they cause as well as the maximum inconsistency each gFD exhibits.

### 2.) What gFDs cause much data redundancy?

In the context of normalization an important goal is to minimize redundancy and in order to achieve this we are interested in gFDs that cause high levels of redundancy. For our experiments we ordered gFDs in the datasets with respect to the redundancy they cause and further analyzed those that appar to be meaningful.

### 3.) How much inconsistency can gFDs avoid?

Fill

### 4.)

Fill

### 5.)

Fill

### 6.)

Fill

### 7.)

Fill




