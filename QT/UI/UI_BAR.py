from PyQt5.Qt import QProgressBar


class UI_Bar(QProgressBar):

    def __init__(self, parent):
        super(UI_Bar, self).__init__(parent)
        self.setHidden(True)
    def Bar_Show(self, t, value):
        if t == 'range':
            self.setRange(0, value)
        if t == 'value':
            self.setValue(value)
        if t == 'end':
            if value == 0:
                self.setHidden(True)
            else:
                self.setRange(0, 0)