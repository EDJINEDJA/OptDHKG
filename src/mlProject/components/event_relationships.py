import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import EventRelationshipsConfig

from neo4j import GraphDatabase
import glob
import math
import numpy as np

class EventRelationships:
    def __init__(self, config: EventRelationshipsConfig):
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

    def eventRelationships(self):

        # Defining path towards the log
        subjectids_path = self.config.subjectids_path

        # Defining taxonomy
        taxonomy = self.config.taxonomy

        #Defining key vwich corresponding to the unique identifaction of patient
        key = self.config.key

        #Defining time
        time = self.config.time

        #Defining type of relationship
        type_relation =  self.config.type_relation

        pation_logs = pd.read_csv(subjectids_path)

        subjectids = list(pation_logs[self.config.identifier])

        subjectids_unique = list(set(subjectids))

        for patient_id  in subjectids_unique:

            query = ("UNWIND $patient_id AS id MATCH ("+ "n" + ":" + taxonomy + " WHERE n." + key + "=id)" + " WITH n ORDER BY n." + time + " WITH collect(n) AS nodes FOREACH(i IN RANGE(0, size(nodes)-2) | FOREACH(node1 IN [nodes[i]] | FOREACH(node2 IN [nodes[i+1]] | CREATE (node1)-[:" + type_relation + "]->(node2))))")

            try:
                self.query(query, parameters={"patient_id": patient_id})
            except Exception as e:
                logger.info("Issue when creating relations between nodes")
        logger.info("Relationchips are created successfully")
        self.close()