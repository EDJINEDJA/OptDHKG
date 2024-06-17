from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class PatientsRepresentationConfig:
    root_dir: Path
    data_path: Path
    column_id: str
    taxonomy: str
    sub_taxonomy: str
    all_attributs: dict

@dataclass(frozen=True)
class EventLogsConfig:
    root_dir: Path
    subjectids: Path
    identifier: str
    logs: dict
    patient_attributs: dict


@dataclass(frozen=True)
class EventsRepresentationConfig:
    data_path: Path
    taxonomy: str
    sub_taxonomy: str
    column_id: str
    space: str
    time: str
    relation: str
    event_attributs: dict
    patient_attributs: dict

@dataclass(frozen=True)
class EventRelationshipsConfig:
    subjectids_path: Path
    identifier: str
    taxonomy: str
    sub_taxonomy: str
    key: str
    time: str
    type_relation: str


@dataclass(frozen=True)
class EntityRelationshipsConfig:
    subjectids_path: Path
    identifier: str
    type_relation: str
    entity_taxonomy: str
    event_taxonomy: str
    key: str


@dataclass(frozen=True)
class ClassRelationshipsConfig:
    subjectids_path: Path
    identifier: str
    type_relation: str
    entity_taxonomy: str
    event_taxonomy: str
    key: str
    check_attribut: str

@dataclass(frozen=True)
class ResourceRelationshipsConfig:
    resources_path: Path
    subjectids_path: Path
    identifier: str
    type_relation: str
    event_taxonomy: str
    key: str


@dataclass(frozen=True)
class EventsOptimizationConfig:
    subjectids_path: Path
    identifier: str
    event_taxonomy: str
    key: str
