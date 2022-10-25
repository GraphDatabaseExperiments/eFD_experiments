# How do benefits of normalization scale

For the experiments on synthetic datasets we used Python along with Neo4j using the Neo4j Python Driver.

This folder contains the Python script used to execute the experiments on synthetic data and results from these experiments can be found in this folder. As graph databse we used an adaptation of a popular example from relational databases. Here we created a graph with one node labelled "Company" and multiple nodes connected to this one labelled "Employee". The employee-nodes have properties "name", "department" and "manager", with additional properties for certain experiment settings. Our underlying business rule says that every department has at most one manager which results in the gFD {Employee} : {department, manager} : {department} -> {manager}.

In each experiment setting, we perform a query on the same baseline graph and scale this graph by factor k to have k times as many Employee-nodes while keeping the number of departments fixed. In comparison we also execute the corresponding query on the normalized graph with respect to the gFD {Employee} : {department, manager} : {department} -> {manager} for certain experiment settings.


## How query performance scales

To showcase how the benifts of graph normalization scale with respect to updates we perform the two queries

```
MATCH (e:Employee) WITH e.department AS dept, COUNT(*) AS size RETURN min(size), max(size), avg(size)
```

on the baseline graph and

```
MATCH (d:Department) WITH SIZE([(d)--(e:Employee) | e]) AS dept RETURN min(dept), max(dept), avg(dept)
```

on the normalized graph with newly created nodes labelled "Department" carrying the properties "manager" and "department" that have been transferred from the Employee-nodes.

To illustrate the benefits of normalization on updates we compare the performance of the queries

```
MATCH (e:Employee) WHERE e.manager = 'Boss_0' SET e.manager = 'New_boss'
```

on the baseline graph compared to

```
MATCH (d:Department) WHERE d.manager = 'Boss_0' SET d.manager = 'New_boss'
```

on the normalized graph.







