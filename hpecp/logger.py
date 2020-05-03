import logging
import os

class Logger:

    def get_logger(self, clazz):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=format)
        logger = logging.getLogger(clazz)
        logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
        return logger
