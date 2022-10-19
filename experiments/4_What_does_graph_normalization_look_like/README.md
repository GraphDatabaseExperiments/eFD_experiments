# What does graph normalization look like

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
