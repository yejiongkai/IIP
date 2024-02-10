from PyQt5.Qt import QWidget, QPushButton, QMainWindow, QAction, QLabel, QMenu, QLineEdit, QListWidget,\
                        QFont, QCheckBox, QIntValidator, QTreeWidget, QAbstractItemView, QHeaderView, QDockWidget, \
                        QHBoxLayout, QVBoxLayout, QSplitter, QToolBar, QComboBox, QListWidgetItem, QIcon, QSize
from PyQt5.QtCore import QPoint, Qt
from UI_BAR import UI_Bar
from UI_List import UI_List
import os


class UI_widget(QMainWindow):
    def InitUI(self):
        self.setWindowTitle('IIP')
        self.setGeometry(400, 200, 1200, 1000)
        # self.setFixedSize(self.width(), self.height())
        self.statusBar().showMessage('准备就绪')
        self.font = QFont("Microsoft YaHei ")
        self.font.setPointSize(10)
        self.StyleChange(self.cur_style)

        #######################文件菜单########################

        stylechange = QMenu('风格设置', self)
        style_Ubuntu = QAction('Ubuntu', self)
        style_Ubuntu.triggered.connect(lambda: self.StyleChange('Ubuntu'))
        style_MacOS = QAction('MacOS', self)
        style_MacOS.triggered.connect(lambda: self.StyleChange('MacOS'))
        style_AMOLED = QAction('AMOLED', self)
        style_AMOLED.triggered.connect(lambda: self.StyleChange('AMOLED'))
        style_ElegantDark = QAction('ElegantDark', self)
        style_ElegantDark.triggered.connect(lambda: self.StyleChange('ElegantDark'))
        style_ConsoleStyle = QAction('ConsoleStyle', self)
        style_ConsoleStyle.triggered.connect(lambda: self.StyleChange('ConsoleStyle'))
        style_ManjaroMix = QAction('ManjaroMix', self)
        style_ManjaroMix.triggered.connect(lambda: self.StyleChange('ManjaroMix'))
        stylechange.addActions([style_Ubuntu, style_MacOS, style_AMOLED, style_ElegantDark, style_ConsoleStyle, style_ManjaroMix])

        exitAct = QAction('退出(&E)', self)  # 退出
        exitAct.setShortcut('Ctrl+A')  # 设置快捷键
        exitAct.triggered.connect(self.close)  # 连接到quit()方法，当触发特定动作时会被使用

        newAct = QMenu('新建(&N)', self)

        newAct_Single = QAction('单通道图片', self)
        newAct_Single.triggered.connect(lambda: self.New(0))
        newAct_Multi = QAction('多通道图片', self)
        newAct_Multi.triggered.connect(lambda: self.New(1))
        newAct_Video = QAction("视频", self)
        newAct_Video.triggered.connect(lambda: self.New(2))
        newAct.addActions([newAct_Single, newAct_Multi, newAct_Video])

        newStep = QAction('新建步骤文件', self)
        newStep.triggered.connect(self.MakeStepProject)

        openstepfile = QAction('打开步骤文件', self)
        openstepfile.triggered.connect(self.OpenStepProject)

        saveAct = QAction('保存图片', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(self.SaveImage)

        #######################滤波处理#########################
        HighPassFilter = QAction('HighPassFilter', self)
        HighPassFilter.setStatusTip('高通滤波')
        HighPassFilter.triggered.connect(lambda: self.ADD('HighPassFilter'))

        LowPassFilter = QAction('LowPassFilter', self)
        LowPassFilter.setStatusTip('低通滤波')
        LowPassFilter.triggered.connect(lambda: self.ADD('LowPassFilter'))

        IdealBandFilter = QAction('IdealBandFilter', self)
        IdealBandFilter.setStatusTip('理想带阻/带通滤波器')
        IdealBandFilter.triggered.connect(lambda: self.ADD('IdealBandFilter'))

        ButterworthBandFilter = QAction('ButterworthBandFilter', self)
        ButterworthBandFilter.setStatusTip('n阶巴特沃斯陷波带阻滤波器')
        ButterworthBandFilter.triggered.connect(lambda: self.ADD('ButterworthBandFilter'))

        GaussianBandFilter = QAction('GaussianBandFilter', self)
        GaussianBandFilter.setStatusTip('GaussianBandFilter')
        GaussianBandFilter.triggered.connect(lambda: self.ADD('GaussianBandFilter'))

        NLM = QAction('NLM', self)  # NLM滤波
        NLM.setStatusTip('非局部去噪方法')
        NLM.triggered.connect(lambda: self.ADD('NLM'))

        Blur = QAction('Blur', self)  # 均值过滤
        Blur.setStatusTip('均值滤波')
        Blur.triggered.connect(lambda: self.ADD('Blur'))

        MedianBlur = QAction('MedianBlur', self)  # 中值过滤
        MedianBlur.triggered.connect(lambda: self.ADD('MedianBlur'))
        MedianBlur.setStatusTip('中值滤波')

        GaussianBlur = QAction('GaussianBlur', self)  # 高斯滤波
        GaussianBlur.triggered.connect(lambda: self.ADD('GaussianBlur'))
        GaussianBlur.setStatusTip('高斯滤波')

        MaxFilter = QAction('MaxFilter', self)  # 最大值滤波
        MaxFilter.triggered.connect(lambda: self.ADD('MaxFilter'))
        MaxFilter.setStatusTip('最大值滤波')

        MinFilter = QAction('MinFilter', self)  # 最小值滤波
        MinFilter.triggered.connect(lambda: self.ADD('MinFilter'))
        MinFilter.setStatusTip('最小值滤波')

        BilateralFilter = QAction('BilateralFilter', self)  # 双边滤波
        BilateralFilter.triggered.connect(lambda: self.ADD('BilateralFilter'))
        BilateralFilter.setStatusTip('双边滤波')

        HomoFilter = QAction('HomoFilter', self)  # 同态滤波
        HomoFilter.triggered.connect(lambda: self.ADD('HomoFilter'))
        HomoFilter.setStatusTip('同态滤波')

        MatchFilter = QAction('MatchFilter', self)  # 匹配滤波
        MatchFilter.triggered.connect(lambda: self.ADD('MatchFilter'))
        MatchFilter.setStatusTip('匹配滤波')

        GuideFilter = QAction('GuideFilter', self)  #指导性滤波
        GuideFilter.triggered.connect(lambda: self.ADD('GuideFilter'))
        GuideFilter.setStatusTip('指导性滤波')

        MeanShiftFilter = QAction('MeanShiftFilter', self)
        MeanShiftFilter.setStatusTip('均值平移')
        MeanShiftFilter.triggered.connect(lambda: self.ADD('MeanShiftFilter'))

        FloodFill = QAction('FloodFill', self)
        FloodFill.triggered.connect(lambda: self.ADD('FloodFill'))
        FloodFill.setStatusTip('漫水填充')

        #######################增强#########################

        EqualizeHist = QAction('EqualizeHist', self)  # 直方图均衡化
        EqualizeHist.setStatusTip('直方图均衡化')
        EqualizeHist.triggered.connect(lambda: self.ADD('EqualizeHist'))

        # CalcBackProject = QAction('CalcBackProject', self)  # 直方图反向投影
        # CalcBackProject.setStatusTip('直方图反向投影')
        # CalcBackProject.triggered.connect(lambda: self.ADD('CalcBackProject'))

        AdaptEqualizeHist = QAction('AdaptEqualizeHist', self)  # 自适应直方图均衡化
        AdaptEqualizeHist.setStatusTip('自适应直方图均衡化')
        AdaptEqualizeHist.triggered.connect(lambda: self.ADD('AdaptEqualizeHist'))

        AdaptContrastEnhancement = QAction('AdaptContrastEnhancement', self)  # 自适应对比度增强
        AdaptContrastEnhancement.setStatusTip('自适应对比度增强')
        AdaptContrastEnhancement.triggered.connect(lambda: self.ADD('AdaptContrastEnhancement'))

        LogChange = QAction('LogChange', self)  # 对数变换
        LogChange.setStatusTip('对数变换')
        LogChange.triggered.connect(lambda: self.ADD('LogChange'))

        Gamma = QAction('Gamma', self)
        Gamma.setStatusTip('Gamma变换')
        Gamma.triggered.connect(lambda: self.ADD('Gamma'))

        ConvertScaleAbs = QAction('ConvertScaleAbs', self)  # 调整亮度和对比度
        ConvertScaleAbs.setStatusTip('调整亮度和对比度')
        ConvertScaleAbs.triggered.connect(lambda: self.ADD('ConvertScaleAbs'))

        Threshold = QAction('Threshold', self)  # 阈值处理
        Threshold.setStatusTip('阈值处理')
        Threshold.triggered.connect(lambda: self.ADD('Threshold'))

        AdaptiveThreshold = QAction('AdaptiveThreshold', self)
        AdaptiveThreshold.setStatusTip('自适应阈值')
        AdaptiveThreshold.triggered.connect(lambda: self.ADD('AdaptiveThreshold'))

        Negate = QAction('Negate', self)  # 取反
        Negate.setStatusTip('取反')
        Negate.triggered.connect(lambda: self.ADD('Negate'))

        ########################边缘检测#########################
        HoughLine = QAction('HoughLine', self)
        HoughLine.setStatusTip('霍夫直线检测')
        HoughLine.triggered.connect(lambda: self.ADD('HoughLine'))

        Gabor = QAction('Gabor', self)  # Gabor滤波
        Gabor.triggered.connect(lambda: self.ADD('Gabor'))
        Gabor.setStatusTip('Gabor')

        Prewitt = QAction('Prewitt', self)
        Prewitt.setStatusTip('Prewitt')
        Prewitt.triggered.connect(lambda: self.ADD('Prewitt'))

        Robert = QAction('Robert', self)
        Robert.setStatusTip('Robert')
        Robert.triggered.connect(lambda: self.ADD('Robert'))

        Canny = QAction('Canny', self)  # Canny滤波
        Canny.setStatusTip('Canny滤波')
        Canny.triggered.connect(lambda: self.ADD('Canny'))

        Sobel = QAction('Sobel', self)
        Sobel.setStatusTip('Sobel')
        Sobel.triggered.connect(lambda: self.ADD('Sobel'))

        Laplacian = QAction('Laplacian', self)
        Laplacian.setStatusTip('Laplacian')
        Laplacian.triggered.connect(lambda: self.ADD('Laplacian'))

        USM = QAction('USM', self)
        USM.setStatusTip('USM')
        USM.triggered.connect(lambda: self.ADD('USM'))
        #######################形态学操作######################
        OPEN = QAction('OPEN', self)
        OPEN.setStatusTip('开运算')
        OPEN.triggered.connect(lambda: self.ADD('OPEN'))

        CLOSE = QAction('CLOSE', self)
        CLOSE.setStatusTip('闭运算')
        CLOSE.triggered.connect(lambda: self.ADD('CLOSE'))

        DILATE = QAction('DILATE', self)
        DILATE.setStatusTip('膨胀')
        DILATE.triggered.connect(lambda: self.ADD('DILATE'))

        ERODE = QAction('ERODE', self)
        ERODE.setStatusTip('腐蚀')
        ERODE.triggered.connect(lambda: self.ADD('ERODE'))

        TOPHAT = QAction('TOPHAT', self)
        TOPHAT.setStatusTip('顶帽')
        TOPHAT.triggered.connect(lambda: self.ADD('TOPHAT'))

        BLACKHAT = QAction('BLACKHAT', self)
        BLACKHAT.setStatusTip('黑帽')
        BLACKHAT.triggered.connect(lambda: self.ADD('BLACKHAT'))

        ####################小波变换#######################

        dwt_user = QAction('Dwt_User', self)
        dwt_user.setStatusTip('自定义小波去噪')
        dwt_user.triggered.connect(lambda: self.ADD('Dwt_User'))

        dwt_erode = QAction('Dwt_Erode', self)
        dwt_erode.setStatusTip('小波腐蚀去噪')
        dwt_erode.triggered.connect(lambda: self.ADD('Dwt_Erode'))

        dwt_gauss = QAction('Dwt_Gauss', self)
        dwt_gauss.setStatusTip('小波高斯去噪')
        dwt_gauss.triggered.connect(lambda: self.ADD('Dwt_Gauss'))

        dwt_threshold = QAction('Dwt_Threshold', self)
        dwt_threshold.setStatusTip('小波阈值去噪')
        dwt_threshold.triggered.connect(lambda: self.ADD('Dwt_Threshold'))

        ##################噪声##############################

        GaussNoise = QAction('GaussNoise', self)
        GaussNoise.setStatusTip('高斯噪声')
        GaussNoise.triggered.connect(lambda: self.ADD('GaussNoise'))

        ######################其它##########################
        Add = QAction('Add', self)
        Add.setStatusTip('图像相加')
        Add.triggered.connect(lambda: self.ADD('Add'))

        Subtract = QAction('Subtract', self)  # 相减
        Subtract.setStatusTip('图片相减')
        Subtract.triggered.connect(lambda: self.ADD('Subtract'))

        Plot_Demo = QAction('灰度直方图', self)  # 灰度直方图
        Plot_Demo.setStatusTip('灰度直方图')
        Plot_Demo.triggered.connect(lambda: self.ADD('Plot_Demo'))

        Display3D = QAction('3D图像显示', self)  # 3D图像显示
        Display3D.setStatusTip('3D图像显示（只支持单通道）')
        Display3D.triggered.connect(lambda: self.ADD('Display3D'))

        Resize = QAction('Resize', self)
        Resize.setStatusTip('修改图片尺寸')
        Resize.triggered.connect(lambda: self.ADD('Resize'))

        Partial = QAction('Partial', self)
        Partial.setStatusTip('局部窗口')
        Partial.triggered.connect(lambda: self.ADD('Partial'))

        Normalize = QAction('Normalize', self)
        Normalize.setStatusTip('归一化')
        Normalize.triggered.connect(lambda: self.ADD('Normalize'))

        LUT = QAction('LUT', self)
        LUT.setStatusTip('快速上色')
        LUT.triggered.connect(lambda: self.ADD('LUT'))

        Capture = QAction('Capture', self)
        Capture.setStatusTip('查看色素区间')
        Capture.triggered.connect(lambda: self.ADD('Capture'))

        Maximum = QAction('Maximum', self)
        Maximum.setStatusTip('取最大')
        Maximum.triggered.connect(lambda: self.ADD('Maximum'))

        Minimum = QAction('Minimum', self)
        Minimum.setStatusTip('取最小')
        Minimum.triggered.connect(lambda: self.ADD('Minimum'))

        GrayToBGR = QAction('GrayToBGR', self)
        GrayToBGR.setStatusTip('灰度转BGR')
        GrayToBGR.triggered.connect(lambda: self.ADD('GrayToBGR'))

        GrayToHSV = QAction('GrayToHSV', self)
        GrayToHSV.setStatusTip('灰度转HSV')
        GrayToHSV.triggered.connect(lambda: self.ADD('GrayToHSV'))

        GrayToYUV = QAction('GrayToYUV', self)
        GrayToYUV.setStatusTip('灰度转YUV')
        GrayToYUV.triggered.connect(lambda: self.ADD('GrayToYUV'))

        #######################菜单栏####################################
        Menubar = self.menuBar()  # 添加菜单栏
        File = Menubar.addMenu('文件(&F)')  # 添加菜单
        File.addMenu(newAct)
        File.addActions([saveAct, newStep, openstepfile])
        File.addMenu(stylechange)
        File.addActions([exitAct])

        Filter = Menubar.addMenu('滤波处理')
        Filter.addActions(
            [Blur, MedianBlur, GaussianBlur, BilateralFilter, MaxFilter, MinFilter, HomoFilter, NLM, MatchFilter, GuideFilter, HighPassFilter,
             LowPassFilter, IdealBandFilter, GaussianBandFilter, ButterworthBandFilter, MeanShiftFilter, FloodFill])

        Enhancement = Menubar.addMenu('增强')
        Enhancement.addActions(
            [EqualizeHist, AdaptEqualizeHist, AdaptContrastEnhancement, LogChange, Gamma,
             ConvertScaleAbs, Threshold,
             AdaptiveThreshold, Negate])

        Edge = Menubar.addMenu('边缘检测')
        Edge.addActions([Prewitt, Robert, Sobel, Laplacian, Gabor, Canny, HoughLine, USM])

        Morphology = Menubar.addMenu('形态学操作')
        Morphology.addActions([ERODE, DILATE, OPEN, CLOSE, TOPHAT, BLACKHAT])

        WaveTrans = Menubar.addMenu('小波变换')
        WaveTrans.addActions([dwt_user, dwt_gauss, dwt_erode, dwt_threshold])

        Noise = Menubar.addMenu('噪声')
        Noise.addActions([GaussNoise])

        Else = Menubar.addMenu('其它')
        Else.addActions([Plot_Demo, Display3D, Resize, Partial, Normalize, Subtract, Add, Capture,
                         Maximum, Minimum, GrayToBGR, GrayToHSV, GrayToYUV])

        self.UserDefine = Menubar.addMenu('自定义函数')


        ####################标签、进度条等####################
        self.step_label = QPushButton(QIcon('QT/UI/UI_ICON/file.png'), '', self)
        self.step_label.setIconSize(QSize(22, 22))
        self.step_label.setFixedHeight(25)
        self.step_label.setStyleSheet('border-radius:4px;'
                                      'border-style:solid;border-width:1px;')
        self.step_label.clicked.connect(self.OpenStepProject)
        self.step_label.setFont(QFont('Times New Roman', 12))
        if self.address_step and os.path.exists(self.address_step):
            address = os.path.split(self.address_step)[-1]
            self.step_label.setText(address)
            self.step_label.setToolTip(self.address_step)
        else:
            self.step_label.setText('操作列表')
        # self.pictureList_label = QLabel(self)
        # self.pictureList_label.setText('已执行操作')
        # self.cacheList_label = QLabel(self)
        # self.cacheList_label.setText('缓存图片')
        # self.spend_time_label = QLabel(self)
        # self.spend_time_label.setText('耗时:')
        self.bar = UI_Bar(self)
        self.bar.setFormat(' %v/%m')

        # 操作菜单
        self.List = UI_List(self)
        self.List.item_row_changed.connect(self.Step_Item_Row_Changed)
        self.List.itemEntered.connect(self.List_Enter)
        self.List.setContextMenuPolicy(3)   # 发送customContextMenuRequested信号
        self.List.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)
        self.StepInit()  # 初始化
        self.List.itemClicked.connect(self.STEP_CHOOSE)  # 选中要执行的步骤
        self.List.itemDoubleClicked.connect(self.Modify)

        # 缓存区
        self.CacheList = UI_List(self)
        self.CacheList.item_row_changed.connect(self.Cache_Item_Row_Changed)
        self.CacheList.setContextMenuPolicy(3)
        self.CacheList.customContextMenuRequested[QPoint].connect(self.myCacheWidgetContext)
        self.CacheList.setMouseTracking(True)
        self.CacheList.itemEntered.connect(self.Cache_Enter)
        self.CacheList.itemClicked.connect(self.CACHE_CHOOSE)
        self.CacheList.itemClicked.connect(lambda: self.PictureChoose(1))  # 显示图片

        # 保存过去执行的图片
        self.PictureList = UI_List(self)
        self.PictureList.setContextMenuPolicy(3)
        self.PictureList.setMouseTracking(True)
        self.PictureList.itemEntered.connect(self.Picture_Enter)
        self.PictureList.customContextMenuRequested[QPoint].connect(self.myExecutWidgetContext)
        self.PictureList.itemClicked.connect(lambda: self.PictureChoose(0))  # 单击选中过去实现的图片并显示
        self.PictureList.itemDoubleClicked.connect(self.DoublePictureChoose)  # 双击选中过去实现的图片完成回归操作

        # 删除或添加操作
        # self.line = QLineEdit(self)
        # self.line.setFont(self.font)
        # self.line.setValidator(QIntValidator(0, 65535))
        ####################按钮#######################
        # 显示
        self.start = QPushButton(QIcon("QT/UI/UI_ICON/start.png"), '', self)
        self.start.setIconSize(QSize(25, 25))
        self.start.setFixedSize(25, 25)
        self.start.clicked.connect(self.Multi_Thread_LOOK)
        # 停止
        self.stop = QPushButton(QIcon("QT/UI/UI_ICON/stop.png"), '', self)
        self.stop.setIconSize(QSize(25, 25))
        self.stop.setFixedSize(25, 25)
        self.stop.clicked.connect(self.Stop)
        self.stop.setEnabled(False)
        # 是否保存步骤中的每步效果
        self.showall = QCheckBox(self)
        self.showall.setStyleSheet("QCheckBox::indicator{width:25px; height:25px;}"
                                    "QCheckBox::indicator:unchecked{image: url('QT/UI/UI_ICON/step_close.png');}"
                                    "QCheckBox::indicator:checked{image: url('QT/UI/UI_ICON/step_open.png');}")
        self.showall.setFixedSize(30, 30)
        # 是否将每次操作跳出显示
        self.jumpshow = QCheckBox(self)
        self.jumpshow.setStyleSheet("QCheckBox::indicator{width:25px; height:25px;}"
                                          "QCheckBox::indicator:unchecked{image: url('QT/UI/UI_ICON/jump_close.png');}"
                                          "QCheckBox::indicator:checked{image: url('QT/UI/UI_ICON/jump_open.png');}")
        self.jumpshow.setFixedSize(30, 30)
        # 单通道模式
        self.single_channel = QCheckBox(self)
        self.single_channel.setStyleSheet("QCheckBox::indicator{width:25px; height:25px;}"
                                          "QCheckBox::indicator:unchecked{image: url('QT/UI/UI_ICON/single_close.png');}"
                                          "QCheckBox::indicator:checked{image: url('QT/UI/UI_ICON/single_open.png');}")
        self.single_channel.setFixedSize(30, 30)
        # 设置显示缩放比例
        self.scale_button = QComboBox(self)
        self.scale_button.setEditable(True)
        self.scale_button.setDuplicatesEnabled(False)
        self.scale_button.lineEdit().setAlignment(Qt.AlignCenter)
        self.scale_button.lineEdit().setClearButtonEnabled(False)
        self.scale_button.setMaximumWidth(60)
        rates = [300, 200, 100, 75, 50, 25, 10]
        self.scale_button.addItems(map(lambda x: str(x)+"%", rates))
        self.scale_button.setEditText('100%')
        self.scale_button.lineEdit().editingFinished.connect(self.Scale_Change)
        # # 删除
        # delete = QPushButton('删除', self)
        # delete.setFont(self.font)
        # delete.clicked.connect(self.DELETE)
        # # 删除整行
        # deleteline = QPushButton('删除整行', self)
        # deleteline.setFont(self.font)
        # deleteline.clicked.connect(self.DELETELINE)

        # 新增行
        make = QPushButton(QIcon('QT/UI/UI_ICON/make.png'), '', self)
        make.setIconSize(QSize(25, 25))
        make.setFixedSize(25, 25)
        make.clicked.connect(self.MAKE)
        # 保存
        save = QPushButton(QIcon('QT/UI/UI_ICON/save.png'), '', self)
        save.setIconSize(QSize(25, 25))
        save.setFixedSize(25, 25)
        save.clicked.connect(self.SAVE)

        # 新建算子
        # userDefined = QPushButton('新建算子', self)
        # userDefined.setFont(self.font)
        # userDefined.clicked.connect(self.UserDefined)
        # # 保存算子
        # saveOperator = QPushButton('保存算子', self)
        # saveOperator.setFont(self.font)
        # saveOperator.clicked.connect(self.SaveOperator)
        # # 删除算子
        # deleteOperator = QPushButton('删除算子', self)
        # deleteOperator.setFont(self.font)
        # deleteOperator.clicked.connect(self.DELETEOPERATOR)

        CloseAllPicture = QPushButton(QIcon('QT/UI/UI_ICON/clear_show.png'), '', self)
        CloseAllPicture.setIconSize(QSize(25, 25))
        CloseAllPicture.setFixedSize(25, 25)
        CloseAllPicture.clicked.connect(self.CloseAllPicture)
        CloseAllPicture.setShortcut("ctrl+shift+d")

        screenshot = QPushButton(QIcon('QT/UI/UI_ICON/screenshot.png'), '', self)
        screenshot.setIconSize(QSize(25, 25))
        screenshot.setFixedSize(25, 25)
        screenshot.clicked.connect(self.Screen_Shot)
        screenshot.setShortcut('ctrl+shift+s')

        ########################步骤右键菜单#############################
        self.Menu = QMenu(self)
        step_insert = QAction(u'插入', self)
        step_insert.triggered.connect(self.MAKE)
        step_delete = QAction(u'删除', self)
        step_delete.triggered.connect(self.DELETELINE)
        step_copy = QAction(u'复制(&C)', self)
        step_copy.triggered.connect(self.COPY)
        step_paste = QAction(u'粘贴(&V)', self)
        step_paste.triggered.connect(self.PASTE)
        export = QAction('导出', self)
        export.triggered.connect(self.ExportStep)
        self.Menu.addActions([step_insert, step_delete, step_copy, step_paste, export])

        ########################缓存右键菜单############################
        self.CacheMenu = QMenu(self)
        cache_choose = QAction(u'选为当前图片', self)
        cache_choose.triggered.connect(self.ChooseCachePicture)
        cache_delete = QAction(u'删除', self)
        cache_delete.triggered.connect(self.DELCACHE)
        cache_deleteAll = QAction(u'删除全部', self)
        cache_deleteAll.triggered.connect(self.DELCACHEALL)
        delete_without_choose = QAction(u'删除除选中项外所有项', self)
        delete_without_choose.triggered.connect(self.DELETE_WITHOUT_CHOOSE)
        bgr_to_channels = QAction(u'BGR转三通道', self)
        bgr_to_channels.triggered.connect(self.BGR2GRAY)
        hsv_to_channels = QAction(u'HSV转三通道', self)
        hsv_to_channels.triggered.connect(self.HSV2GRAY)
        yuv_to_channels = QAction(u'YUV转三通道', self)
        yuv_to_channels.triggered.connect(self.YUV2GRAY)


        self.CacheMenu.addActions([cache_choose, bgr_to_channels, hsv_to_channels, yuv_to_channels,
                                   cache_delete, cache_deleteAll, delete_without_choose])
        # self.CacheMenu.actions()[0].setEnabled(False)
        # self.CacheMenu.actions()[0].setVisible(False)

        ##########################已执行操作右键菜单########################
        self.Execut = QMenu(self)

        execut_insert_step = QAction(u'放入步骤', self)
        execut_insert_step.triggered.connect(self.DONETOSTEP)
        execut_insert_cache = QAction(u'放入缓存', self)
        execut_insert_cache.triggered.connect(self.InsertCache)
        execut_return_step = QAction(u'回到当前步骤', self)
        execut_return_step.triggered.connect(self.DoublePictureChoose)

        self.Execut.addActions([execut_insert_step, execut_insert_cache, execut_return_step])


        ##########################界面布局###############################
        top_layout = QVBoxLayout()

        # 步骤列表相关布局
        step_layout = QVBoxLayout()
        step_function_layout = QHBoxLayout()
        step_mangage_layout = QHBoxLayout()
        step_mangage_layout.addWidget(self.step_label)
        step_mangage_layout.addWidget(save)
        step_mangage_layout.addWidget(make)
        step_mangage_layout.setAlignment(Qt.AlignLeft)

        step_run_layout = QHBoxLayout()
        step_run_layout.addWidget(self.start)
        step_run_layout.addWidget(self.stop)
        step_run_layout.addWidget(screenshot)
        step_run_layout.addWidget(CloseAllPicture)
        step_run_layout.addWidget(self.single_channel)
        step_run_layout.addWidget(self.showall)
        step_run_layout.addWidget(self.jumpshow)
        step_run_layout.addWidget(self.scale_button)
        step_run_layout.setAlignment(Qt.AlignRight)

        step_function_layout.addLayout(step_mangage_layout)
        step_function_layout.addLayout(step_run_layout)
        step_layout.addLayout(step_function_layout)
        step_layout.addWidget(self.List)

        # 功能按钮及单选框相关布局
        # delete_layout = QHBoxLayout()
        # delete_layout.addWidget(delete)
        # delete_layout.addWidget(deleteline)
        # textline_save_layout = QHBoxLayout()
        # textline_save_layout.addWidget(self.line)
        # textline_save_layout.addWidget(save)

        # function_layout = QVBoxLayout()
        # function_layout.addLayout(delete_layout)
        # function_layout.addLayout(textline_save_layout)
        # function_layout.addWidget(make)
        # function_layout.addWidget(userDefined)
        # function_layout.addWidget(saveOperator)
        # function_layout.addWidget(deleteOperator)
        # function_layout.addWidget(CloseAllPicture)
        # function_layout_widget = QWidget()
        # function_layout_widget.setLayout(function_layout)
        # function_layout_dock = QDockWidget(self)
        # bar = QToolBar()
        # bar.setStyleSheet('background-color:rgba(0, 225, 225, 12)')
        # function_layout_dock.setTitleBarWidget(bar)
        # function_layout_dock.setFeatures(
        #     QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        # function_layout_dock.setStyleSheet('font-size: 12px;font-family: "宋体";background-color:rgba(255, 255, 255, 230)')
        # function_layout_dock.setFloating(False)
        # function_layout_dock.setWidget(function_layout_widget)

        # 已执行区相关布局
        picture_layout = QVBoxLayout()
        picture_label_layout = QHBoxLayout()
        # picture_label_layout.addWidget(self.pictureList_label)
        picture_label_layout.addWidget(self.bar)
        # picture_label_layout.addWidget(self.spend_time_label)
        picture_label_layout.setAlignment(Qt.AlignBaseline)
        picture_layout.addLayout(picture_label_layout)
        picture_layout.addWidget(self.PictureList)

        # 缓存区相关布局
        cache_layout = QVBoxLayout()
        # cache_layout.addWidget(self.cacheList_label)
        cache_layout.addWidget(self.CacheList)

        # 结合步骤列表相关布局和功能按钮相关布局
        step_function_layout = QHBoxLayout()
        step_function_layout.addLayout(step_layout, stretch=3)
        # step_function_layout.addLayout(function_layout, stretch=1)

        # 结合已执行区和缓存区相关布局
        picture_cache_layout = QSplitter(Qt.Horizontal)
        picutre_layout_widget = QWidget()
        picutre_layout_widget.setLayout(picture_layout)
        cache_layout_widget = QWidget()
        cache_layout_widget.setLayout(cache_layout)
        picture_cache_layout.addWidget(picutre_layout_widget)
        picture_cache_layout.addWidget(cache_layout_widget)
        picture_cache_layout.setSizes([200, 100])
        # picture_cache_layout = QHBoxLayout()
        # picture_cache_layout.addLayout(picture_layout)
        # picture_cache_layout.addLayout(cache_layout)

        # 整体布局
        step_function_layout_widget = QWidget()
        step_function_layout_widget.setLayout(step_function_layout)
        top_layout_widget = QSplitter(Qt.Vertical)
        top_layout_widget.addWidget(step_function_layout_widget)
        top_layout_widget.addWidget(picture_cache_layout)

        top_layout.addWidget(top_layout_widget)

        layout_widget = QWidget()
        layout_widget.setLayout(top_layout)
        self.setCentralWidget(layout_widget)
        # self.addDockWidget(Qt.RightDockWidgetArea, function_layout_dock)




