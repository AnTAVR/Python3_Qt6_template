#!/usr/bin/env python3
import logging
import os

import src.libs.logs.args
from src.libs import SRC_DIR
from src.libs.all import run_command
from src.libs.args import arg_parser

src.libs.logs.args.run(logging.DEBUG)

logger = logging.getLogger(__name__)

DIR_QT = SRC_DIR.joinpath('qt')

ENV = os.environ.copy()
ENV['PYTHONPATH'] = os.pathsep.join(x for x in (
    str(DIR_QT.joinpath('window')),
    str(DIR_QT.joinpath('widget')),
    # str(DIR_QT),
    ENV.get('PYTHONPATH', None)
) if x)


def main() -> int:
    # --------

    # --------
    arguments = arg_parser.parse_args()
    # --------

    # --------
    """
    Генерирует ресурсы *.qrc и *.ui по заданному пути
    """
    exit_code = os.EX_OK
    for input_file_path in DIR_QT.rglob('*.*'):
        if not input_file_path.is_file():
            continue

        file_name, file_ext = os.path.splitext(input_file_path.name)
        if file_ext == '.ui':
            file_name = 'ui_' + file_name + '.py'
            # command = ['/usr/lib/qt6/uic', '-g', 'python']  # PySide6
            command = ['pyuic6', ]  # PyQt6
        elif file_ext == '.qrc':
            file_name += '.rcc'  # PyQt6
            command = ['/usr/lib/qt6/rcc', '--binary']  # PyQt6
        #     file_name += '_rc.py'  # PySide6
        #     command = ['/usr/lib/qt6/rcc', '-g', 'python']  # PySide6
        else:
            continue
        out_file_path = input_file_path.with_name(file_name)

        if out_file_path.exists() and input_file_path.stat().st_mtime_ns <= out_file_path.stat().st_mtime_ns:
            continue

        command += ['-o', str(out_file_path.relative_to(SRC_DIR)), str(input_file_path.relative_to(SRC_DIR))]
        exit_code = run_command(command, str(SRC_DIR), ENV).returncode
        if exit_code:
            return exit_code

    return exit_code


if __name__ == '__main__':
    exit(main())
