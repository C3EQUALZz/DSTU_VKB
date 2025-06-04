"""
Here you must write all filters for logging.
"""

import logging


class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.INFO
