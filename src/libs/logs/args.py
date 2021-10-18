__all__ = ['run']

import logging
from argparse import ArgumentParser
from gettext import gettext as _
from typing import Union

from .conf import CFG
from ..args import arg_parser


def init() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    # noinspection PyProtectedMember,PyUnresolvedReferences
    parser.add_argument('--loglevel', choices=tuple(logging._nameToLevel),
                        help=_('Logging level.'),
                        dest='loglevel',
                        type=str,
                        default=CFG.loglevel)

    arguments, tmp = parser.parse_known_args()

    CFG.loglevel = arguments.loglevel

    return parser


def run(loglevel: Union[int, str] = None, log_file: str = None):
    exception = None
    try:
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from colorlog import basicConfig
    except ImportError as e:
        exception = e
        # noinspection PyPep8Naming
        basicConfig = logging.basicConfig

    if loglevel is None:
        loglevel = CFG.loglevel

    basicConfig(level=loglevel, filename=log_file, filemode='w',
                format=CFG.format)

    if exception is not None:
        logger = logging.getLogger(__name__)
        logger.warning(exception)


arg_parser.add_parent(init())
