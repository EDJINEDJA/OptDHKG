import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import PatientsRepresentationConfig
from neo4j import GraphDatabase

class PatientsRepresentation:
    def __init__(self, config: PatientsRepresentationConfig):
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

    def patients2entitynodes(self):

        PATIENTS = pd.read_csv(self.config.data_path)
        all_attributes = self.config.all_attributs
        column_id = self.config.column_id
        taxonomy = self.config.taxonomy
        sub_taxonomy = self.config.sub_taxonomy
        items = all_attributes.items()
        reader = PATIENTS.to_dict(orient='records')
        logger.info("Creating dictionaries of patient information from patient logs")

        for raw in reader:
            node_facts = { column:  raw[f"{column}"] for attribute, column in items}

            #Filling the display name of the node for the visualization
            node_facts["displayName"] = "Patient_" + f"{node_facts[column_id]}"
    
            # Créer un nouveau dictionnaire avec les clés sans simples cotes
            id_value = str(raw[column_id])
            params = {
                "labels":{
                "taxonomy": taxonomy,
                "sub_taxonomy": sub_taxonomy,
                "id": id_value},
                "props": node_facts
            }
            
            query = (
                "UNWIND $props AS properties "
                "CREATE (" + "n" + ":" + params["labels"]["taxonomy"] + ") "
                "SET n = properties"
            )

            try:
                self.query(query, parameters=params)
            except Exception as e:
                logger.info("Issue when creating the entity node")

        logger.info("Create node entity with informations")
        self.close()