#!/usr/bin/env python3
import logging
import os

import libs.logs.args
from libs import DOMAIN
from libs.args import arg_parser

libs.logs.args.run()

logger = logging.getLogger(DOMAIN)


def main() -> int:
    # --------

    # --------
    arguments = arg_parser.parse_args()
    # --------

    # --------
    exit_code = os.EX_OK
    logger.info('exit_code={}'.format(exit_code))
    return exit_code


if __name__ == '__main__':
    exit(main())
