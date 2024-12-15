import logging
import logging.config

from logger_config import config as logger_config


logging.config.dictConfig(logger_config)


def get_logger(name: str):
    return logging.getLogger(name)
