from PyQt5.Qt import QFont, QTabWidget, QApplication, QPushButton, QWidget, QDialog, QTableWidget, \
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QHeaderView, QSizePolicy, QAbstractScrollArea
from PyQt5.QtCore import Qt
import sys
import numpy as np
import cv2
import re


class UI_Modify(QDialog):
    def __init__(self, steps, parent=None):
        super(UI_Modify, self).__init__(parent)
        self.steps = steps
        self.result = []

        row = len(self.steps)
        col = max([(len(eval(pam[1])) if isinstance(eval(pam[1]), tuple) else 1) for pam in self.steps]) + 1
        self.table = QTableWidget(row, col, self)

        self.initUI()

    def initUI(self):
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)   # QSizePolicy.Expanding, QSizePolicy.Expanding
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.itemChanged.connect(self.item_activate)
        for i, (method, pam_s) in enumerate(self.steps):
            # pam = re.findall('\((.{0,100})\)', pam_s)[0].split(",")
            pam = eval(pam_s) if eval(pam_s) else [None]
            table_item = QTableWidgetItem(method)
            table_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, table_item)
            for j, p in enumerate(pam):
                if isinstance(p, str):
                    table_item = QTableWidgetItem("'{}'".format(p))
                else:
                    table_item = QTableWidgetItem(str(p))
                table_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j + 1, table_item)

        # self.setMinimumSize(table.sizeHint())
        # self.resize(500, 500)
        bt1 = QPushButton("OK", self)
        bt1.setFont(QFont("Times New Roman", 13))
        b_sp = QSizePolicy()
        b_sp.setWidthForHeight(True)
        bt1.setSizePolicy(b_sp)
        bt1.clicked.connect(self.return_steps)
        # bt2 = QPushButton("取消", self)
        # bt2.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addWidget(bt1)
        # hbox.addWidget(bt2)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def item_activate(self, item):
        item.setTextAlignment(Qt.AlignCenter)

    def return_steps(self):
        row, col = self.table.rowCount(), self.table.columnCount()
        self.result = []
        for i in range(row):
            method = self.table.item(i, 0).text()
            if method:
                step = (method, '(' + ','.join([self.table.item(i, j).text() for j in range(1, col)
                                                if self.table.item(i, j) is not None
                                                and self.table.item(i, j).text() != ""]) + ")")
                self.result.append(step)

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # example = UI_Modify(
    #     [('Normalize', '(0, 69, cv2.NORM_MINMAX, 1, 1, 1, 1)'), ('Normalize', '(0, 127, cv2.NORM_MINMAX)'),
    #      ('Normalize', '(127, 255, cv2.NORM_MINMAX)')])
    example = UI_Modify(
        [('Normalize', '(None)'), ('Normalize', '(None, None, None)'), ('Normalize', '(None)')])
    sys.exit(example.exec_())
