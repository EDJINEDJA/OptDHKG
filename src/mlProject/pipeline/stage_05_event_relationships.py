from mlProject import logger
from mlProject.components.event_relationships import EventRelationships
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Event relationships stage"


class EventRelationshipsPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        event_relationships_config = config.event_relationships_config()
        event_relationships_config = EventRelationships(config=event_relationships_config)
        event_relationships_config.eventRelationships()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EventRelationshipsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
