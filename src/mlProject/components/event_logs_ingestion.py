import os
import pandas as pd
import numpy as np
from mlProject import logger
from mlProject.entity.config_entity import EventLogsConfig

class EventLogsTransformation:
    def __init__(self, config: EventLogsConfig):
        self.config = config

    def event_logs_ingestion(self):

        pation_logs = pd.read_csv(self.config.subjectids)

        subjectids = list(pation_logs[self.config.identifier])

        subjectids_unique = list(set(subjectids))

        logs = { attribute :  column for attribute, column in self.config.logs.items()}

        logger.info("Creating unique subject identifier,  facts and logs")

        for subject_id  in subjectids_unique:
            events = {}
            facts = { column:  float('nan') for attribute, column in self.config.patient_attributs.items()}
    
            for _ , path in logs.items():
                filename = path.split("/")[-1].replace(".csv", "")
                logger.info(f"Processing filname {filename}")
                data = pd.read_csv(path)
                list_dict = data.to_dict(orient = "records")
                compt = 0
                for dict  in list_dict:
                    if dict[self.config.identifier] == subject_id:
                        compt += 1
                        for attribute , value in dict.items():
                            facts[attribute] = value
                        facts = {cle: valeur for cle, valeur in facts.items()}
                        events[compt] = facts
                    else:
                        pass

            envents_df = pd.DataFrame.from_dict(data=events, orient='index')
            envents_df.to_csv(self.config.root_dir + "event_log_" + f"{subject_id}" + ".csv",index=False,encoding="utf-8")

            logger.info(f"Creating log of patient {subject_id} ")
        logger.info(f"Creating event logs of all patients")