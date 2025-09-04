import json
import logging
import sys


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)


def log_json(**kwargs):
    logging.getLogger().info(json.dumps(kwargs))
