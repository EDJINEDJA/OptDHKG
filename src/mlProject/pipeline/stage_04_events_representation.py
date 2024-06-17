from mlProject import logger
from mlProject.components.events_representation import EventsRepresentation
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Event representation stage"


class EventsRepresentationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        events_representation_config = config.representation_events_config()
        events_representation_config = EventsRepresentation(config=events_representation_config)
        events_representation_config.eventsRepresentation()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EventsRepresentationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
