#! /usr/bin/env python3
import logging
import subprocess
import tempfile
from typing import Sequence

import src.libs.logs.args
from src.libs import DOMAIN, TEXTDOMAINDIR, SRC_DIR, DIR_PO
from src.libs.all import run_command
from src.libs.args import arg_parser

src.libs.logs.args.run(logging.DEBUG)

logger = logging.getLogger(__name__)

ADDRESS = '{}@antavr.ru'.format(DOMAIN)
COPYRIGHT = ''
CODE = 'UTF-8'
LANGS = ('ru_RU',)

__ver1 = subprocess.run(['git',
                         'rev-list',
                         '--count',
                         'HEAD',
                         ], capture_output=True).stdout.decode().strip()
__ver2 = subprocess.run(['git',
                         'rev-parse',
                         '--short',
                         'HEAD',
                         ], capture_output=True).stdout.decode().strip()

VERSION = '{}.{}'.format(__ver1, __ver2)


def gen_mo(domain: str, list_files: Sequence[str]):
    tmp_file = tempfile.NamedTemporaryFile('w+t', newline='\n')
    tmp_file.writelines(list_files)
    tmp_file.flush()

    file_pot = DIR_PO.joinpath(domain + '.pot')

    logger.info("make '{}'".format(file_pot))
    command = ['xgettext',
               '--sort-output',
               '--default-domain={}'.format(domain),
               '--package-name={}'.format(domain),
               '--package-version={}'.format(VERSION),
               '--msgid-bugs-address={}'.format(ADDRESS),
               '--copyright-holder={}'.format(COPYRIGHT),
               '--files-from={}'.format(tmp_file.name),
               '--from-code={}'.format(CODE),
               '--output={}'.format(file_pot),
               ]
    exit_code = run_command(command).returncode

    tmp_file.close()

    if exit_code:
        return exit_code

    for lang in LANGS:
        file_po = file_pot.with_suffix('.{}.{}.po'.format(lang, CODE))
        if file_po.exists():
            logger.info("merge '{}'".format(file_po))
            command = ['msgmerge',
                       '--sort-output',
                       '--update',
                       '--multi-domain',
                       '--previous',
                       '--backup=off',
                       '--lang={}'.format(lang),
                       '{}'.format(file_po),
                       '{}'.format(file_pot),
                       ]
        else:
            logger.info("make '{}'".format(file_po))
            command = ['msginit',
                       '--no-translator',
                       '--locale={}.{}'.format(lang, CODE),
                       '--input={}'.format(file_pot),
                       '--output-file={}'.format(file_po),
                       ]
        exit_code = run_command(command).returncode
        if exit_code:
            break

        dir_mo = TEXTDOMAINDIR.joinpath(lang, 'LC_MESSAGES')
        dir_mo.mkdir(parents=True, exist_ok=True)

        file_mo = dir_mo.joinpath(domain + '.mo')
        logger.info("make '{}'".format(file_mo))
        command = ['msgfmt',
                   '--output-file={}'.format(file_mo),
                   '{}'.format(file_po),
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
    import argparse
    list_files = (argparse.__file__ + '\n', 'src/libs/args/__init__.py')
    exit_code = gen_mo(argparse.__name__, list_files)
    if exit_code:
        return exit_code

    DIR_PO.mkdir(parents=True, exist_ok=True)

    list_files = tuple(
        str(path.relative_to(SRC_DIR.parent)) + '\n'
        for path in SRC_DIR.rglob('*.[pP][yY]')
        if not path.relative_to(SRC_DIR.parent).is_relative_to('src/libs/args/__init__.py')
    )
    exit_code = gen_mo(DOMAIN, list_files)
    if exit_code:
        return exit_code

    return exit_code


if __name__ == '__main__':
    exit(main())
