import os

import numpy as np
import pandas as pd

from mlProject import logger
from mlProject.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from mlProject.pipeline.stage_02_event_logs_ingestion import EventLogsPipeline
from mlProject.pipeline.stage_03_patients_representation import PatientsRepresentationPipeline
from mlProject.pipeline.stage_04_events_representation import EventsRepresentationPipeline
from mlProject.pipeline.stage_05_event_relationships import EventRelationshipsPipeline
from mlProject.pipeline.stage_06_entity_relationships import EntityRelationshipsPipeline
from mlProject.pipeline.stage_07_class_relationships import ClassRelationshipsPipeline
from mlProject.pipeline.stage_08_resource_relationships import ResourceRelationshipsPipeline
from mlProject.pipeline.stage_09_events_optimization import EventsOptimizationPipeline

if __name__ == "__main__":

    STAGE_NAME = "Data Ingestion stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        data_ingestion = DataIngestionPipeline()
        data_ingestion.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    STAGE_NAME = "Event logs Ingestion stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        event_logs_ingestion = EventLogsPipeline()
        event_logs_ingestion.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    STAGE_NAME = "Patient Nodes representation"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = PatientsRepresentationPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Events represention with relationship stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = EventsRepresentationPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    STAGE_NAME = "Event relationships represention stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = EventRelationshipsPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Entity relationships stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = EntityRelationshipsPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Class relationships stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = ClassRelationshipsPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Resource relationships stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = ResourceRelationshipsPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Events Optimization stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        Patients_node = EventsOptimizationPipeline()
        Patients_node.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e