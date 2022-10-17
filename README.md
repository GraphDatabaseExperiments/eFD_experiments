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

### 1.)



Fill this section with overview on experiments


--------------------

Get rid of what is below


Which experiments have been conducted, enumerate and refer to files to replicate them.

### 1. Experiments on synthetic graph dataset

Explain experiments on synthetic dataset



### 2. Northwind graph dataset

This dataset contains information on customers and the order they made.

Nodes:
Edges:

Explain experiments



Queries performed:


Validation of gFD on denormalised graph:

MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
WITH o.customerID AS ids, COUNT(DISTINCT(o.shipCity)) AS dist1, COUNT(DISTINCT(o.shipName)) AS dist2, COUNT(DISTINCT(o.shipPostalCode)) AS dist3, COUNT(DISTINCT(o.shipCountry)) AS dist4, COUNT(DISTINCT(o.shipAddress)) AS dist5, COUNT(DISTINCT(o.shipRegion)) AS dist6
WHERE dist1 > 1 OR dist2 > 2 OR dist3 > 1 OR dist4 > 1 OR dist5 > 1 OR dist6 > 1 
RETURN ids, dist1, dist2, dist3, dist4, dist5, dist6


Updating customer nodes and remove properties from order vertices (no need to create new nodes and label for normalization here)


MATCH (o:Order),(c:Customer) WHERE
EXISTS(c.customerID) AND
EXISTS(o.customerID) AND
(o.customerID = c.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
SET c.shipCity = o.shipCity
REMOVE o.shipCity
SET c.shipName = o.shipName
REMOVE o.shipName
SET c.shipPostalCode = o.shipPostalCode
REMOVE o.shipPostalCode
SET c.shipCountry = o.shipCountry
REMOVE o.shipCountry
SET c.shipAddress = o.shipAddress
REMOVE o.shipAddress
SET c.shipRegion = o.shipRegion
REMOVE o.shipRegion
REMOVE o.customerID



Queries for aggregation:


Aggregate query denormalised


MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion) AND
WITH o.customerID AS orders, COUNT(*) AS amount
RETURN min(amount), max(amount), avg(amount)



----------------


Aggregate query normalised


MATCH (c:Customer) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion) AND
WITH SIZE((c)--()) AS amount
RETURN min(amount), max(amount), avg(amount)




Update queries:






### 2. Offshore leaks graph dataset

This dataset contains information on companies worldwide.

Explain experiments




