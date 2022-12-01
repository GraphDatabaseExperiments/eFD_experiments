# Manual to replicate experiments

This manual will provide a step by step guide on how to get set up to replicate the experiments discussed in our research.

In particular, this folder contains information on the following:

- instructions on how to set up Neo4j
- information on how to import dump files in Neo4j Desktop
- details on how to run Python in conjunction with Neo4j

## Setting up Neo4j: 

We will present two options to set up Neo4j. Using Neo4j Browser in an online environment called the [Neo4j Sandbox](https://neo4j.com/sandbox/) is the quickest and easiest way, yet will be limited to replicating experiments using the Offshore dataset. For full usability and to replicate all experiments discussed we show how to obtain [Neo4j Desktop](https://neo4j.com/download/) and set it up.

### Neo4j Sandbox:

To replicate the experiments using the Offshore dataset we recommend using the [Neo4j Sandbox](https://neo4j.com/sandbox/). By clicking the link and logging in the user will be able to create a project using one of Neo4j's sample datasets.

![Create new Sandbox project](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/sandbox1.JPG?raw=true)

Among these datasets is the ICIJ Offshore Leaks dataset.

![Create ICIJ Offshore project](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/sandbox2.JPG?raw=true)

Once created the user can open dataset using Neo4j Browser online

![Open Neo4j Broswer](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/sandbox3.JPG?raw=true)

and perform queries on the dataset.

![Perform queries](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/sandbox4.JPG?raw=true)

Now the user can perform the queries for the Offshore dataset as outlined in the [experiments folder](https://github.com/GraphDatabaseExperiments/normalization_experiments/tree/main/experiments/).

### Neo4j Desktop:

To gain full usability and replicate all experiments we recommend to download Neo4j Desktop. This can be obtained in Neo4j's official [Download Center](https://neo4j.com/download-center/#desktop). Detailed installation instructions can be found in [Neo4j Desktop's manual](https://neo4j.com/docs/desktop-manual/current/installation/). The manual also provides on overview of Neo4j Desktop's feautures in the [Visual Tour](https://neo4j.com/docs/desktop-manual/current/visual-tour/).

Once installed the user will have to open Neo4j Desktop and create a new project

![Create new project](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/desktop1.JPG?raw=true)

and within this project create a new local database.

![Create new database](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/desktop2.JPG?raw=true)



## Import dump files in Neo4j Desktop: 





## How to run Python and Neo4j using Neo4j Python Driver: 
