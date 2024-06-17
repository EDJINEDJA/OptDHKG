import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import ResourceRelationshipsConfig

from neo4j import GraphDatabase
import glob
import math
import numpy as np

class ResourceRelationships:
    def __init__(self, config: ResourceRelationshipsConfig):
        self.config = config
        self.__uri = os.getenv('NEO4J_URI')
        self.__user_name = os.getenv('USER_NAME')
        self.__password = os.getenv('PASSWORD')
        self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user_name, self.__password))
    
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    
    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def resourceRelationships(self):

        # Defining path towards the patients log
        subjectids_path = self.config.subjectids_path

        # Defining path towards the services log
        services_path = self.config.resources_path

        # Defining taxonomy
        taxonomy = self.config.event_taxonomy

        #Defining key vwich corresponding to the unique identifaction of patient
        key = self.config.key

        #Defining type of relationship
        type_relation =  self.config.type_relation

        #Reading the patients event logs to get patients id 
        pation_logs = pd.read_csv(subjectids_path)

        subjectids = list(pation_logs[self.config.identifier])

        subjectids_unique = list(set(subjectids))

        #Reading the services event logs to get prev_service,curr_service
        services_logs = pd.read_csv(services_path)

        for patient_id  in subjectids_unique:

            selected_rows = services_logs.loc[services_logs[key]==patient_id,"prev_service":"curr_service"]
            
            if selected_rows['prev_service'].to_string(index=False, header=False) != 'NaN':

                property = selected_rows['prev_service'].to_string(index=False, header=False) + ' and ' + selected_rows['curr_service'].to_string(index=False, header=False)
            else:
                property = selected_rows['curr_service'].to_string(index=False, header=False)
            
            params = {"resource":  property, "displayName": property}
            id = f"{patient_id}"

            query = (
                "UNWIND $proprety AS propreties "
                "MERGE (h:Resource) "
                "SET h = propreties "
                "WITH h "
                "MATCH (e:" + taxonomy + ") WHERE e." + key + "=" + id + " "
                "CREATE (h)-[:" + type_relation + "]->(e);"
            )
            try:
                self.query(query, parameters={"proprety": params})
            except Exception as e:
                logger.info("Issue when creating relations between ressource and event nodes")

        logger.info("Relationships are created successfully")
        self.close()