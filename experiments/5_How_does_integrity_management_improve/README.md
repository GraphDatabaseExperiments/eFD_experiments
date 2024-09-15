# How does integrity management improve

The aim of graph normalization is minimizing and ideally eliminating the occurence of redundant data occurences. Using our notions of gFDs and gUCs this can be achieved by transforming a redundancy causing gFD into a gUC that holds on the newly created nodes. As a result we won't have to update multiple occurences of a property value of one of the properties in Y for a gFD L:P:X -> Y which can be huge for gFDs causing high redundancy.

In our experiments we looked at the Northwind dataset with respect to the gFD 'Order':'customerID','shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion' : 'customerID' -> 'shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion'

Here we want to perform updates for all nodes carrying the label 'Order' that are complete with respect to the properties outlined in the gFD above and have a particular customerID. In particular we want to update one of the values on the right hand side of the gFD, in our experiment, the value for the property 'shipCountry'.

We looked at different scenarios with respect to the amount of redundant value occurences. This means we chose nodes with values of 'customerID' that have minimal, average and maximum number of redundant property values on the right hand side of the gFD.

For this we performed the queries

```
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion) AND
o.customerID = 'SAVEA'
SET o.shipCountry = 'United States'
```

```
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion) AND
o.customerID = 'SEVES'
SET o.shipCountry = 'United Kingdom'
```

```
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion) AND
o.customerID = 'CENTC'
SET o.shipCountry = 'Estados Unidos Mexicanos'
```

on the original graph and meassured their performance in contrast to the queries

```
MATCH (c:Customer) WHERE 
EXISTS(c.customerID) AND
EXISTS(c.shipCity) AND
EXISTS(c.shipName) AND
EXISTS(c.shipPostalCode) AND
EXISTS(c.shipCountry) AND
EXISTS(c.shipAddress) AND
EXISTS(c.shipRegion) AND
c.customerID = 'SAVEA'
SET c.shipCountry = 'United States'
```

```
MATCH (c:Customer) WHERE 
EXISTS(c.customerID) AND
EXISTS(c.shipCity) AND
EXISTS(c.shipName) AND
EXISTS(c.shipPostalCode) AND
EXISTS(c.shipCountry) AND
EXISTS(c.shipAddress) AND
EXISTS(c.shipRegion) AND
c.customerID = 'SEVES'
SET c.shipCountry = 'United Kingdom'
```

```
MATCH (c:Customer) WHERE 
EXISTS(c.customerID) AND
EXISTS(c.shipCity) AND
EXISTS(c.shipName) AND
EXISTS(c.shipPostalCode) AND
EXISTS(c.shipCountry) AND
EXISTS(c.shipAddress) AND
EXISTS(c.shipRegion) AND
c.customerID = 'CENTC'
SET c.shipCountry = 'Estados Unidos Mexicanos'
```

on the normalized graph with respect to the gFD 'Order':'customerID','shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion' : 'customerID' -> 'shipCity', 'shipName', 'shipPostalCode', 'shipCountry', 'shipAddress', 'shipRegion'.

In the case of the Offshore dataset we performed experiments in a similar fashion and for further details on these experiments we refer to the files in this folder.

In the journal version of our research we performed insertions of new nodes under two scenarios where one time we inserted new nodes with already existing values for properties XY of respective equivalence classes associated with dependencies that hold and one time new nodes with new values for these properties.

More specifically, in the case of the Northwind dataset we inserted new nodes in the original graph using the Cypher operation

```
MERGE (o:Order{orderID: 99999, customerID: "SAVEA", shipCity: "Boise", shipName: "Save-a-lot Markets", shipPostalCode: 83720, shipCountry: "USA", shipAddress: "187 Suffolk Ln.", shipRegion: "ID"})
WITH o AS newnode
CALL{
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
WITH o.customerID AS ids, COUNT(DISTINCT(o.shipCity + o.shipName + o.shipPostalCode + o.shipCountry + o.shipAddress + o.shipRegion)) AS amount
WHERE amount > 1
RETURN ids, amount
}
DELETE newnode
```

which represents a node insertion for already existing values of XY and for the insertion of nodes with completely new values we used

```
MERGE (o:Order{orderID: 99999, customerID: "new", shipCity: "new", shipName: "new", shipPostalCode: 99999, shipCountry: "new", shipAddress: "new", shipRegion: "new"})
WITH o AS newnode
CALL{
MATCH (o:Order) WHERE
EXISTS(o.customerID) AND
EXISTS(o.shipCity) AND
EXISTS(o.shipName) AND
EXISTS(o.shipPostalCode) AND
EXISTS(o.shipCountry) AND
EXISTS(o.shipAddress) AND
EXISTS(o.shipRegion)
WITH o.customerID AS ids, COUNT(DISTINCT(o.shipCity + o.shipName + o.shipPostalCode + o.shipCountry + o.shipAddress + o.shipRegion)) AS amount
WHERE amount > 1
RETURN ids, amount
}
DELETE newnode
```
These operations include the validation of currently existing constraints and a rejection of the insertion in case this constraint is violated after insertion of the new node. In the Offshore dataset we performed experiments in a similar fashion and for further details on this we refer to the files in this folder.
