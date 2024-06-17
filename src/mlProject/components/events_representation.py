import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import EventsRepresentationConfig

from neo4j import GraphDatabase
import glob
import math
import numpy as np

class EventsRepresentation:
    def __init__(self, config: EventsRepresentationConfig):
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

    def eventsRepresentation(self):

        # Définir le chemin des fichiers d'événements
        events_log_path = self.config.data_path
        time_column = self.config.time
        taxonomy = self.config.taxonomy

        # Récupérer tous les chemins des fichiers CSV dans le répertoire des événements
        events_files = glob.glob(events_log_path + "*.csv")

        event = { column:  float('nan') for attribute, column in self.config.event_attributs.items()}

        additional_info_patients = { column:  float('nan') for attribute, column in self.config.patient_attributs.items()}

        for file_path in events_files:
            # Lire le fichier CSV et le trier par la colonne de temps
            events_log = pd.read_csv(file_path).sort_values(by=time_column)

            # Convertir le DataFrame en dictionnaire de dictionnaires
            events_data = events_log.to_dict(orient='records')

            # Créer les événements et les relations de suivi direct
            for i in range(len(events_data)):

                # event = events_data[i]
                event_i = events_data[i]
                for column , value in event_i.items():
                    if column in event:
                        event[column] = value

                #Filling the display name of the node for the visualization
                event["displayName"] = "Event_" + f"{i}"
               
                # Supprimer toutes les clés où la valeur est nan
                event_props = {k: v for k, v in event.items() if not isinstance(v, float) or not math.isnan(v)}
            
                #Créer le nœud pour l'événement
                query = (
                    "UNWIND $props AS properties "
                    "CREATE (" + "e" + ":" + taxonomy + ") "
                    "SET e = properties"
                )
                try:
                    self.query(query, parameters={"props": event_props})
                except Exception as e:
                    logger.info("Issue when creating the event node")
            
            #All event containing together these same attribut
            #Extracting additional information from events log
            
            for column , value in events_data[0].items():
                if column in additional_info_patients:
                    additional_info_patients[column] = value
            
            # Supprimer toutes les clés où la valeur est nan
            additional_info = {k: v for k, v in additional_info_patients.items() if not isinstance(v, float) or not math.isnan(v)}
          
            #Extracting the identifaction of the patient
            subject_id = events_data[0]["subject_id"]

            # Construire la liste de paires clé-valeur à partir du dictionnaire des nouvelles propriétés
            properties_list = [{key: value} for key, value in additional_info.items()]

            # Construire la requête Cypher avec UNWIND pour mettre à jour les propriétés du nœud existant
            query = (
                "UNWIND $additional_info_patients AS property "
                "MATCH (n:Patient) WHERE n.subject_id = $subject_id "
                "SET n += property"
            )
            try:
                self.query(query, parameters={"additional_info_patients": properties_list,"subject_id":subject_id})
            except Exception as e:
                logger.info("Issue when creating the event node")

        logger.info("Events are created successfully and additional information are added")
        self.close()