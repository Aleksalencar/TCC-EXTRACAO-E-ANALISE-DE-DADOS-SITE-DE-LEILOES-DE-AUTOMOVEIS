import logging
from datetime import date



class LoggingConfig:
    # Config logging
    def __init__(self):
        today = date.today()
        log_date = today.strftime("%Y%m%d")

        # posteriorly add config.json with project_base_path
        log_file = "Log_" + log_date + ".txt"

        # Change this var to log on file
        is_file_logging = False
        log_format = '%(asctime)s | %(levelname)s | %(message)s'

        if is_file_logging:
            logging.basicConfig(level=logging.DEBUG, filename=log_file, format=log_format)
        else:
            logging.basicConfig(level=logging.INFO, format=log_format)



    @staticmethod
    def get_logging():
        return logging