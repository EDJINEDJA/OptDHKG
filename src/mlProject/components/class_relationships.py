import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import ClassRelationshipsConfig

from neo4j import GraphDatabase
import glob
import math
import numpy as np

class ClassRelationships:
    def __init__(self, config: ClassRelationshipsConfig):
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

    def classRelationships(self):
        # Defining path towards the log
        subjectids_path = self.config.subjectids_path

        # Defining the taxonomy used for representing entity
        entity_taxonomy = self.config.entity_taxonomy

        #Defining the sub taxonomy used for representing event
        event_taxonomy = self.config.event_taxonomy

        #Defining the key
        key = self.config.key

        #Defining the type of relation
        type_relation =  self.config.type_relation

        pation_logs = pd.read_csv(subjectids_path)

        subjectids = list(pation_logs[self.config.identifier])

        subjectids_unique = list(set(subjectids))

        check_attribut = self.config.check_attribut

        for patient_id  in subjectids_unique:
            query = (
                "UNWIND $patient_id AS id "
                "MATCH (n:" + entity_taxonomy + ") WHERE n." + key + "=id "
                "MATCH (e:" + event_taxonomy + ") WHERE e." + key + "=id " 
                "CREATE (p:Class {dead: CASE WHEN exists(n." + check_attribut + ") THEN 'yes' ELSE 'no' END})"
                "CREATE (p)-[:" + type_relation + "]->(e);"
            )
            try:
                self.query(query, parameters={"patient_id": patient_id})
            except Exception as e:
                logger.info("Issue when creating relations between class and event nodes")

        logger.info("Relationchips are created successfully")
        self.close()