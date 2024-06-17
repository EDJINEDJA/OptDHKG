import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import EventsOptimizationConfig

from neo4j import GraphDatabase
import glob
import math
import numpy as np

class EventOptimization:
    def __init__(self, config: EventsOptimizationConfig):
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

    def eventOptimization(self):

        # Defining path towards the log
        subjectids_path = self.config.subjectids_path

        # Defining taxonomy
        taxonomy = self.config.event_taxonomy

        # Defining the key which corresponds to the unique identification of a patient
        key = self.config.key

        # Read subject IDs from CSV
        patient_logs = pd.read_csv(subjectids_path)
        subjectids = list(patient_logs[self.config.identifier])
        subjectids_unique = list(set(subjectids))

        for patient_id in subjectids_unique:
            # query = (
            #     "MATCH (n:" + taxonomy + ") "
            #     "WHERE n." + key + "=$id "
            #     "WITH COLLECT(n) AS nodeList, [prop IN keys(head(nodeList)) | prop] AS properties "
            #     "UNWIND properties AS propertyName "
            #     "WITH nodeList, propertyName, COUNT(propertyName) AS propertyCount, SIZE(nodeList) AS totalNodes "
            #     "WITH nodeList, -SUM((propertyCount / TOFLOAT(totalNodes)) * LOG(propertyCount / TOFLOAT(totalNodes)) / LOG(2)) AS initialEntropy "
            #     "FOREACH (ignored IN CASE WHEN SIZE(nodeList) > 1 THEN [1] ELSE [] END | "
            #     "   WITH nodeList, initialEntropy, "
            #     "        REDUCE(s = 0.0, prop IN keys(head(nodeList)) | s + (COUNT(prop) / TOFLOAT(SIZE(nodeList))) * LOG(COUNT(prop) / TOFLOAT(SIZE(nodeList))) / LOG(2)) AS currentEntropy "
            #     "   SET nodeList = TAIL(nodeList) "
            #     "   WITH nodeList, initialEntropy, currentEntropy, HEAD(nodeList) AS removedNode "
            #     "   UNWIND keys(removedNode) AS removedProperty "
            #     "   WITH nodeList, initialEntropy, currentEntropy, removedNode, removedProperty, COUNT(removedProperty) AS removedPropertyCount, SIZE(nodeList) AS remainingNodes "
            #     "   WITH nodeList, initialEntropy, currentEntropy, removedNode, removedProperty, removedPropertyCount, remainingNodes, "
            #     "       -SUM((removedPropertyCount / TOFLOAT(remainingNodes)) * LOG(removedPropertyCount / TOFLOAT(remainingNodes)) / LOG(2)) AS removedNodeEntropy "
            #     "   FOREACH (ignored IN CASE WHEN currentEntropy >= initialEntropy THEN [1] ELSE [] END | DETACH DELETE removedNode) "
            #     "   FOREACH (ignored IN CASE WHEN currentEntropy < initialEntropy THEN [1] ELSE [] END | SET nodeList = [removedNode] + nodeList) "
            #     "   SET initialEntropy = currentEntropy - removedNodeEntropy "
            #     ")"
            # )
            # query = (
            #     "MATCH (n:Event) WHERE n.subject_id=$id "
            #     "WITH COLLECT(n) AS nodeList "
            #     "UNWIND nodeList AS n "
            #     "WITH nodeList, "
            #     "COUNT(n) AS nodeCount "
            #     "WITH nodeList, "
            #     "-SUM((nodeCount / TOFLOAT(SIZE(nodeList))) * "
            #     "LOG(nodeCount / TOFLOAT(SIZE(nodeList))) / LOG(2)) AS initialEntropy, "
            #     "HEAD(nodeList) AS collectedNode "
            #     "FOREACH (ignored IN CASE WHEN SIZE(nodeList) > 1 THEN [1] ELSE [] END | "
            #     "SET nodeList = TAIL(nodeList)) "
            #     "WITH collectedNode, initialEntropy "
            #     "UNWIND [collectedNode] AS node "
            #     "WITH collectedNode, initialEntropy, "
            #     "REDUCE(s = 0.0, prop IN keys(node) | "
            #     "s + (COUNT(prop) / TOFLOAT(SIZE([collectedNode]))) * "
            #     "LOG(COUNT(prop) / TOFLOAT(SIZE([collectedNode]))) / LOG(2)) AS currentEntropy, "
            #     "collectedNode AS removedNode "
            #     "UNWIND keys(removedNode) AS removedProperty "
            #     "WITH collectedNode, initialEntropy, currentEntropy, removedNode, "
            #     "removedProperty, COUNT(removedProperty) AS removedPropertyCount, "
            #     "SIZE([collectedNode]) AS remainingNodes, "
            #     "-SUM((removedPropertyCount / TOFLOAT(SIZE([collectedNode]))) * "
            #     "LOG(removedPropertyCount / TOFLOAT(SIZE([collectedNode]))) / LOG(2)) "
            #     "AS removedNodeEntropy "
            #     "DETACH DELETE removedNode "
            #     "FOREACH (ignored IN CASE WHEN currentEntropy < initialEntropy THEN [1] ELSE [] END | "
            #     "SET nodeList = [removedNode] + nodeList) "
            #     "SET initialEntropy = currentEntropy - removedNodeEntropy "
            # )
            query = (
                "MATCH (n:Event) WHERE n.subject_id=$id "
                "WITH COLLECT(n) AS nodeList "
                "UNWIND nodeList AS event "
                "WITH nodeList, "
                "[prop IN keys(event) | prop] AS properties, "
                "COUNT(event) AS eventCount "
                "WITH nodeList, properties, eventCount, "
                "-SUM((eventCount / TOFLOAT(SIZE(nodeList))) * "
                "LOG(eventCount / TOFLOAT(SIZE(nodeList))) / LOG(2)) AS initialEntropy, "
                "CASE WHEN SIZE(nodeList) > 1 THEN TAIL(nodeList) ELSE nodeList END AS remainingNodes, "
                "HEAD(nodeList) AS removedNode "
                "UNWIND keys(removedNode) AS removedProperty "
                "WITH nodeList, properties, initialEntropy, removedNode, removedProperty, "
                "SIZE(remainingNodes) AS remainingCount, "
                "COUNT(removedProperty) AS removedPropertyCount "
                "DETACH DELETE removedNode "
                "WITH nodeList, initialEntropy, removedPropertyCount, remainingCount "
                "RETURN nodeList, initialEntropy, "
                "-(removedPropertyCount / TOFLOAT(remainingCount)) * "
                "LOG(removedPropertyCount / TOFLOAT(remainingCount)) / LOG(2) AS removedNodeEntropy "
            )

            try:
                self.query(query, parameters={"id": patient_id})
            except Exception as e:
                logger.info("Issue when optimizing nodes")

        logger.info("Optimization is done")
        self.close()
