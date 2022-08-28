import logging

_logger = logging.getLogger(__name__)


def get_name():
    print("Hello CI")
    _logger.info("Hello CI")
