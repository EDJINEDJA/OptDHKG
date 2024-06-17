from mlProject import logger
from mlProject.components.entity_relationships import EntityRelationships
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Entity relationships stage"


class EntityRelationshipsPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        entity_relationships_config = config.entity_relationships_config()
        entity_relationships_config  = EntityRelationships(config= entity_relationships_config )
        entity_relationships_config.entityRelationships()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EntityRelationshipsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
