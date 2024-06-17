from mlProject import logger
from mlProject.components.event_optimization import EventOptimization
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "Events Optimization stage"


class EventsOptimizationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        event_optimization_config = config.event_optimization_config()
        event_optimization_config  = EventOptimization(config=event_optimization_config)
        event_optimization_config.eventOptimization()

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EventsOptimizationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
