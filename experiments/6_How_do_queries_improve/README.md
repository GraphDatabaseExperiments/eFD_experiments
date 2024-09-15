# How do queries improve

In our experiments to illustrate the benefits of normalization to the execution of aggregation queries we look again at the Northwind dataset with respect to the gFD 'Order':'customerID','shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion' : 'customerID' -> 'shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion'.

Here we look at the performancance of the query

```
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
WITH o.customerID AS orders, COUNT(*) AS amount
RETURN min(amount), max(amount), avg(amount)
```

which provides information on the minimum, average and maximum amount of orders associated with the values for the property 'customerID'. We then compare these results to the performance of the corresponding query on the normalized (with respect to the gFD mentioned above) graph

```
MATCH (c:Customer) WHERE
EXISTS(c.customerID) AND
EXISTS(c.shipCity) AND
EXISTS(c.shipName) AND
EXISTS(c.shipPostalCode) AND
EXISTS(c.shipCountry) AND
EXISTS(c.shipAddress) AND
EXISTS(c.shipRegion)
WITH SIZE((c)--()) AS amount
RETURN min(amount), max(amount), avg(amount)
```

We proceeded in a similar fashion for the experiments in the Offshore dataset and for further details we refer to the files in this folder.

In the journal version of our research we performed additional queries involving the DISTINCT operation. For this we executed the query

```
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
RETURN DISTINCT(o.customerID)
```

in the orginal Northwind graph and

```
MATCH (c:Customer) WHERE
EXISTS(c.customerID) AND
EXISTS(c.shipCity) AND
EXISTS(c.shipName) AND
EXISTS(c.shipPostalCode) AND
EXISTS(c.shipCountry) AND
EXISTS(c.shipAddress) AND
EXISTS(c.shipRegion)
RETURN DISTINCT(c.customerID)
```

in the normalized graph. We proceeded in a similar fashion with these experiments in the Offshore graph and the files provided in this folder provide further information on this.


