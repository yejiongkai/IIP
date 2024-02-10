from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QComboBox, QPushButton, QTreeWidgetItemIterator, \
    QMessageBox, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, QMimeData, QVariant, QPoint, pyqtSignal
from PyQt5 import QtGui, QtCore


class UI_List(QTreeWidget):
    item_row_changed = pyqtSignal(tuple, tuple)

    def __init__(self, parent):
        super(UI_List, self).__init__(parent)
        self._vertical_scroll_value = 0
        self._start_item_row = None
        self._end_item_row = None
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setColumnCount(1)
        self.header().setHidden(True)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)  # 避免内容被省略
        self.header().setStretchLastSection(False)
        self.setAutoScroll(False)
        self.setExpandsOnDoubleClick(False)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setSelectionBehavior(QTreeWidget.SelectItems)
        self.setMouseTracking(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # 内部item移动
        if event.source() == self:
            if self.currentIndex().parent().isValid():
                self._start_item_row = (self.currentIndex().parent().row(), self.currentIndex().row())
            else:
                self._start_item_row = (self.currentIndex().row(), None)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        try:
            # 拖动到边界，自动滚动
            y = event.pos().y()
            height = self.height()
            if y <= 20:
                self._vertical_scroll_value = self.verticalScrollBar().value() - 1
                self.verticalScrollBar().setValue(self._vertical_scroll_value)
            elif y >= height - 50:
                self._vertical_scroll_value = self.verticalScrollBar().value() + 1
                self.verticalScrollBar().setValue(self._vertical_scroll_value)

            item: QTreeWidgetItem = self.itemAt(event.pos())
            # 如果拖动目的item为空
            if item is None:
                event.ignore()
                return
            else:
                event.accept()

            # # 如果拖动目的item不允许drop
            # des_flags = self.itemAt(event.pos()).flags().__int__()
            # if des_flags & Qt.ItemIsDropEnabled == 0:
            #     event.ignore()
            #     return

        except Exception as e:
            QMessageBox.warning(self, "drapMoveEvent_Error", '{}'.format(e))

    # 释放鼠标时Event
    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        try:
            # 内部拖拽item
            if event.source() == self:
                item = self.indexAt(event.pos())
                if item is not None:
                    if item.parent().isValid():
                        self._end_item_row = (item.parent().row(), item.row())
                    else:
                        self._end_item_row = (item.row(), None)

                    if self._start_item_row is not None and self._end_item_row is not None:
                        self.item_row_changed.emit(self._start_item_row, self._end_item_row)
            else:
                event.ignore()

        except Exception as e:
            QMessageBox.warning(self, "DropError",  '{}'.format(e))
