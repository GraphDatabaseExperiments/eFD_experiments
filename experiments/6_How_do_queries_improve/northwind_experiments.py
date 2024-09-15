'''
Graph Database experiments on normalisation
'''



from unicodedata import is_normalized

from neo4j import GraphDatabase, basic_auth
from py2neo import Graph, Node, Relationship

import xlsxwriter # writing to excel

from datetime import datetime
import time





# databse class
class gdbms_test:


    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def reset(self):
        with self.driver.session() as session:
            session.run("MATCH (m) DETACH DELETE m")

    def execute_query(self, query):
        with self.driver.session() as session:
            session.run(query)

    def execute_query_with_output(self, query):
        with self.driver.session() as session:
            record = session.run(query)
        return record


    def execute_query_with_output_result(self, query):
        with self.driver.session() as session:
            record = session.run(query)
            return [dict(i) for i in record]
        


########################

# write to excel file

def write_to_excel(filename, sheetname, experiment_name, heading: list, content: list):

    # create sheet
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(sheetname)
    
    # write experiment name
    worksheet.write(0,0, experiment_name)

    
    # write heading (list), give information on variables, etc
    row_start = 2

    for row in range(len(heading)):
            worksheet.write(row_start + row, 0, heading[row])

    # write content (content list of iterables)
    row_start += (2 + len(heading))
    column_start = 0

    for row in range(len(content)):
        for column in range(len(content[row])):
            worksheet.write(row_start + row, column_start + column, content[row][column])

    # close workbook
    workbook.close()




####################################################

# performing queries



def show_query_details(database, query):

    
    new_db = database
    
    result = new_db.execute_query_with_output(query)

    summary = result.consume()

    summary = summary.profile

    return  (sum_db_hits(summary), sum_time(summary))


# getting db_hits

def sum_db_hits(profile):
    return (profile.get("dbHits", 0) + sum(map(sum_db_hits, profile.get("children", []))))


# getting execution time

def sum_time(profile):
    return (profile.get("time", 0) + sum(map(sum_time, profile.get("children", []))))



#########################

# main function

