import tempfile

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFontMetrics, QPainter
from hydrus.client import ClientGlobals as CG
from qtpy import QtGui as QG
from hydrus.core import HydrusGlobals as HG
from qtpy.QtWidgets import QApplication, QMainWindow
from hydrus.client.gui import ClientGUIFunctions as CGF


# noinspection PyPep8Naming,PyMethodMayBeStatic
class FakeBitmapManager:
    FORMAT = {
        24: QG.QImage.Format.Format_RGB888,
        32: QG.QImage.Format.Format_RGBA8888,
    }
    
    def GetQtImage(self, width, height, depth):
        return QG.QImage(width, height, self.FORMAT[depth])
    # end def
# end class

class FakeClientController:
    def __init__(self):
        self.bitmap_manager = FakeBitmapManager()
    # end def
# end class


class FakeHydrusController:
    def __init__(self):
        self._tmp_dir = tempfile.mkdtemp()

    def GetHydrusTempDir(self):
        return self._tmp_dir
    # end def
# end class


def patch():
    CG.client_controller = FakeClientController()
    print('HydrusGlobals patched with FakeClientController')
    # app = QApplication([])
    print('prepared QApplication')
    # QMainWindow.insertToolBar = lambda *args, **kwargs: None
    # QMainWindow.menuBar = lambda *args, **kwargs: None
    # window = QMainWindow()
    print('prepared QMainWindow')
    front_metrics = QFontMetrics(QG.QFont())
    CGF.GetTextSizeFromPainter = lambda painter, text: (QSize(len(text) * 20, 20), text)
    QG.QPainter.fontMetrics = lambda painter: front_metrics
    # QPainter(text_extent_qt_image)

    HG.controller = FakeHydrusController()
    print('set the value instead of the real HydrusGlobals.controller')
# end def
