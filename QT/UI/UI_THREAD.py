from PyQt5.Qt import QThread, pyqtSignal


class UI_Thread(QThread):
    step_range = pyqtSignal(str, int)
    step_value = pyqtSignal(str, int)
    step_end = pyqtSignal(str, int)
    step_error = pyqtSignal(str, str, str)
    progress_end = pyqtSignal()
    JumpShow = pyqtSignal(int)

    def __init__(self, parent):
        super(UI_Thread, self).__init__(parent)
        self.parent = parent
        self.stop = False