def main():

    #local bolt and http port, etc:

    local_bolt = "bolt://localhost:11009"
    #local_http = "http://localhost:7474"
    local_pw = "Pskav752$api"
    local_user = "neo4j"


    # Initialise DB
    new_db = gdbms_test(local_bolt, local_user, local_pw)
        

    # Northwind operations
    #
    ###################

    # Northwind update queries

    query_northwind_update_denormalized_max = """PROFILE MATCH (o:Order) WHERE
                                            EXISTS(o.customerID) AND
                                            EXISTS(o.shipCity) AND
                                            EXISTS(o.shipName) AND
                                            EXISTS(o.shipPostalCode) AND
                                            EXISTS(o.shipCountry) AND
                                            EXISTS(o.shipAddress) AND
                                            EXISTS(o.shipRegion) AND
                                            o.customerID = 'SAVEA'
                                            SET o.shipCountry = 'United States'"""
    
    query_northwind_update_denormalized_avg = """PROFILE MATCH (o:Order) WHERE
                                            EXISTS(o.customerID) AND
                                            EXISTS(o.shipCity) AND
                                            EXISTS(o.shipName) AND
                                            EXISTS(o.shipPostalCode) AND
                                            EXISTS(o.shipCountry) AND
                                            EXISTS(o.shipAddress) AND
                                            EXISTS(o.shipRegion) AND
                                            o.customerID = 'SEVES'
                                            SET o.shipCountry = 'United Kingdom'"""



    query_northwind_update_denormalized_min = """PROFILE MATCH (o:Order) WHERE
                                            EXISTS(o.customerID) AND
                                            EXISTS(o.shipCity) AND
                                            EXISTS(o.shipName) AND
                                            EXISTS(o.shipPostalCode) AND
                                            EXISTS(o.shipCountry) AND
                                            EXISTS(o.shipAddress) AND
                                            EXISTS(o.shipRegion) AND
                                            o.customerID = 'CENTC'
                                            SET o.shipCountry = 'Estados Unidos Mexicanos'"""
    


    query_northwind_update_normalized_max = """PROFILE MATCH (c:Customer) WHERE 
                                            EXISTS(c.customerID) AND
                                            EXISTS(c.shipCity) AND
                                            EXISTS(c.shipName) AND
                                            EXISTS(c.shipPostalCode) AND
                                            EXISTS(c.shipCountry) AND
                                            EXISTS(c.shipAddress) AND
                                            EXISTS(c.shipRegion) AND
                                            c.customerID = 'SAVEA'
                                            SET c.shipCountry = 'United States'"""
    
    query_northwind_update_normalized_avg = """PROFILE MATCH (c:Customer) WHERE 
                                            EXISTS(c.customerID) AND
                                            EXISTS(c.shipCity) AND
                                            EXISTS(c.shipName) AND
                                            EXISTS(c.shipPostalCode) AND
                                            EXISTS(c.shipCountry) AND
                                            EXISTS(c.shipAddress) AND
                                            EXISTS(c.shipRegion) AND
                                            c.customerID = 'SEVES'
                                            SET c.shipCountry = 'United Kingdom'"""
    
    query_northwind_update_normalized_min = """PROFILE MATCH (c:Customer) WHERE 
                                            EXISTS(c.customerID) AND
                                            EXISTS(c.shipCity) AND
                                            EXISTS(c.shipName) AND
                                            EXISTS(c.shipPostalCode) AND
                                            EXISTS(c.shipCountry) AND
                                            EXISTS(c.shipAddress) AND
                                            EXISTS(c.shipRegion) AND
                                            c.customerID = 'CENTC'
                                            SET c.shipCountry = 'Estados Unidos Mexicanos'"""
    

    # Northwind aggregate queries

    query_northwind_aggregate_denormalized = """PROFILE MATCH (o:Order) WHERE
                                            EXISTS(o.customerID) AND
                                            EXISTS(o.shipCity) AND
                                            EXISTS(o.shipName) AND
                                            EXISTS(o.shipPostalCode) AND
                                            EXISTS(o.shipCountry) AND
                                            EXISTS(o.shipAddress) AND
                                            EXISTS(o.shipRegion)
                                            WITH o.customerID AS orders, COUNT(*) AS amount
                                            RETURN min(amount), max(amount), avg(amount)"""

    query_northwind_aggregate_normalized = """PROFILE MATCH (c:Customer) WHERE
                                            EXISTS(c.customerID) AND
                                            EXISTS(c.shipCity) AND
                                            EXISTS(c.shipName) AND
                                            EXISTS(c.shipPostalCode) AND
                                            EXISTS(c.shipCountry) AND
                                            EXISTS(c.shipAddress) AND
                                            EXISTS(c.shipRegion)
                                            WITH SIZE((c)--()) AS amount
                                            RETURN min(amount), max(amount), avg(amount)"""
    

    # Northwind distinct queries

    query_northwind_distinct_denormalized = """PROFILE MATCH (o:Order) WHERE
                                            EXISTS(o.customerID) AND
                                            EXISTS(o.shipCity) AND
                                            EXISTS(o.shipName) AND
                                            EXISTS(o.shipPostalCode) AND
                                            EXISTS(o.shipCountry) AND
                                            EXISTS(o.shipAddress) AND
                                            EXISTS(o.shipRegion)
                                            RETURN DISTINCT(o.customerID)"""
    

    query_northwind_distinct_normalized = """PROFILE MATCH (c:Customer) WHERE
                                            EXISTS(c.customerID) AND
                                            EXISTS(c.shipCity) AND
                                            EXISTS(c.shipName) AND
                                            EXISTS(c.shipPostalCode) AND
                                            EXISTS(c.shipCountry) AND
                                            EXISTS(c.shipAddress) AND
                                            EXISTS(c.shipRegion)
                                            RETURN DISTINCT(c.customerID)"""
    

    # Northwind insertion operations

    query_northwind_insertion_denormalized_1 =   """PROFILE MERGE (o:Order{orderID: 99999, customerID: "SAVEA", shipCity: "Boise", shipName: "Save-a-lot Markets", shipPostalCode: 83720, shipCountry: "USA", shipAddress: "187 Suffolk Ln.", shipRegion: "ID"})
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
                                                    """
    
    query_northwind_insertion_denormalized_2 =  """PROFILE MERGE (o:Order{orderID: 99999, customerID: "new", shipCity: "new", shipName: "new", shipPostalCode: 99999, shipCountry: "new", shipAddress: "new", shipRegion: "new"})
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
                                                """

    query_northwind_insertion_denormalized_3 = "MATCH (o:Order{orderID: 99999}) DELETE o"


    query_northwind_insertion_normalized_1 = "PROFILE MATCH (c:Customer{customerID: 'SAVEA'}) MERGE (o:Order{orderID: 99999})<-[r:PURCHASED]-(c)"
    
    query_northwind_insertion_normalized_2 = "PROFILE MERGE (o:Order{orderID: 99999})<-[r:PURCHASED]-(c:Customer{customerID: 'new', shipCity: 'new', shipName: 'new', shipPostalCode: 99999, shipCountry: 'new', shipAddress: 'new', shipRegion: 'new'})"

    query_northwind_insertion_normalized_3 = "MATCH (o:Order{orderID: 99999}) OPTIONAL MATCH (c:Customer{customerID: 'new'}) DETACH DELETE o,c"








    # Offshore operations
    #
    ###################


    # Offshore update queries

    query_offshore_update_denormalized_max = """PROFILE MATCH (e:Entity)
                                            WHERE EXISTS(e.service_provider) AND EXISTS(e.sourceID) AND EXISTS(e.valid_until)
                                            AND e.service_provider = 'Mossack Fonseca'
                                            SET e.valid_until = 'The Panama Papers data is current through 2016'"""

    query_offshore_update_denormalized_avg = """PROFILE MATCH (e:Entity)
                                            WHERE EXISTS(e.service_provider) AND EXISTS(e.sourceID) AND EXISTS(e.valid_until)
                                            AND e.service_provider = 'Portcullis Trustnet'
                                            SET e.valid_until = 'The Offshore Leaks data is current through 2011'"""
    
    query_offshore_update_denormalized_min = """PROFILE MATCH (e:Entity)
                                            WHERE EXISTS(e.service_provider) AND EXISTS(e.sourceID) AND EXISTS(e.valid_until)
                                            AND e.service_provider = 'Appleby'
                                            SET e.valid_until = 'Appleby data is current through 2015'"""


    query_offshore_update_normalized_max = """PROFILE MATCH (p:Provider)
                                            WHERE EXISTS(p.service_provider) AND EXISTS(p.sourceID) AND EXISTS(p.valid_until)
                                            AND p.service_provider = 'Mossack Fonseca'
                                            SET p.valid_until = 'The Panama Papers data is current through 2016'"""
    
    query_offshore_update_normalized_avg = """PROFILE MATCH (p:Provider)
                                            WHERE EXISTS(p.service_provider) AND EXISTS(p.sourceID) AND EXISTS(p.valid_until)
                                            AND p.service_provider = 'Portcullis Trustnet'
                                            SET p.valid_until = 'The Offshore Leaks data is current through 2011'"""
    
    query_offshore_update_normalized_min = """PROFILE MATCH (p:Provider)
                                            WHERE EXISTS(p.service_provider) AND EXISTS(p.sourceID) AND EXISTS(p.valid_until)
                                            AND p.service_provider = 'Appleby'
                                            SET p.valid_until = 'Appleby data is current through 2015'"""
    



    # Offshore aggregate queries
    
    query_offshore_aggregate_denormalized = """PROFILE MATCH (e:Entity) WHERE
                                            EXISTS(e.service_provider) AND EXISTS(e.sourceID) AND EXISTS(e.valid_until)
                                            WITH e.service_provider AS provider, COUNT(*) AS amount
                                            RETURN min(amount), max(amount), avg(amount)
                                            """



    query_offshore_aggregate_normalized = """PROFILE MATCH (p:Provider) WHERE
                                            EXISTS(p.service_provider) AND EXISTS(p.sourceID) AND EXISTS(p.valid_until)
                                            WITH SIZE((p)--()) AS amount
                                            RETURN min(amount), max(amount), avg(amount)
                                            """
    


    # Offshore distinct queries

    query_offshore_distinct_denormalized = """PROFILE MATCH (e:Entity) WHERE
                                            EXISTS(e.service_provider) AND EXISTS(e.sourceID) AND EXISTS(e.valid_until)
                                            RETURN DISTINCT(e.service_provider)
                                            """
    

    query_offshore_distinct_normalized = """PROFILE MATCH (p:Provider) WHERE
                                            EXISTS(p.service_provider) AND EXISTS(p.sourceID) AND EXISTS(p.valid_until)
                                            RETURN DISTINCT(p.service_provider)
                                            """
    


    # Offshore insertion operations (no difference between min / avg / max size of equivalence classes unlike in update)   

    query_offshore_insertion_denormalized_1 =   """PROFILE MERGE (e:Entity{name: 'new', service_provider: 'Mossack Fonseca', sourceID: 'Panama Papers', valid_until: 'The Panama Papers data is current through 2015'})
                                                WITH e AS newnode
                                                CALL{
                                                MATCH (e:Entity) WHERE
                                                e.service_provider IS NOT NULL AND
                                                e.sourceID IS NOT NULL AND
                                                e.valid_until IS NOT NULL
                                                WITH e.service_provider AS provider, COUNT(DISTINCT(e.sourceID + e.valid_until)) AS amount
                                                WHERE amount > 1
                                                RETURN provider, amount
                                                }
                                                DELETE newnode
                                                """
    
    query_offshore_insertion_denormalized_2 =   """PROFILE MERGE (e:Entity{name: 'new', service_provider: 'new', sourceID: 'new', valid_until: 'new'})
                                                WITH e AS newnode
                                                CALL{
                                                MATCH (e:Entity) WHERE
                                                e.service_provider IS NOT NULL AND
                                                e.sourceID IS NOT NULL AND
                                                e.valid_until IS NOT NULL
                                                WITH e.service_provider AS provider, COUNT(DISTINCT(e.sourceID + e.valid_until)) AS amount
                                                WHERE amount > 1
                                                RETURN provider, amount
                                                }
                                                DELETE newnode
                                                """
    
    query_offshore_insertion_denormalized_3 = "MATCH (e:Entity{name: 'new'}) DELETE e"



    query_offshore_insertion_normalized_1 = "PROFILE MATCH (p:Provider{service_provider: 'Mossack Fonseca'}) MERGE (e:Entity{name: 'new'})<-[r:PROVIDED_TO]-(p)"
    
    query_offshore_insertion_normalized_2 = "PROFILE MERGE (e:Entity{name: 'new'})<-[r:PROVIDED_TO]-(p:Provider{service_provider: 'new', sourceID: 'new', valid_until: 'new'})"

    query_offshore_insertion_normalized_3 = "MATCH (e:Entity{name: 'new'}) OPTIONAL MATCH (p:Provider{service_provider: 'new'}) DETACH DELETE e,p"
    
    



    #####################################################################################
    #####################################################################################
    query = query_northwind_distinct_denormalized

    is_normalized = False

    with_index = False

    dataset = "Northwind"
    #####################################################################################



    db_hits = []
    db_times = []

    runs = 20

    outliers = 5

    precision = 2



    today = datetime.now().strftime("%Y_%m_%d")
    current = datetime.now().strftime("%H_%M_%S")

    for i in range(0, runs):
        

        # perform query and meassure db hits

        current_details = show_query_details(new_db, query)
        db_hits.append(current_details[0])
        db_times.append(current_details[1])


        # comment in for deletion of new nodes and adjust depending dataset and on normalisation for insertion experiments
        #
        #new_db.execute_query(query_offshore_insertion_denormalized_3)
        #new_db.execute_query(query_offshore_insertion_normalized_3)
        #
        #new_db.execute_query(query_northwind_insertion_denormalized_3)
        #new_db.execute_query(query_northwind_insertion_normalized_3)



        #print()
        print(f"{runs-i} more experiments to go...")
        #print()

    db_times.sort()
    db_hits.sort()

    print(db_hits)
    print(db_times)
    print()

    db_times = db_times[outliers:-outliers]
    db_hits = db_hits[outliers:-outliers]
    
    
    print(db_hits)
    print(db_times)
    average_time = round(sum(db_times)/(1000000*(runs - 2*outliers)), precision)
    average_db_hits = round(sum(db_hits)/(runs - 2*outliers))
    print()
    
    print(average_db_hits)
    print(average_time)

    # closing db
    new_db.close()

    # Experiment results
        
    # Details need more info on normalized or not, how many attributes (later on)
    filename = "Experiments_running_times_" + str(today) + "---" + str(current) + ".xlsx"
    sheetname = "Experiment"
    experiment_name = is_normalized*"Normalized " + (not is_normalized)*"Denormalized " + dataset + with_index*(" with index") + (not with_index)*(" without index")

    experiment_details = [query]
    
    # create content depending on whether normalised or denormalised instance (add redundancy)
    content = [["query_db_hits:"] + db_hits + [""] + ["average:", average_db_hits], ["query_times (ms):"] + list(map(lambda n : round(n/1000000, precision), db_times)) + [""] + ["average (ms):", average_time]]

    # writing to file
    write_to_excel(filename, sheetname, experiment_name, experiment_details, content)


main()




