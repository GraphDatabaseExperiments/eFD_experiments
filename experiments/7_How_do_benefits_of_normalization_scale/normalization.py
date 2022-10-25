'''
Graph Database experiments on normalisation


from sqlite3 import DatabaseError

import random # used to split up departments randomly
import math # math module
from unicodedata import is_normalized

from neo4j import GraphDatabase, basic_auth
from py2neo import Graph, Node, Relationship

import matplotlib.pyplot as plt

import xlsxwriter # writing to excel

import time # use for benchmarking code and finding bottlenecks





# databse class
class gdbms_test:


    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, name):
        cypher_query = "CREATE (p:Person {name: '" + name + "'})"
        print(cypher_query)
        with self.driver.session() as session:
            session.run(cypher_query)

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





##############################################
# create database


# method to create db_instance
def create_db_instance(database, people_per_department: list, department_distribution:list , is_normalised: bool, different_labels: bool, labels_distribution: list, properties: list):

    # check input fits
    if len(people_per_department) != len(department_distribution):
        raise Exception("Input lengths not matching")
    ######### ask someone to do this nicer in one if statement
    for percentage in department_distribution:
        if percentage < 0 or percentage > 1:
            raise Exception("Distribution below 0 or above 1")
    
    new_db = database

    # wipe clean
    new_db.reset()

    # queries for creating db


    # create company
    create_company = "CREATE (c:Company {ceo: 'Homer', companyName: 'ACME', founded: 2000})"
    new_db.execute_query(create_company)

    
    # create vertices
    if is_normalised:
        create_normalised(new_db, people_per_department, department_distribution)
    else:
        create_denormalised(new_db, people_per_department, department_distribution, different_labels, labels_distribution, properties)


# submethods used in create_db_instance

def create_denormalised(database, people_per_department, department_distribution, different_labels, labels_distribution, properties):
    
    new_db = database

    default_value = "new"

    # create vertices
    for dept in range(len(people_per_department)):

        with_skills = round(people_per_department[dept] * department_distribution[dept])
        
        if different_labels:
            employee_of_the_month = round(labels_distribution[0] * people_per_department[dept])
            amount_person = round((1 / labels_distribution[1]) * people_per_department[dept])

            if employee_of_the_month > with_skills:
                raise Exception("Too many employee of the month relative to skilled")

        if different_labels:
            create_departments_skills_eom = "UNWIND range(1," + str(employee_of_the_month) + ") AS vertices CREATE(e:Employee:EoM:Person{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_ " + str(dept) +  " ',department:'Department_" + str(dept) + "', skills:'Department_" + str(dept) + "_Pro'})"
            
            create_departments_skills = "UNWIND range(" + str(employee_of_the_month + 1) + "," + str(with_skills) + ") AS vertices CREATE(e:Employee:Person{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_ " + str(dept) +  " ',department:'Department_" + str(dept) + "', skills:'Department_" + str(dept) + "_Pro'})"
            create_departments_no_skills = "UNWIND range(" + str(with_skills + 1) + ", " + str(people_per_department[dept]) + ") AS vertices CREATE(e:Employee:Person{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_" + str(dept) +  "',department:'Department_" + str(dept) + "'})"
            
            # create non-employee person with property status 'retired' / seems to add additional dbhits for EXISTS filter
            # create_departments_retired = "UNWIND range(" + str(people_per_department[dept] + 1) + ", " + str(amount_person) + ") AS vertices CREATE(e:Person{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_" + str(dept) +  "',department:'Department_" + str(dept) + "', status: 'retired'})"
            create_departments_retired = "UNWIND range(" + str(people_per_department[dept] + 1) + ", " + str(amount_person) + ") AS vertices CREATE(e:Person{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_" + str(dept) +  "',department:'Department_" + str(dept) + "'})"
            

            new_db.execute_query(create_departments_skills_eom)
            
            new_db.execute_query(create_departments_skills)
            new_db.execute_query(create_departments_no_skills)

            new_db.execute_query(create_departments_retired)
        else:
            create_departments_skills = "UNWIND range(1," + str(with_skills) + ") AS vertices CREATE(e:Employee{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_ " + str(dept) +  " ',department:'Department_" + str(dept) + "', skills:'Department_" + str(dept) + "_Pro'})"
            create_departments_no_skills = "UNWIND range(" + str(with_skills + 1) + ", " + str(people_per_department[dept]) + ") AS vertices CREATE(e:Employee{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_" + str(dept) +  "',department:'Department_" + str(dept) + "'})"
            new_db.execute_query(create_departments_skills)
            new_db.execute_query(create_departments_no_skills)

        ######### this needs replacing with a single query
        #t0 = time.perf_counter()
        for prop in range(len(properties)):

            with_properties = round(properties[prop] * people_per_department[dept])

            #for j in range(1, with_properties + 1):
                #replace query within loop with one query using unwind
                # update = "MATCH (n) WHERE n.name = 'New_Department_" + str(dept) + "_Employee_" + str(j) + "' SET n.property_" + str(prop) + " = '" + default_value + "'"
            
            # commented out for the moment
            # update = "UNWIND range(1, " + str(with_properties) + ") AS vertices MATCH (n:Employee) WHERE n.name = 'New_Department_" + str(dept) + "_Employee_' +toString(vertices) SET n.property_" + str(prop) + " = '" + default_value + "'"
            
            # just included for one additional property and all nodes possess this
            update = "MATCH (n:Employee) SET n.property_" + str(prop) + " = '" + default_value + "'"

            # UNWIND range(0, " + str(len(people_per_department)) +") 
            new_db.execute_query(update)
        #t = time.perf_counter()
        #print(f"{round(t - t0, 3)} milliseonds for prop update")

    

    # create relationships
    create_relationships = "MATCH (e:Employee), (c:Company) CREATE (e)-[:WORKS_FOR]->(c)"
    new_db.execute_query(create_relationships)




# transfrom denromalised instance into normalised with respect to one particular eFD

def normalise_db_fd(database):

    new_db = database

    create_depts = "MATCH (e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.skills) WITH DISTINCT e.department AS depts, e.manager AS mgrs CREATE (d:Department {dept: depts, manager: mgrs})"
    
    # important: check if normaising works corectly if X -> Y, but not Y -> X, i.e. for example if we have Sales / Sarah, Marketing / Sarah as well

    create_rel_and_remove_properties = "MATCH (e:Employee),(d:Department) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.skills) AND e.department = d.dept WITH e AS emp, d AS dpt CREATE (emp)-[:IN_DEPARTMENT]->(dpt) REMOVE emp.manager, emp.department"
    
    new_db.execute_query(create_depts)

    new_db.execute_query(create_rel_and_remove_properties)



####################################################

# performing queries



def show_dbhits(database, query):

    
    new_db = database
    
    result = new_db.execute_query_with_output(query)

    summary = result.consume().profile


    return  sum_db_hits(summary)


# getting db_hits

def sum_db_hits(profile):
    return (profile.get("dbHits", 0) + sum(map(sum_db_hits, profile.get("children", []))))



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


########################

# create random department sizes for fixed amount
def split_up(total, slots):
    result = [0]*slots
    slow_start = 0
    while total > 0:
        if slow_start <= 4:
            amount = random.randrange(1, math.ceil(0.2*(total + 1)))
        else:
            amount = random.randrange(1,total + 1)
        slot = random.randrange(0,slots)
        result[slot] += amount
        total -= amount
        slow_start += 1
    return result


#################################################

# functions to generate queries



# embedding / existence check

def add_embedding_check(node_variable, embeddings: list):
    embeddings_query_list = []
    for embedding in embeddings:
        embeddings_query_list.append("EXISTS(" + node_variable + "." + embedding + ")")
    return " AND ".join(embeddings_query_list)



#########################

# main function

def main():

    #local bolt and http port, etc:
    local_bolt = "bolt://localhost:7687" #alternative same as original: original stopped working
    local_http = "http://localhost:7474"
    local_pw = "Pskav752$api"
    local_user = "neo4j"

    # Initialise DB
    new_db = gdbms_test(local_bolt, local_user, local_pw)
        
    # perform experiment multiple times
    runs = 6
    for i in range(1, runs):
        # perform experiment for different scaling factors
        #factors = [1,2,5,10,25,50,100,250,500,1000]
        factors = [1,2]
        #departments = [10, 15, 10, 20, 40, 25, 30]
        departments = [1,4,2]
        #departments = split_up(150, 5)
        distribution = [1]*len(departments)
        labels_distribution = [0.25, 0.8] # what percentage of employees are empl of the month and what percentage of person are employees / !!!!currently assume labels_distribution[0] , min(distribution)
        properties = [1,1] # computationally costly, especially the more additional properties included

        dbhits = []
        redundancy = []

        # different queries for experiments
        aggregate_norm_query = "PROFILE MATCH (d:Department) WITH SIZE([(d)--(e:Employee) | e]) AS dept RETURN min(dept), max(dept), avg(dept)"
        aggregate_denorm_query = "PROFILE MATCH (e:Employee) WITH e.department AS dept, COUNT(*) AS size RETURN min(size), max(size), avg(size)"

        
        #verify_efd_denorm_query_1 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_efd_denorm_query_2 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_efd_denorm_query_3 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_efd_denorm_query_4 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) AND EXISTS(e.skills) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_efd_denorm_query_list = [verify_efd_denorm_query_1, verify_efd_denorm_query_2, verify_efd_denorm_query_3, verify_efd_denorm_query_4]
        verify_efd_denorm_query = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) AND EXISTS(e.skills) RETURN e.department, COUNT (DISTINCT e.manager)"
        verify_euc_norm_query = "PROFILE MATCH(d:Department) WHERE EXISTS(d.manager) AND EXISTS(d.dept) RETURN d.dept, COUNT(d)"
        
        #trade_off_update_denorm = "PROFILE MATCH (e:Employee) WHERE e.manager = 'Boss_" + str(i-1) +"' SET e.manager = 'New_boss'"
        trade_off_update_denorm = "PROFILE MATCH (e:Employee) WHERE e.manager = 'Boss_0' SET e.manager = 'New_boss'"
        trade_off_update_norm = "PROFILE MATCH (d:Department) WHERE d.manager = 'Boss_0' SET d.manager = 'New_boss'"

        trade_off_query_denorm = "PROFILE MATCH (e:Employee) WHERE e.department = 'Department_1' AND e.name = 'New_Department_1_Employee_2' RETURN e"
        trade_off_query_norm = "PROFILE MATCH (e:Employee)-[IN_DEPTARTMENT]->(d:Department) WHERE d.dept = 'Department_1' AND e.name = 'New_Department_1_Employee_2' RETURN e"

        # naive approach to counting redundancy: trivial not regarded and assumed full redundancy
        count_redundancy = "MATCH (e:Employee) WHERE EXISTS (e.name) AND EXISTS (e.department) AND EXISTS (e.manager) AND EXISTS (e.skills) WITH e.name AS redundancy RETURN COUNT(redundancy) AS redundant"

        # queries to meassure impact of labels EoM subseteq Empoloyee subseteq Person (Person includes nodes that aren't employees with status 'retired')
        impact_lables_eom_verify_efd_denorm_query = "PROFILE MATCH(e:EoM) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        impact_lables_employee_verify_efd_denorm_query = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        impact_lables_person_verify_efd_denorm_query = "PROFILE MATCH(e:Person) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"

        
        #query_list = [impact_lables_eom_verify_efd_denorm_query, impact_lables_employee_verify_efd_denorm_query, impact_lables_person_verify_efd_denorm_query]


        # test impact of different embeddings on queries for denormalised instance
        embedding = ['name', 'department', 'manager', 'skills']
        additional_embedding = ['property_' + str(k) for k in range(len(properties))]
        embedding += additional_embedding
        embedding = embedding[:1 + i]

        query_denorm = "PROFILE MATCH (e:Employee) WHERE " + add_embedding_check('e', embedding) + " AND e.department = 'Department_1' AND e.name = 'New_Department_1_Employee_2' RETURN e"

        print()
        print(query_denorm)
        print()

        query = query_denorm
        is_normalized = False
        different_labels = False


        for factor in factors:
            # create db instance

            #create_db_instance(new_db, departments, distribution, is_normalised = is_normalized)
            create_db_instance(new_db, [factor * x for x in departments], distribution, is_normalised = is_normalized, different_labels = different_labels, labels_distribution = labels_distribution, properties = properties)

            # perform query and meassure db hits
            current_dbhits = show_dbhits(new_db, query)
            dbhits.append(current_dbhits)

            # meassure E-redundancy (only in denormalised instance)
            if not is_normalized:
                current_redundancy = new_db.execute_query_with_output_result(count_redundancy)[0]['redundant']
                redundancy.append(current_redundancy)

                # Nice to leave to see exp is running
                print(f"Redundancy is: {current_redundancy}")
            
            # Nice to leave to see exp is running
            ###print(f"DbHits are: {current_dbhits}")
        # Nice to leave to see exp is running
        print()
        print(f"{runs-i-1} more experiments to go...")
        print()
        

        # Experiment results
        # Details need more info on normalized or not, how many attributes (later on)
        filename = "Test" + str(i) + ".xlsx"
        sheetname = "Experiment"
        experiment_name = is_normalized*"Normalised" + (not is_normalized)*"Denormalized" + " database with " + str(len(departments)) + " departmens and the following details:"

        experiment_details = ["Dept_Size: " + str(departments), "Distribution: " + str(distribution), query]
        
        # create content depending on whether normalised or denormalised instance (add redundancy)
        if not is_normalized:
            content = [["Scaling"] + factors ,["DbHits"] + dbhits, ["Redundancy"] + redundancy]
        else:
            content = [["Scaling"] + factors ,["DbHits"] + dbhits]

        # writing to file
        write_to_excel(filename, sheetname, experiment_name, experiment_details, content)

    '''
    # plotting graph
    for i in range(len(factors)):
        print(str(factors[i]) + " --- " + str(dbhits[i]))

    plt.plot(factors, dbhits)
    plt.xlabel('Sacling factor')
    plt.ylabel('Database hits')
    plt.show()

    '''


    # closing db
    new_db.close()


main()




