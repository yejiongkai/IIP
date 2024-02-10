from PyQt5.Qt import QMessageBox, QAction, QSettings, QFileDialog, QMutex, QTimer, QPen, QPainter, QColor, \
    QApplication, QGuiApplication, Qt, QRect, QDialog
import numpy as np
import re
import importlib
import os
import cv2
import sys
from UI_Function.UI_function_picture import UI_function_picture
from UI_Function.UI_function_step import UI_function_step
from UI_Function.UI_function import UI_function
from UI_widget import UI_widget
from UI_THREAD import UI_Thread
from UI_ScreenShot import UI_ScreenShot
from Filter_old import *
from Enhancement_old import *
from Morphology_old import *
from Else import *
from Edge import *
from WaveTrans import *
from Noise import *
import UserDefine as User


class UI(UI_function_step, UI_function_picture, UI_function, UI_widget):
    def __init__(self, debug=False):
        super(UI, self).__init__()
        self.debug = debug
        self.filter_sum = {'Blur': Blur, 'MedianBlur': MedianBlur, 'GaussianBlur': GaussianBlur,
                           'HomoFilter': HomoFilter, 'MatchFilter': MatchFilter, 'FloodFill': FloodFill,
                           'BilateralFilter': BilateralFilter, 'NLM': NLM, 'HighPassFilter': HighPassFilter,
                           'LowPassFilter': LowPassFilter, 'MaxFilter': MaxFilter, 'MinFilter': MinFilter,
                           'GaussianBandFilter': GaussianBandFilter, 'IdealBandFilter': IdealBandFilter,
                           'ButterworthBandFilter': ButterworthBandFilter, 'GuideFilter': GuideFilter,
                           'MeanShiftFilter': MeanShiftFilter, }
        self.enhancement_sum = {'EqualizeHist': EqualizeHist, 'Gamma': Gamma, 'AdaptEqualizeHist': AdaptEqualizeHist,
                                'ConvertScaleAbs': ConvertScaleAbs,
                                'AdaptContrastEnhancement': AdaptContrastEnhancement, 'LogChange': LogChange,
                                'Negate': Negate, 'Threshold': Threshold, 'AdaptiveThreshold': AdaptiveThreshold, }
        self.morphology_sum = {'ERODE': ERODE, 'DILATE': DILATE, 'OPEN': OPEN,
                               'CLOSE': CLOSE, 'TOPHAT': TOPHAT, 'BLACKHAT': BLACKHAT}
        self.else_sum = {'Add': Add, 'Normalize': Normalize, 'Plot_Demo': Plot_Demo, 'Display3D': Display3D,
                         'GrayToBGR': GrayToBGR, 'GrayToHSV': GrayToHSV, 'GrayToYUV': GrayToYUV, 'ELA': ELA,
                         'Resize': Resize, 'LUT': LUT, 'Capture': Capture, 'Maximum': Maximum, 'Minimum': Minimum}
        self.edge_sum = {'Gabor': Gabor, 'Canny': Canny, 'HoughLine': HoughLine, 'Prewitt': Prewitt,
                         'Robert': Robert, 'Sobel': Sobel, 'Laplacian': Laplacian, 'USM': USM}
        self.noise_sum = {'GaussNoise': GaussNoise}
        self.dwt_sum = {'Dwt_User': Dwt_User, 'Dwt_Erode': Dwt_Erode,
                        'Dwt_Gauss': Dwt_Gauss, 'Dwt_Threshold': Dwt_Threshold}
        modules = [self.filter_sum, self.enhancement_sum, self.morphology_sum,
                   self.edge_sum, self.else_sum, self.dwt_sum, self.noise_sum]
        self.SUM = {'算子': UserDefined}
        for module in modules:
            self.SUM.update(module)
        self.settings = None
        ########## 系统截图 #########
        self.setMouseTracking(False)  # 按下时才触发move跟踪
        ########## 缓存配置 ##########
        self.address = None
        self.address_operator = None
        self.address_step = None
        self.cur_image_address = None
        self.cur_step_address = None
        self.cur_operator_address = None
        self.cur_model_address = None
        self.cur_style = None
        self.scale = 1

        self.User_SUM = {}
        self.pictures_info = []
        self.pictures_imgs = []
        self.cachepictures_info = []
        self.cachepictures_imgs = []
        self.steps = []
        self.copy = None
        self.numbers = []
        self.cache_numbers = []
        self.pictures_numbers = []
        self.now = None
        self.User = []
        self.operators = []
        self.model = None
        self.video_close = False

        # self.Model_Init()  # 模型初始化
        self.Read_Settings()
        self.Address()  # 目录初始化
        self.Information_Step()  # 初始化
        self.InitUI()
        self.User_Init()

        self.tooptip_timer = QTimer(self)
        self.tooptip_timer.setInterval(500)

        self.Thread = UI_Thread(self)  # 将显示效果放入另一个线程
        self.Lock = QMutex()
        self.Thread.step_error.connect(self.Error)
        self.Thread.step_range.connect(self.bar.Bar_Show)
        self.Thread.step_value.connect(self.bar.Bar_Show)
        self.Thread.step_end.connect(self.bar.Bar_Show)
        self.Thread.progress_end.connect(self.End)
        self.Thread.JumpShow.connect(self.JumpShow)
        self.show()

    def User_Init(self):
        try:
            importlib.reload(User)
            with open('QT/module/UserDefine.py', 'r+', encoding='utf-8') as f:
                self.UserDefine.clear()
                User_Define = QAction('导入', self)
                User_Define.setStatusTip('导入自定义函数文件')
                User_Define.triggered.connect(self.User_Define)
                self.UserDefine.addAction(User_Define)
                for line in f.readlines():
                    if line[:3] == 'def':
                        name = re.findall('def (.{0,100})\(.{0,100}\)', line)[0]
                        self.User_SUM[name] = eval('User.' + name)
                        action = QAction(name, self)
                        action.setStatusTip(name)
                        action.triggered.connect(lambda: self.ADD(self.sender().text()))
                        self.UserDefine.addAction(action)
        except Exception as error:
            QMessageBox.information(self, '提示', '{}'.format(error))

    def Read_Settings(self):
        settings_address = 'config.ini'
        if not os.path.exists(settings_address):
            with open(settings_address, 'wb+'):
                pass
        self.settings = QSettings(settings_address, QSettings.IniFormat)
        self.address = self.settings.value("ADDRESS")
        self.address_step = self.settings.value('ADDRESS_STEP')
        self.address_operator = self.settings.value('ADDRESS_OPERATOR')
        self.cur_image_address = self.settings.value('CUR_IMAGE_ADDRESS')
        self.cur_step_address = self.settings.value('CUR_STEP_ADDRESS')
        self.cur_operator_address = self.settings.value('CUR_OPERATOR_ADDRESS')
        self.cur_model_address = self.settings.value('CUR_MODEL_ADDRESS')
        self.cur_style = self.settings.value('CUR_STYLE')
        if self.address is None or os.path.exists(self.address) is False:
            if self.address:
                QMessageBox.information(self, '提示', '{}目录不存在'.format(self.address))
            Dir = QFileDialog.getExistingDirectory(self, '选择根目录', 'C:/eyeUI')
            if Dir:
                self.address = Dir
            else:
                sys.exit(0)
        if self.cur_style is None:
            self.cur_style = 'AMOLED'

    def Save_Settings(self):
        self.settings.setValue('ADDRESS', self.address)
        self.settings.setValue('ADDRESS_STEP', self.address_step)
        self.settings.setValue('ADDRESS_OPERATOR', self.address_operator)
        self.settings.setValue('CUR_IMAGE_ADDRESS', self.cur_image_address)
        self.settings.setValue('CUR_STEP_ADDRESS', self.cur_step_address)
        self.settings.setValue('CUR_OPERATOR_ADDRESS', self.cur_operator_address)
        self.settings.setValue('CUR_MODEL_ADDRESS', self.cur_model_address)
        self.settings.setValue('CUR_STYLE', self.cur_style)

    def Screen_Shot(self):
        if self.now is None:
            screenshot = UI_ScreenShot(None, self)
        else:
            if self.now.ndim < 3:
                screenshot = UI_ScreenShot(
                    cv2.resize(cv2.cvtColor(self.now, cv2.COLOR_GRAY2BGR), None, None, fx=self.scale, fy=self.scale),
                    self)
            else:
                screenshot = UI_ScreenShot(
                    cv2.resize(self.now, None, None, fx=self.scale, fy=self.scale), self)
        screenshot.Run()
        screenshot.show()
        if screenshot.exec_() == QDialog.Accepted:
            pos = [screenshot.rectTopleftX, screenshot.rectTopleftY, screenshot.rectHeight, screenshot.rectWidth]
            if screenshot.isScreen:
                actual_TopLeftX, actual_TopLeftY, actual_height, actual_width = pos
                image = screenshot.np_fullScreenImage[actual_TopLeftY:actual_TopLeftY + actual_height,
                        actual_TopLeftX:actual_TopLeftX + actual_width].copy()
            else:
                actual_TopLeftX, actual_TopLeftY, actual_height, actual_width = [int(p / self.scale) for p in pos]
                image = self.now[actual_TopLeftY:actual_TopLeftY + actual_height,
                        actual_TopLeftX:actual_TopLeftX + actual_width].copy()

            self.cachepictures_info.append(
                ['{}'.format(len(self.cachepictures_info)), ["ScreenShot", 0], 0])
            self.cachepictures_imgs.append([cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) if screenshot.isScreen else image,])
            self.CacheRefresh()
            # self.Show_Picture("result", image)
