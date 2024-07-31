'''
Graph Database experiments on normalization
'''


import random # used to split up departments randomly
import math # math module

from neo4j import GraphDatabase, basic_auth
from py2neo import Graph, Node, Relationship

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
    for percentage in department_distribution:
        if percentage < 0 or percentage > 1:
            raise Exception("Distribution below 0 or above 1")
    
    new_db = database

    # wipe database clean
    new_db.reset()

    # queries for creating db


    # create company node
    create_company = "CREATE (c:Company {ceo: 'Homer', companyName: 'ACME', founded: 2000})"
    new_db.execute_query(create_company)

    
    # create nodes
    if is_normalised:
        create_normalised(new_db, people_per_department, department_distribution)
    else:
        create_denormalised(new_db, people_per_department, department_distribution, different_labels, labels_distribution, properties)


# submethods used in create_db_instance

# create baseline graph instance
def create_denormalised(database, people_per_department, department_distribution, different_labels, labels_distribution, properties):
    
    new_db = database

    default_value = "new"

    # create nodes
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
            
            # create non-employee person with property status 'retired' / adds additional dbhits for EXISTS filter
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

        for prop in range(len(properties)):

            update = "MATCH (n:Employee) SET n.property_" + str(prop) + " = '" + default_value + "'"

            new_db.execute_query(update)

    
    # create relationships
    create_relationships = "MATCH (e:Employee), (c:Company) CREATE (e)-[:WORKS_FOR]->(c)"
    new_db.execute_query(create_relationships)


# create normalized instance
def create_normalised(database, people_per_department, department_distribution): #different_lables so far no application in normalised DB as eFDs only evaluated for denormalised instance
    new_db = database

    # create vertices
    for dept in range(len(people_per_department)):
        with_skills = round(people_per_department[dept] * department_distribution[dept])
        create_departments_skills = "UNWIND range(1," + str(with_skills) + ") AS vertices CREATE(e:Employee{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices), skills:'Department_" + str(dept) + "_Pro'})"
        create_departments_no_skills = "UNWIND range(" + str(with_skills + 1) + ", " + str(people_per_department[dept]) + ") AS vertices CREATE(e:Employee{name:'New_Department_" + str(dept) + "_Employee_'+ toString(vertices),manager:'Boss_" + str(dept) +  "',department:'Department_" + str(dept) + "'})"
        
        if with_skills > 0:
            query_department = "CREATE (d:Department {dept:'Department_" + str(dept) + "', manager: 'Boss_" + str(dept) + "'})"
            new_db.execute_query(query_department)
        
        new_db.execute_query(create_departments_skills)
        new_db.execute_query(create_departments_no_skills)
        

    # create relationships
    create_relationships_one = "MATCH (e:Employee), (c:Company) CREATE (e)-[:WORKS_FOR]->(c)"
    create_relationships_two = "MATCH (e:Employee),(d:Department) WHERE EXISTS(e.skills) AND e.name CONTAINS d.dept CREATE (e)-[:IN_DEPARTMENT]->(d)"
    # change EXISTS according to property set P
    
    new_db.execute_query(create_relationships_one)
    new_db.execute_query(create_relationships_two)




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

