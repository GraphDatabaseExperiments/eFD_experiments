# What does graph normalization look like

### Setting

In our experiments we looked at the original graph from the Offshore dataset and performed different normalizations with respect to the label L = 'Entity' and different embeddings P and the corresponding gFDs L:P:X -> Y that are satsified.

In particular we looked at the following property sets:

1.) P1 = {'jurisdiction_description', 'countries', 'service_provider', 'country_codes'} with constraints:

- L:P1: 'countries' -> 'country_codes'
- L:P1: 'country_codes' -> 'countries'


2.) P2 = {'jurisdiction_description', 'valid_until', 'countries', 'sourceID', 'country_codes'} with constraints:

- L:P2: 'countries', 'sourceID' -> 'country_codes'
- L:P2: 'country_codes', 'sourceID' -> 'countries'
- L:P2: 'countries', 'valid_until' -> 'country_codes'
- L:P2: 'country_codes', 'valid_until' -> 'countries'
- L:P2: 'countries', 'jurisdiction_description' -> 'country_codes'

3.) P3 = {'jurisdiction_description', 'service_provider', 'countries', 'valid_until', 'sourceID', 'country_codes'} which represents the union of P1 and P2 with constraints:

- L:P3: 'countries' -> 'country_codes'
- L:P3: 'country_codes' -> 'countries'
- L:P3: 'service_provider' -> 'sourceID'
- L:P3: 'service_provider' -> 'valid_until'
- L:P3: 'sourceID' -> 'valid_until'
- L:P3: 'valid_until' -> 'sourceID'


### Cyper queries:

To meassure the amount of redundancy caused by the given gFDs associated with P1 we can execute the following queries:

```
MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND
EXISTS(e.countries) AND
EXISTS(e.service_provider) AND
EXISTS(e.country_codes)
WITH e.countries AS countries, COUNT(e.countries) AS dist WHERE dist > 1
RETURN SUM(dist)
```

and

```
MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND
EXISTS(e.countries) AND
EXISTS(e.service_provider) AND
EXISTS(e.country_codes)
WITH e.country_codes AS codes, COUNT(e.country_codes) AS dist WHERE dist > 1
RETURN SUM(dist)
```


The Cypher queries to transform the original property graph into the normalized graph for the set P1 are as follows:

```
MATCH (e:Entity)
WHERE EXISTS(e.countries) AND EXISTS(e.country_codes) AND EXISTS(e.jurisdiction_description) AND EXISTS(e.service_provider)
WITH DISTINCT e.countries AS countries, e.country_codes as codes
CREATE (l:Location{countries: countries, country_codes: codes})
```

to create the new nodes with properties XY on them and

```
MATCH (e:Entity),(l:Location)
WHERE EXISTS(e.countries) AND EXISTS(e.country_codes) AND EXISTS(e.jurisdiction_description) AND EXISTS(e.service_provider) AND
e.countries = l.countries
CREATE (e)<-[:LOCATION_OF]-(l)
```

to create the edges between the new nodes and the original nodes. Finally we need to remove the respective properties from the original nodes using

```
MATCH (e:Entity)
WHERE EXISTS(e.countries) AND EXISTS(e.country_codes) AND EXISTS(e.jurisdiction_description) AND EXISTS(e.service_provider)
REMOVE e.countries, e.country_codes
```

which results in the normalized graph. Here we used meaningful labels for the newly created nodes and edges.
