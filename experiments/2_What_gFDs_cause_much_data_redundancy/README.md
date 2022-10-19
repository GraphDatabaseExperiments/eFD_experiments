# What gFDs cause much data redundancy

Among the gFDs mined in our datasets we are particularly interested in the ones that cause high levels of redundancy. Information on these gFDs can guide the process of deciding which gFDs are consdidered to be meaningful and express business rules.

In the Offshore dataset there are many gFDs L:P:X ->Y causing high redundancy with the L = 'Entity', 'jurisdiction_description' as part of the property set X and 'jurisdiction' as part of Y. The difference in these gFDs are the additional properties in X or P\XY. This leds us to believe that these additional properties might filter out dirty data, i.e. nodes that violate the gFD 'Entity':'jurisdiction_description' -> 'jurisdiction'.

Performing the query

MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND EXISTS(e.jurisdiction)
WITH e.jurisdiction_description AS description, COUNT(DISTINCT(e.jurisdiction)) AS dist WHERE dist > 1
RETURN description, dist

shows 