# create random department sizes for fixed amount of employees
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
    local_bolt = "<enter_local_bolt>"
    local_http = "<enter_local_http>"
    local_pw = "<enter_password_for_graph_db>"
    local_user = "<enter_user_for_graph_db__neo4j_by_default>"

    # Initialise DB
    new_db = gdbms_test(local_bolt, local_user, local_pw)
        
    # perform experiment multiple times
    runs = 10
    for i in range(1, runs):
        # perform experiment for different scaling factors
        # commented out parts for different experiment scenarios
        
        factors = [1,2,5,10,25,50,100,250,500,1000]
        
        #departments = [10, 15, 10, 20, 40, 25, 30]
        
        departments = [1,4,2]
        #departments = split_up(150, 5)
        distribution = [1]*len(departments) # determines which percentage of employees in each department possess additional property skills
        #labels_distribution = [0.25, 0.8] # what percentage of employees are employee of the month and what percentage of person are employees / !!!!currently assume labels_distribution[0] , min(distribution)
        labels_distribution = [0,1]
        properties = [] # additional synthetic properites that can be added to each employee

        dbhits = []
        redundancy = []

        # different queries for experiments
        # queries commented out depending on experiment scenario
        # depending on whether query for normalized graph or baseline graph set boolean variable is_normalised to True or False and ajdust line 168 according to property set P

        
        # queries to meassure performance of aggreation
        #aggregate_norm_query = "PROFILE MATCH (d:Department) WITH SIZE([(d)--(e:Employee) | e]) AS dept RETURN min(dept), max(dept), avg(dept)"
        #aggregate_denorm_query = "PROFILE MATCH (e:Employee) WITH e.department AS dept, COUNT(*) AS size RETURN min(size), max(size), avg(size)"
        

        # queries to meassure performance of updates
        #update_denorm = "PROFILE MATCH (e:Employee) WHERE e.manager = 'Boss_" + str(i-1) +"' SET e.manager = 'New_boss'"
        #update_denorm = "PROFILE MATCH (e:Employee) WHERE e.manager = 'Boss_0' SET e.manager = 'New_boss'"
        #update_norm = "PROFILE MATCH (d:Department) WHERE d.manager = 'Boss_0' SET d.manager = 'New_boss'"
        

        
        # queries to compare verification of gFDs in baseline graph compared to verification of gUCs in normalized graph for P with 4 properties
        #verify_gfd_denorm_query = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) AND EXISTS(e.skills) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_guc_norm_query = "PROFILE MATCH(d:Department) WHERE EXISTS(d.manager) AND EXISTS(d.dept) RETURN d.dept, COUNT(d)"

        
        # queries to meassure performance depending on size of P
        #verify_gfd_denorm_query_1 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_gfd_denorm_query_2 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_gfd_denorm_query_3 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_gfd_denorm_query_4 = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) AND EXISTS(e.skills) RETURN e.department, COUNT (DISTINCT e.manager)"
        #verify_gfd_denorm_query_list = [verify_gfd_denorm_query_1, verify_gfd_denorm_query_2, verify_gfd_denorm_query_3, verify_gfd_denorm_query_4]

        # alternatively
        # test impact of different embeddings on queries for denormalized instance
        #embedding = ['name', 'department', 'manager', 'skills']
        #additional_embedding = ['property_' + str(k) for k in range(len(properties))]
        #embedding += additional_embedding
        #embedding = embedding[:1 + i]
        #query_denorm = "PROFILE MATCH (e:Employee) WHERE " + add_embedding_check('e', embedding) + " AND e.department = 'Department_1' AND e.name = 'New_Department_1_Employee_2' RETURN e"

        # queries to meassure impact of labels EoM subseteq Empoloyee subseteq Person (Person includes nodes that aren't employees with status 'retired') / set different_labels to True
        #impact_lables_eom_verify_gfd_denorm_query = "PROFILE MATCH(e:EoM) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        #impact_lables_employee_verify_gfd_denorm_query = "PROFILE MATCH(e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        #impact_lables_person_verify_gfd_denorm_query = "PROFILE MATCH(e:Person) WHERE EXISTS(e.manager) AND EXISTS(e.department) AND EXISTS(e.name) RETURN e.department, COUNT (DISTINCT e.manager)"
        #query_list = [impact_lables_eom_verify_gfd_denorm_query, impact_lables_employee_verify_gfd_denorm_query, impact_lables_person_verify_gfd_denorm_query]


        #queries to meassure impact of ratio of P-complete nodes
        # Adjust distribution list to respective values 0.2, 0.4, etc




        # counting redundancy
        count_redundancy = "MATCH (e:Employee) WHERE EXISTS (e.name) AND EXISTS (e.department) AND EXISTS (e.manager) AND EXISTS (e.skills) WITH e.name AS redundancy RETURN COUNT(redundancy) AS redundant"

        
        
        # queries to compare verification of gFDs in baseline graph compared to verification of gUCs in normalized graph for trivial embedding P
        #
        # baseline graph
        query = "PROFILE MATCH (e:Employee) WHERE EXISTS(e.manager) AND EXISTS(e.department) RETURN e.department, COUNT(DISTINCT e.manager)"
        #
        # normalized graph / set is_normalized to true
        #query = "PROFILE MATCH(d:Department) WHERE EXISTS(d.manager) AND EXISTS(d.dept) RETURN d.dept, COUNT(d)"


        
        is_normalized = False
        different_labels = False


        for factor in factors:
            # create db instance

            #create_db_instance(new_db, departments, distribution, is_normalised = is_normalized)
            create_db_instance(new_db, [factor * x for x in departments], distribution, is_normalised = is_normalized, different_labels = different_labels, labels_distribution = labels_distribution, properties = properties)

            # perform query and meassure db hits
            current_dbhits = show_dbhits(new_db, query)
            dbhits.append(current_dbhits)

            # meassure P-redundancy (only in denormalised instance)
            if not is_normalized:
                current_redundancy = new_db.execute_query_with_output_result(count_redundancy)[0]['redundant']
                redundancy.append(current_redundancy)

            
        # shows if experiment is still running
        print()
        print(f"{runs-i-1} more experiments to go...")
        print()
        

        # Experiment results

        filename = "Experiment" + str(i) + ".xlsx"
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



    # closing db
    new_db.close()


main()




