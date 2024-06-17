from mlProject import logger
from mlProject.components.resource_relationships import ResourceRelationships
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Resource relationships stage"


class ResourceRelationshipsPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        resource_relationships_config = config.resource_relationships_config()
        resource_relationships_config  = ResourceRelationships(config=resource_relationships_config)
        resource_relationships_config.resourceRelationships()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ResourceRelationshipsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
