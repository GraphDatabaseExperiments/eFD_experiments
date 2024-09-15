'''
Graph Database experiments on normalisation
'''



from unicodedata import is_normalized

from neo4j import GraphDatabase, basic_auth
from py2neo import Graph, Node, Relationship

import xlsxwriter # writing to excel

from datetime import datetime





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

    summary = result.consume().profile

    #print(summary)

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
    local_bolt = <local_bolt>
    local_pw = <password>
    local_user = "neo4j"

    # Initialise DB
    new_db = gdbms_test(local_bolt, local_user, local_pw)
        

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

    #####################################################################################
    query = query_offshore_northwind_denormalized

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

        #print()
        print(f"{runs-i-1} more experiments to go...")
        #print()

    db_times.sort()

    print(db_hits)
    print(db_times)
    print(db_times[outliers:-outliers])
    average_time = round(sum(db_times[outliers:-outliers])/(1000000*(runs - 2*outliers)), precision)
    print(average_time)

    # closing db
    new_db.close()

    # Experiment results
        
    # Details need more info on normalized or not, how many attributes (later on)
    filename = "Experiments_running_times_" + str(today) + "---" + str(current) + ".xlsx"
    sheetname = "Experiment"
    experiment_name = is_normalized*"Normalised " + (not is_normalized)*"Denormalized " + dataset + with_index*(" with index") + (not with_index)*(" without index")

    experiment_details = [query]
    
    # create content depending on whether normalised or denormalised instance (add redundancy)
    content = [["query_times (ms):"] + list(map(lambda n : round(n/1000000, precision), db_times[outliers:-outliers])), ["average (ms):"] + [average_time]]

    # writing to file
    write_to_excel(filename, sheetname, experiment_name, experiment_details, content)


main()




