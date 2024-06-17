from mlProject import logger
from mlProject.components.event_logs_ingestion import EventLogsTransformation
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Event logs stage"


class EventLogsPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        event_logs_config = config.get_event_logs_config()
        event_logs_transformation = EventLogsTransformation(config=event_logs_config)
        event_logs_transformation.event_logs_ingestion()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EventLogsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
