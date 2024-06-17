from pathlib import Path

from mlProject import logger
from mlProject.components.patients_representation import PatientsRepresentation
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME = "PATIENTS Transformation stage"


class PatientsRepresentationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
          
            config = ConfigurationManager()
            data_transformation_config = config.get_patients_representation_config()
            data_transformation = PatientsRepresentation(
                config=data_transformation_config
            )
            data_transformation.patients2entitynodes()

          
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PatientsRepresentationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
