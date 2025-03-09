import tempfile

from hydrus.client import ClientGlobals as CG
from qtpy import QtGui as QG
from hydrus.core import HydrusGlobals as HG
from qtpy.QtWidgets import QApplication, QMainWindow


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
    app = QApplication([])
    window = QMainWindow()

    HG.controller = FakeHydrusController()
# end def
