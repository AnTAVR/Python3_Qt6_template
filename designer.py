#!/usr/bin/env python3
import logging
import os

import src.libs.logs.args
from src.libs import SRC_DIR, CURRENT_DIR
from src.libs.all import run_command
from src.libs.args import arg_parser

src.libs.logs.args.run(logging.DEBUG)

logger = logging.getLogger(__name__)

DIR_DESIGNER = CURRENT_DIR.joinpath('project')
DIR_QT = SRC_DIR.joinpath('qt')

ENV = os.environ.copy()
ENV['PYQTDESIGNERPATH'] = os.pathsep.join(x for x in (
    str(DIR_DESIGNER.joinpath('window')),
    str(DIR_DESIGNER.joinpath('widget')),
    # str(DIR_DESIGNER),
    ENV.get('PYQTDESIGNERPATH', None)
) if x)


def main() -> int:
    # --------

    # --------
    arguments = arg_parser.parse_args()
    # --------

    # --------
    """
    Запускаю Designer
    """
    # exit_code = os.EX_OK
    command = ['designer6', ]
    exit_code = run_command(command, str(DIR_QT), ENV).returncode
    if exit_code:
        return exit_code

    return exit_code


if __name__ == '__main__':
    exit(main())
