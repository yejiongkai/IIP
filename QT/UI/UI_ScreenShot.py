import sys, time, logging
import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPen, QPainter, QColor, QGuiApplication, QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QDialog


class UI_ScreenShot(QDialog):
    fullScreenImage = None
    np_fullScreenImage = None
    captureImage = None
    isMousePressLeft = None
    isScreen = None
    beginPosition = None
    endPosition = None
    rectWidth = None
    rectHeight = None
    rectTopleftX = None
    rectTopleftY = None
    isMove = False
    movePosition = None

    # 创建 QPainter 对象
    painter = QPainter()

    def __init__(self, img, parent=None):
        super(UI_ScreenShot, self).__init__(parent)
        self.setMouseTracking(False)  # 按下时才触发move跟踪
        if img is None:
            self.isScreen = True
            self.captureFullScreen()
            image = self.fullScreenImage.toImage()  # 得到的是四通道图像
            width = image.width()
            height = image.height()
            byte_buffer = image.bits().asstring(width * height * 4)
            self.np_fullScreenImage = np.frombuffer(byte_buffer, np.uint8).reshape((height, width, 4))
        else:
            self.isScreen = False
            height, width = img.shape[:2]
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)
            self.fullScreenImage = QPixmap.fromImage(qImg)
            self.np_fullScreenImage = img.copy()
        self.save_img = None

    def Run(self):
        self.initWindow()  # 初始化窗口
        # self.captureFullScreen()  # 捕获全屏

    def initWindow(self):
        self.setCursor(Qt.CrossCursor)  # 设置光标
        self.setWindowFlag(Qt.FramelessWindowHint)  # 产生无边框窗口，用户不能通过窗口系统移动或调整无边界窗口的大小
        self.setWindowState(Qt.WindowFullScreen)  # 窗口全屏无边框

    def captureFullScreen(self):
        # 捕获当前屏幕，返回像素图
        self.fullScreenImage = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

    def paintBackgroundImage(self):
        # 填充颜色，黑色半透明
        fillColor = QColor(0, 0, 0, 100)
        # 加载显示捕获的图片到窗口
        self.painter.drawPixmap(0, 0, self.fullScreenImage)
        # 填充颜色到给定的矩形
        self.painter.fillRect(self.fullScreenImage.rect(), fillColor)

    def getRectangle(self, beginPoint, endPoint):
        # 计算矩形宽和高
        self.rectWidth = int(abs(beginPoint.x() - endPoint.x()))
        self.rectHeight = int(abs(beginPoint.y() - endPoint.y()))
        # 计算矩形左上角 x 和 y
        self.rectTopleftX = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
        self.rectTopleftY = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
        # 构造一个以（x，y）为左上角，给定宽度和高度的矩形
        pickRect = QRect(self.rectTopleftX, self.rectTopleftY, self.rectWidth, self.rectHeight)
        # 调试日志
        # logging.info('开始坐标：%s,%s', beginPoint.x(),beginPoint.y())
        # logging.info('结束坐标：%s,%s', endPoint.x(), endPoint.y())
        return pickRect

    def paintSelectBox(self):
        # 画笔颜色，蓝色
        penColor = QColor(30, 150, 255)  # 画笔颜色
        textColor = QColor(255, 255, 255)
        # 设置画笔属性，蓝色、2px大小、实线
        self.painter.setPen(QPen(penColor, 2, Qt.SolidLine))
        if self.isMousePressLeft is True \
                and self.beginPosition.x() != self.endPosition.x() \
                and self.beginPosition.y() != self.endPosition.y():
            pickRect = self.getRectangle(self.beginPosition, self.endPosition)  # 获得要截图的矩形框
            self.captureImage = self.fullScreenImage.copy(pickRect)  # 捕获截图矩形框内的图片
            self.painter.drawPixmap(pickRect.topLeft(), self.captureImage)  # 填充截图的图片
            self.painter.drawRect(pickRect)  # 绘制矩形边框
            self.painter.setPen(QPen(textColor, 2, Qt.SolidLine))
            self.painter.setFont(QFont("Arial", 12 if (self.rectWidth / 30) < 12 else (self.rectWidth // 30)
            if (self.rectWidth / 30) < 30 else 30))
            self.painter.drawText(self.rectTopleftX + 5, self.rectTopleftY - 8,
                                  "({},{})".format(self.rectTopleftX, self.rectTopleftY))
            self.painter.drawText(self.rectTopleftX + self.rectWidth + self.rectHeight // 50,
                                  self.rectTopleftY + self.rectHeight // 2, str(self.rectHeight))
            self.painter.drawText(self.rectTopleftX + self.rectWidth // 2,
                                  self.rectTopleftY + self.rectHeight + 15 + self.rectWidth // 50, str(self.rectWidth))

    def paintEvent(self, event):
        self.painter.begin(self)  # 开始绘制
        self.paintBackgroundImage()  # 绘制背景
        self.paintSelectBox()  # 绘制选框
        self.painter.end()  # 结束绘制

    def mousePressEvent(self, event):
        # 如果鼠标事件为左键，则记录起始鼠标光标相对于窗口的位置
        if event.button() == Qt.LeftButton:
            if self.beginPosition is not None and self.beginPosition.x() < event.pos().x() < self.endPosition.x() and \
                    self.beginPosition.y() < event.pos().y() < self.endPosition.y():
                self.isMove = True
                self.movePosition = event.pos()
            else:
                self.beginPosition = event.pos()
            self.isMousePressLeft = True
        # 如果鼠标事件为右键，不改变起始点
        if event.button() == Qt.RightButton:
            if self.captureImage is not None:
                self.captureImage = None
                self.update()  # 更新，会擦除之前的选框

    def mouseMoveEvent(self, event):
        if self.isMove:
            self.beginPosition.setX(self.beginPosition.x() + event.pos().x() - self.movePosition.x())
            self.beginPosition.setY(self.beginPosition.y() + event.pos().y() - self.movePosition.y())
            self.endPosition.setX(self.endPosition.x() + event.pos().x() - self.movePosition.x())
            self.endPosition.setY(self.endPosition.y() + event.pos().y() - self.movePosition.y())
            self.movePosition = event.pos()

        else:
            self.endPosition = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.isMove:
            self.isMove = False
        else:
            self.endPosition = event.pos()

    def saveImage(self):
        image = self.captureImage.toImage()  # 得到的是四通道图像
        width = image.width()
        height = image.height()
        byte_buffer = image.bits().asstring(width * height * 4)
        self.save_img = np.frombuffer(byte_buffer, np.uint8).reshape((height, width, 4))

    def keyPressEvent(self, event):
        # 如果按下 ESC 键，则退出截图
        if event.key() == Qt.Key_Escape:
            self.reject()
        # 如果按下 Enter 键，并且已经选取了区域，就截图选区图片
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.captureImage is not None:
                # self.saveImage()
                self.accept()
                # self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建 QApplication 对象
    windows = UI_ScreenShot(img=None)  # 创建 Screenshot 对象
    windows.Run()
    windows.show()
    sys.exit(app.exec_())  # 进入主事件循环并等待直到 exit() 被调用
