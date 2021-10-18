import logging
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot, QResource
from PyQt6.QtWidgets import QMainWindow, QApplication

# from .ui_mainwindow import Ui_MainWindow

logger = logging.getLogger(__name__)


# class MainWindow(QMainWindow, Ui_MainWindow):
class MainWindow(QMainWindow):
    """
    Главное окно.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация класса главного окна.
        :param args:
        """
        super().__init__(*args, **kwargs)
        path = Path(__file__)
        QResource.registerResource(str(path.with_suffix('.rcc')))

        # self.setupUi(self)
        uic.loadUi(path.with_suffix('.ui'), self)

    @pyqtSlot(name='on_actionAboutQtX_triggered')
    def aboutQtX(self):
        """
        Слот раздела меню AboutQtX.
        Выводит окно с версией Qt.
        """
        logger.debug('on_actionAboutQtX_triggere')
        QApplication.aboutQt()
