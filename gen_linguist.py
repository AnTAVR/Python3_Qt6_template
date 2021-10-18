#! /usr/bin/env python3
import logging
import os
from typing import Sequence

import src.libs.logs.args
from src.libs import DOMAIN, TEXTDOMAINDIR, SRC_DIR, DIR_PO
from src.libs.all import run_command
from src.libs.args import arg_parser

src.libs.logs.args.run(logging.DEBUG)

logger = logging.getLogger(__name__)

CODE = 'UTF-8'
LANGS = ('ru_RU',)


def gen_ts(domain: str, list_files: Sequence[str]):
    exit_code = os.EX_OK
    for lang in LANGS:
        file_ts = DIR_PO.joinpath(domain).with_suffix('.{}.{}.ts'.format(lang, CODE))
        logger.info("make '{}'".format(file_ts))
        command = ['pylupdate6',  # '/usr/lib/qt6/bin/lupdate'
                   '-no-obsolete',
                   '-ts',
                   str(file_ts),
                   ] + list(list_files)
        exit_code = run_command(command).returncode
        if exit_code:
            break

        dir_mo = TEXTDOMAINDIR.joinpath(lang, 'LC_MESSAGES')
        dir_mo.mkdir(parents=True, exist_ok=True)

        file_qm = dir_mo.joinpath(domain + '.qm')
        logger.info("make '{}'".format(file_qm))
        command = ['/usr/lib/qt6/bin/lrelease',
                   str(file_ts),
                   '-qm',
                   str(file_qm),
                   ]
        exit_code = run_command(command).returncode
        if exit_code:
            break

    return exit_code


def main() -> int:
    # --------

    # --------
    arguments = arg_parser.parse_args()
    # --------

    # --------
    DIR_PO.mkdir(parents=True, exist_ok=True)

    list_files = tuple(
        str(path.relative_to(SRC_DIR.parent))
        for path in SRC_DIR.rglob('*.[pP][yY]')
        if not path.relative_to(SRC_DIR.parent).is_relative_to('src/libs/args/__init__.py')
    )
    list_files += tuple(
        str(path.relative_to(SRC_DIR.parent))
        for path in SRC_DIR.rglob('*.[uU][iI]')
    )
    exit_code = gen_ts(DOMAIN, list_files)
    if exit_code:
        return exit_code

    return exit_code


if __name__ == '__main__':
    exit(main())
