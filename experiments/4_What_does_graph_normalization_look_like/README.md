# What does graph normalization look like

In our experiments we looked at the original graph from the Offshore dataset and performed different normalizations with respect to different embeddings P and the corresponding gFDs 'Entity':P:X -> Y that hold.

In particular we looked at the following:

1.) P1 = {'jurisdiction_description', 'countries', 'service_provider', 'country_codes'} with the set of constraints:






2.) P2 = {'jurisdiction_description', 'valid_until', 'countries', 'sourceID', 'country_codes'} with the set of constraints:





3.) P3 = {'jurisdiction_description', 'service_provider', 'countries', 'valid_until', 'sourceID', 'country_codes'} which presents the union of P1 and P2 with the set of constraints:
