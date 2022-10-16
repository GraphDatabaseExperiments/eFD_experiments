# Normalizing Graph Data

## Introduction:

This Github repository complements our research on property graph normalization with graph-tailored uniqueness contraints (gUC) and graph-tailored functional dependencies (gFD) as foundation.

In particular, this repository is comprised of the following:

- source code (written in Python) that outlines how experiments on synthetic datasets have been conducted
- images illustrating the experiments on graph datasets
- links to dump files (Neo4j format) containing the real world datasets used to conduct experiments
- files and instructions on how to replicate experiments



## Preliminaries:

What software, files, etc needed to perform experiments

The software used to perform the experiments carried out in our research are:

- Neo4j Desktop 1.5.0

- Python 3.x



## Experiments:

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




