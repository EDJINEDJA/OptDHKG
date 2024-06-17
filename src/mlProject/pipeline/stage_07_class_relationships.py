from mlProject import logger
from mlProject.components.class_relationships import ClassRelationships
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Class relationships stage"


class ClassRelationshipsPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        class_relationships_config = config.class_relationships_config()
        class_relationships_config  = ClassRelationships(config= class_relationships_config )
        class_relationships_config.classRelationships()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ClassRelationshipsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
