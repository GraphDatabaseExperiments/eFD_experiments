# What gFDs cause much data redundancy

Among the gFDs mined in our datasets we are particularly interested in the ones that cause high levels of redundancy. Information on these gFDs can guide the process of deciding which gFDs are consdidered to be meaningful and express business rules.

In the Offshore dataset there are many gFDs L:P:X ->Y causing high redundancy with the L = 'Entity', 'jurisdiction_description' as part of the property set X and 'jurisdiction' as part of Y. The difference in these gFDs are the additional properties in X or P\XY. This leds us to believe that these additional properties might filter out dirty data, i.e. nodes that violate the gFD 'Entity':'jurisdiction_description' -> 'jurisdiction'.

Performing the query

```
MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND EXISTS(e.jurisdiction)
WITH e.jurisdiction_description AS description, COUNT(DISTINCT(e.jurisdiction)) AS dist
RETURN description, dist
```

confirms that the gFD 'Entity':'jurisdiction_description' -> 'jurisdiction' is violated and provides insight into how many distinct values of 'jurisdiction' exist for the same value of the property 'jurisdiction_description'. This query shows the follwoing:

- 52 values of jurisdiction_description' with each no more than one distinct value of 'jurisdiction' associated
- 25 values of jurisdiction_description' with each two distinct values of 'jurisdiction' associated
- 8 values of jurisdiction_description' with each three distinct values of 'jurisdiction' associated

This inconsistency profile and digging deeper into the data performing queries such as

```
MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND EXISTS(e.jurisdiction)
AND e.jurisdiction_description = 'Bahamas' 
RETURN DISTINCT e.jurisdiction
```

leads us to believe this might not be a meaningful gFD.
