#!/usr/bin/env python3
import logging
import sys

from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtWidgets import QApplication

import libs.logs.args
from libs import DOMAIN, TEXTDOMAINDIR
from libs.args import arg_parser
from qt.window.mainwindow import MainWindow

libs.logs.args.run()

logger = logging.getLogger(DOMAIN)


def main() -> int:
    # --------

    # --------
    arguments = arg_parser.parse_args()
    # --------

    # --------
    logger.info('app')
    app = QApplication(sys.argv)

    translator = QTranslator()
    qt_lang_dir = TEXTDOMAINDIR.joinpath(QLocale.system().name(), 'LC_MESSAGES')
    translator.load(DOMAIN, str(qt_lang_dir))
    app.installTranslator(translator)

    logger.info('main_window')
    main_window = MainWindow()
    logger.info('show')
    main_window.show()

    logger.info('exec')
    exit_code = app.exec()
    logger.info('exit_code={}'.format(exit_code))
    return exit_code


if __name__ == '__main__':
    exit(main())
