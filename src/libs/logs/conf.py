__all__ = ['CFG']

import logging


class CFG:
    loglevel = logging.getLevelName(logging.ERROR)
    format = '%(levelname)s:%(threadName)s:%(name)s:%(lineno)s:%(message)s'
