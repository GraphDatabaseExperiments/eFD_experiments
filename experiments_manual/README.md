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

The two datasets used in the experiments can be found as dump files using the following links:

- https://github.com/neo4j-graph-examples/northwind/blob/main/data/northwind-43.dump

- https://github.com/ICIJ/offshoreleaks-data-packages/blob/main/data/icij-offshoreleaks-42.dump


To import these files using Neo4j Desktop the user will have to follow these steps.

1.) Click on 3 dots that appear on the right when hovering over the database name.

2.) The dump files need to be copied to the folder that opens when clicking "Open Folder" in the dropdown menu that appears when clicking the 3 dots. Alternatively the user can click on "Add" and then on the drop down menu choose "File".

3.) Once the dump file appears under Files then depending on the operating system the user could click on 3 dots next to the dump file and chose "Create new DBMS from dump" or the user might have to click on the 3 dots on the right when hovering over the database name, open the terminal and follow the instructions to import a dump file as shown in the [Neo4j Operation's manual](https://neo4j.com/docs/operations-manual/current/backup-restore/restore-dump/).
These steps are also explained in this [helpful video](https://www.youtube.com/watch?v=HPwPh5FUvAk).

To troubleshoot any issues we refer to to the [Neo4j Community Forum](https://community.neo4j.com/t5/graphacademy-discussions/cannot-create-new-database-from-dump-file/td-p/39914) as well. 

Once the dump file is loaded into the local DBMS instance the user can explore the database by hovering over the database name, clicking on "Start" and choose the option to open the database using Neo4j Browser.

![Open in Neo4j Browser](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/desktop3.JPG?raw=true)

## First experiments:

Once Neo4j is set up the user will be able to replicate the experiments carried out in our research. The experiments on the Offshore leaks dataset can be carried out without much prior preparation by using the Neo4j Sandbox. For instructions on how to set up the Neo4j Sandbox we please see the previous section. For the experiments on the Northwind data the user will have to set up Neo4j Desktop and import the respective dump file as outlined above. For experiments on synthetic data the user will need Neo4j Desktop and install the Neo4j Python Driver which will be explained further below.

The first experiment to carry out is to gather the information for the inconsistency profile for the Offshore leaks dataset. For this the user will have to open the database using Neo4j Browser (Sandbox or Desktop) and perform the following query

'''
MATCH (e:Entity) WHERE
EXISTS(e.jurisdiction_description) AND EXISTS(e.jurisdiction)
WITH e.jurisdiction_description AS description, COUNT(DISTINCT(e.jurisdiction)) AS dist
RETURN description, dist
'''

which will yield the result illustrated below.

![First query](https://github.com/GraphDatabaseExperiments/normalization_experiments/blob/main/experiments_manual/images/desktop5.JPG?raw=true)


## How to run Python and Neo4j using Neo4j Python Driver:

For the experiments on synthetic datasets we used Python and connected to a Neo4j database using the Neo4j Python Driver. For installation instructions and some sample code fragments we refer the user to the [Neo4j Python Driver Manual](https://neo4j.com/docs/api/python-driver/current/).




