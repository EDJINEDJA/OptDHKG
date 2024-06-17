from mlProject.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from mlProject.entity.config_entity import (
    DataIngestionConfig,
    PatientsRepresentationConfig,
    EventLogsConfig,
    EventsRepresentationConfig,
    EventRelationshipsConfig,
    EntityRelationshipsConfig,
    ClassRelationshipsConfig,
    ResourceRelationshipsConfig,
    EventsOptimizationConfig
)
from mlProject.utils.common import create_directories, read_yaml


class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH,
    ):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
        )

        return data_ingestion_config
    
    def get_patients_representation_config(self) -> PatientsRepresentationConfig:
        config = self.config.patients_representation

        create_directories([config.root_dir])

        patients_representation_config = PatientsRepresentationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            column_id = config.column_id,
            taxonomy= config.taxonomy,
            sub_taxonomy= config.sub_taxonomy,
            all_attributs= config.attributs,
        )

        return patients_representation_config
    
     
    def get_event_logs_config(self) -> EventLogsConfig:
        config = self.config.event_logs

        create_directories([config.root_dir])

        event_logs_config = EventLogsConfig(
            root_dir=config.root_dir,
            subjectids =config.subjectids,
            identifier = config.identifier,
            logs = config.logs,
            patient_attributs = config.patient_attributs,
        )

        return  event_logs_config
    

    def representation_events_config(self) -> EventsRepresentationConfig:
        config = self.config.events_representation

        event_representation_config = EventsRepresentationConfig(
            data_path=config.data_path,
            taxonomy=config.taxonomy,
            sub_taxonomy=config.sub_taxonomy,
            column_id =config.column_id,
            space = config.space,
            time=config.time,
            relation=config.relation,
            event_attributs = config.event_attributs,
            patient_attributs= config.patient_attributs,
        )

        return event_representation_config
    
    def event_relationships_config(self) -> EventRelationshipsConfig:
        config = self.config.event_relationships

        event_relationships_config =  EventRelationshipsConfig(
            subjectids_path=config.subjectids_path,
            identifier=config.identifier,
            taxonomy= config.taxonomy,
            sub_taxonomy= config.sub_taxonomy,
            key= config.key,
            time=config.time,
            type_relation= config.type_relation,
        )

        return event_relationships_config
    
    def entity_relationships_config(self) -> EntityRelationshipsConfig:
        config = self.config.entity_relationships

        entity_relationships_config =  EntityRelationshipsConfig(
            subjectids_path=config.subjectids_path,
            identifier= config.identifier,
            type_relation=config.type_relation,
            entity_taxonomy=config.entity_taxonomy,
            event_taxonomy=config.event_taxonomy,
            key=config.key,
        )

        return entity_relationships_config
    

    def  class_relationships_config(self) -> ClassRelationshipsConfig:
        config = self.config.class_relationships

        class_relationships_config =  ClassRelationshipsConfig(
            subjectids_path=config.subjectids_path,
            identifier= config.identifier,
            type_relation=config.type_relation,
            entity_taxonomy=config.entity_taxonomy,
            event_taxonomy=config.event_taxonomy,
            key=config.key,
            check_attribut= config.check_attribut,
        )

        return class_relationships_config
    

    def  resource_relationships_config(self) -> ResourceRelationshipsConfig:
        config = self.config.resource_relationships

        resource_relationships_config =  ResourceRelationshipsConfig(
            resources_path=config.resources_path,
            subjectids_path=config.subjectids_path,
            identifier= config.identifier,
            type_relation=config.type_relation,
            event_taxonomy=config.event_taxonomy,
            key=config.key,
        )

        return resource_relationships_config
    
    def  event_optimization_config(self) -> EventsOptimizationConfig:
        config = self.config.resource_relationships

        event_optimization_config =  EventsOptimizationConfig(
            subjectids_path=config.subjectids_path,
            identifier= config.identifier,
            event_taxonomy=config.event_taxonomy,
            key=config.key,
        )

        return event_optimization_config
    