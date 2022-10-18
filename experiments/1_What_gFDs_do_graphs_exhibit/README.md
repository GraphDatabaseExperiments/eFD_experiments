# What gFDs do graphs exhibit

To showcase the relevance of our research on the proposed graph-tailored functional dependencies and uniqueness constraints we performed a quantitative analysis of real world graph datasets by mining the gFDs that are satsified by the respective property graphs for a given label. In the Norhtwind dataset we chose the label 'Order' and in the Offshore dataset we chose 'Entity'. The gFDs L:P:X -> Y we mined are minimal in the sense that removing a property from P or X will result in a violation.

We created a profile for the gFDs in each dataset by counting the amount of gFDs that are satisfied for different sizes of P. For each size of P we again distinguished between trivial gFDs (where P = XY) and nontrivial gFDs (where P contains additional properties).

