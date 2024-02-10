from PyQt5.Qt import QMessageBox, QInputDialog, Qt, QToolTip, QCursor, QTimer, QThread, qApp, QRect
from pickle import dump, load
import traceback
import numpy as np
import cv2
import os
from copy import deepcopy


class UI_function:

    ####################系统响应函数#######################

    #################检测根目录是否存在######################
    def Address(self):
        if self.address:
            if os.path.exists(self.address):
                return
            else:
                os.mkdir(self.address)

    ###############关闭事件#######################
    def closeEvent(self, QCloseEvent):
        choose = QMessageBox.warning(self, '提示', '确定要关掉程序吗？', QMessageBox.Yes | QMessageBox.No)
        if choose == QMessageBox.No:
            QCloseEvent.ignore()
            return
        cv2.destroyAllWindows()
        if self.address_step and self.steps:
            with open(self.address_step, 'rb+') as f:
                try:
                    cur = load(f)
                    if cur != self.steps:
                        choose = QMessageBox.information(self, '提示', '你的步骤已被修改，是否保存当前步骤？',
                                                         QMessageBox.Yes | QMessageBox.No)
                        if choose == QMessageBox.Yes:
                            self.SAVE()
                except EOFError:
                    return
        if self.address_operator and self.User:
            with open(self.address_operator, 'rb+') as e:
                try:
                    cur = load(e)
                    if cur != self.User:
                        choose = QMessageBox.information(self, '提示', '你的算子已被修改，是否保存当前算子？',
                                                         QMessageBox.Yes | QMessageBox.No)
                        if choose == QMessageBox.Yes:
                            self.SaveOperator()
                except EOFError:
                    pass
        self.Save_Settings()
        self.Thread.wait()
        self.tooptip_timer.stop()
        self.CloseAllPicture()
        QCloseEvent.accept()

    ################按键检测################
    def keyPressEvent(self, a0):
        if a0.modifiers() == Qt.ControlModifier:
            self.CacheList.blockSignals(True)

    def keyReleaseEvent(self, a0):
        if a0.modifiers() == Qt.NoModifier:
            self.CacheList.blockSignals(False)
            self.CACHE_CHOOSE()

    #################关闭所以图片###################
    def CloseAllPicture(self):
        cv2.destroyAllWindows()

    ###################这些函数是应用执行程序################

    ########################修改风格########################
    def StyleChange(self, t):
        if t == 'Ubuntu':
            with open('QT/UI/UI_CSS/Ubuntu.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'Ubuntu'

        if t == 'MacOS':
            with open('QT/UI/UI_CSS/MacOS.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'MacOS'

        if t == 'AMOLED':
            with open('QT/UI/UI_CSS/AMOLED.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'AMOLED'

        if t == 'ElegantDark':
            with open('QT/UI/UI_CSS/ElegantDark.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'ElegantDark'

        if t == 'ConsoleStyle':
            with open('QT/UI/UI_CSS/ConsoleStyle.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'ConsoleStyle'

        if t == 'ManjaroMix':
            with open('QT/UI/UI_CSS/ManjaroMix.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                self.cur_style = 'ManjaroMix'

    ##################选择图片, 用于ADD等函数################
    def ChoosePicture(self):
        if not self.pictures_imgs:
            QMessageBox.information(self, '提示', '已执行步骤中没有图片')
            return None, None
        name = [i[0] for i in self.cachepictures_info]
        dialog = QInputDialog(self)
        dialog.setWindowModality(Qt.NonModal)
        coef1, ok = dialog.getInt(self, '请输入图片1的系数', '请输入图片1的系数', value=1)
        number1, ok1 = dialog.getItem(self, '选择图片', '请选择图片1', name, current=len(name) - 2)
        if 0 <= int(number1) <= len(name) - 1:
            if not ok1:
                return None, None
            coef2, ok = dialog.getInt(self, '请输入图片2的系数', '请输入图片2的系数', value=1)
            number2, ok2 = dialog.getItem(self, '选择图片', '请选择图片2', name, current=len(name) - 1)
            if 0 <= int(number2) <= len(name) - 1:
                if not ok2:
                    return None, None
                return (number1, coef1), (number2, coef2)

    ##################选择图像, 用于GrayToBGR等API###############
    def Choose_Gray_Picture(self):
        if not self.pictures_imgs:
            QMessageBox.information(self, '提示', '已执行步骤中没有图片')
            return None, None, None
        name = [i[0] for i in self.cachepictures_info]
        dialog = QInputDialog(self)
        dialog.setWindowModality(Qt.NonModal)
        coef1, ok = dialog.getDouble(self, '请输入图片1的系数', '请输入图片1的系数', value=1)
        number1, ok1 = dialog.getItem(self, '选择图片', '请选择图片1', name, current=len(name) - 2)
        if 0 <= int(number1) <= len(name) - 1:
            if not ok1:
                return None, None, None
            coef2, ok = dialog.getDouble(self, '请输入图片2的系数', '请输入图片2的系数', value=1)
            number2, ok2 = dialog.getItem(self, '选择图片', '请选择图片2', name, current=len(name) - 1)
            if 0 <= int(number2) <= len(name) - 1:
                if not ok2:
                    return None, None, None
                coef3, ok = dialog.getDouble(self, '请输入图片3的系数', '请输入图片3的系数', value=1)
                number3, ok3 = dialog.getItem(self, '选择图片', '请选择图片3', name, current=len(name) - 1)
                if 0 <= int(number3) <= len(name) - 1:
                    if not ok3:
                        return None, None, None
                    return (number1, coef1), (number2, coef2), (number3, coef3)

    ###############选择单个图像##################
    def Choose_Single_Picture(self):
        if not self.pictures_imgs:
            QMessageBox.information(self, '提示', '已执行步骤中没有图片')
            return None
        name = [i[0] for i in self.cachepictures_info]
        dialog = QInputDialog(self)
        dialog.setWindowModality(Qt.NonModal)
        number1, ok1 = dialog.getItem(self, '选择图片', '请选择图片1', name, current=len(name) - 2)
        if 0 <= int(number1) <= len(name) - 1:
            if not ok1:
                return None
            return self.cachepictures_imgs[number1][-1]

    ################开启另一个线程执行步骤#############
    def Multi_Thread_LOOK(self):
        if self.Thread.isRunning():
            QMessageBox.information(self, '提示', '已存在正在执行的步骤')
        else:
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.bar.setHidden(False)
            self.Thread.run = self.LOOK
            self.Lock.lock()
            self.Thread.start()

    ######################停止进程###############
    def Stop(self):
        if self.Thread.isRunning() and not self.Thread.stop:
            self.Thread.step_end.emit('end', 1)
            self.Thread.stop = True  # 考虑到直接用terminate可能导致程序崩溃, 故使用信号的形式
            self.Thread.exit(-1)

    ###################执行步骤报错##################
    def Error(self, t, value1, value2):
        if t == 'ChooseError':
            QMessageBox.information(self, '提示', '并未选中任何图片步骤或暂不支持该类型')
        elif t == 'FunctionError':
            QMessageBox.information(self, '提示', '{}不存在'.format(value1))
        elif t == 'ParamError':
            QMessageBox.information(self, '错误', '{} : {}'.format(value1, value2))
        self.Thread.step_end.emit('end', 0)
        self.Thread.exit(-1)
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.Lock.unlock()

    #################执行步骤结束#################
    def End(self):
        self.PictureRefresh()
        self.CacheRefresh()
        self.Thread.exit(0)
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.Lock.unlock()

    ##################显示效果###############
    def LOOK(self):
        import time
        last, cur_time, sum_time = 0, 0, 0
        for number in self.numbers:
            flag = False  # 用于判断函数是否存在
            cur = None  # 暂存当前执行的函数
            # self.spend_time_label.clear()
            if self.now is None or not self.steps or number == [None, None]:  # or type(self.now) is cv2.VideoCapture
                self.Thread.step_error.emit('ChooseError', None, None)
                return
            else:
                if type(self.now) is cv2.VideoCapture:
                    self.now.set(cv2.CAP_PROP_POS_FRAMES, self.now.get(cv2.CAP_PROP_POS_FRAMES) - 1)
                    ok, image = self.now.read()
                    self.pictures_info.append(
                        ['{}'.format(len(self.pictures_info)), [None, 0], 0])
                    self.pictures_imgs.append([image.copy(), ])

                else:
                    image = self.now.copy()

                self.pictures_info.append(
                    ['{}'.format(len(self.pictures_info)), ])
                self.pictures_imgs.append([])

                try:  # 用于测试参数是否正确
                    # 判断是根目录还是子目录
                    if number[1] is None:
                        steps = self.steps[number[0]][1:]
                    else:
                        steps = [self.steps[number[0]][number[1] + 1]]

                    channel = 1 if len(image.shape) == 2 else image.shape[2]

                    self.Thread.step_range.emit('range', len(steps))
                    for i in range(len(steps)):
                        step = steps[i]
                        # 当产生终止信号
                        if self.Thread.stop is True:
                            self.now = self.pictures_imgs[-1][-1]
                            self.Thread.stop = False
                            self.Lock.unlock()
                            self.Thread.step_end.emit('end', 0)
                            flag = 1
                            break
                        self.Thread.step_value.emit('value', i)
                        ####### 处理参数 #########
                        if isinstance(step[1], str):
                            param = eval(step[1])
                            param = param if isinstance(param, tuple) else (param,)
                        else:
                            param = np.array(step[1])
                        if step[0][0:2] == '算子':
                            cur = '算子'
                            s = self.SUM.get('算子', 0)
                        else:
                            cur = step[0]
                            s = self.SUM.get(step[0], 0)
                            s = self.User_SUM.get(step[0], 0) if s == 0 else s
                        if s == 0:
                            self.Thread.step_error.emit('FunctionError', step[0], None)
                            flag = True
                            break
                        else:
                            start = time.monotonic()
                            if not self.single_channel.isChecked() or channel == 1 or step[0] == 'Resize':
                                image = s(image, param)
                            else:
                                tmp = cv2.split(image)
                                image = cv2.merge([s(cl, param) for cl in tmp])
                            end = time.monotonic()
                            sum_time += end - start
                            self.pictures_info[-1].append([step, end-start])
                            self.pictures_imgs[-1].append(image.copy())
                    self.pictures_info[-1].append(sum_time)
                except Exception as error:
                    if self.debug:
                        raise error
                    self.Thread.step_error.emit('ParamError', cur, str(error))
                    flag = True

                # 发生错误, 回退
                if flag:
                    self.now = self.pictures_imgs[-2][-1]
                    del self.pictures_info[-1]
                    del self.pictures_imgs[-1]
                    return
                else:
                    if len(self.numbers) == 1:
                        self.now = image.copy()

                self.cachepictures_info.append(['{}'.format(len(self.cachepictures_info)), *self.pictures_info[-1][1:].copy()])
                self.cachepictures_imgs.append(deepcopy(self.pictures_imgs[-1]))

                if len(self.numbers) != 1:
                    del self.pictures_info[-1]
                    del self.pictures_imgs[-1]

                if self.jumpshow.isChecked():
                    self.Thread.JumpShow.emit(number[0])

                # 如果这里不用信号发出结束信号而是直接调用函数，会和提示框发送冲突
                # 发生冲突的地方在self.start.setEnabled(True)和self.stop.setEnabled(False)
                # 猜测是因为self.start和self.stop都在主线程 子线程不可以直接干预主线程
                self.Thread.step_end.emit('end', 0)

        self.Thread.progress_end.emit()
        # self.spend_time_label.setText("耗时:{:5f}".format(sum_time))


    ################勾选弹出结果####################
    def JumpShow(self, num):
        name = 'result{}'.format(num)
        cv2.namedWindow(name)
        x, y = cv2.getWindowImageRect(name)[0:2]
        if x < 0 or y < 0:
            cv2.moveWindow(name, x if x > 0 else 0, y if y > 0 else 0)
        self.Show_Picture(name, self.now)

    #################显示伸缩因子控制响应################
    def Scale_Change(self):
        value = self.scale_button.lineEdit().text()
        if value[-1] == '%':
            value = value[:-1]
        if value.isdigit():
            self.scale = eval(value) / 100
        self.scale_button.setEditText('{}%'.format(int(self.scale * 100)))

    ####################显示图片#######################
    def Show_Picture(self, name, img, t=0):
        if img is None:
            return
        out = None
        if type(img) is cv2.VideoCapture:
            cout, cur_pos = img.get(cv2.CAP_PROP_FRAME_COUNT), img.get(cv2.CAP_PROP_POS_FRAMES)
            cur_pos += cout // 20
            cur_pos = 0 if cur_pos > cout else cur_pos
            img.set(cv2.CAP_PROP_POS_FRAMES, cur_pos)
            ok, image = img.read()
            if ok:
                out = cv2.resize(image, None, None, fx=self.scale, fy=self.scale)
            else:
                return
        else:
            out = cv2.resize(img, None, None, fx=self.scale, fy=self.scale)

        if cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) > 0:
            if self.jumpshow.isChecked():
                cv2.destroyWindow(name)

        cv2.imshow(name, out)
        if cv2.waitKey(t) & 0xff == 27:
            cv2.destroyWindow(name)
            self.video_close = True

    ####################鼠标划过步骤列表事件##############
    def List_Enter(self, item, p):
        def ToolTip():
            pos = QCursor.pos()
            local_pos = self.List.viewport().mapFromGlobal(pos)  # 从全局指向变为self.List的内部坐标
            if self.List.itemAt(
                    local_pos) == item and 0 < local_pos.x() < self.List.width() and 0 < local_pos.y() < self.List.height():
                text = ''
                if item.parent():
                    text += item.text(0)
                else:
                    length = item.childCount()
                    for i in range(length):
                        if i < length - 1:
                            text += str(i) + ' ' + item.child(i).text(0) + '\n'
                        else:
                            text += str(i) + ' ' + item.child(i).text(0)
                QToolTip.showText(pos, text)

        self.tooptip_timer.timeout.connect(ToolTip)
        self.tooptip_timer.start()

    ######################鼠标划过缓存区事件################

    def Cache_Enter(self, item):
        def ToolTip():
            pos = QCursor.pos()
            local_pos = self.CacheList.viewport().mapFromGlobal(pos)  # 从全局指向变为self.List的内部坐标
            if self.CacheList.itemAt(
                    local_pos) == item and 0 < local_pos.x() < self.CacheList.width() and 0 < local_pos.y() < self.CacheList.height():
                number = self.CacheList.indexFromItem(item).row()
                if item.parent():
                    parent_row = self.CacheList.indexOfTopLevelItem(item.parent())
                    picture = self.cachepictures_imgs[parent_row][number]
                    use_time = self.cachepictures_info[parent_row][number+1][-1]
                else:
                    picture = self.cachepictures_imgs[number][-1]
                    use_time = self.cachepictures_info[number][-1]
                if type(picture) is not cv2.VideoCapture and len(picture.shape) < 3:
                    width, height = picture.shape
                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'time: {:.6f}'.format(width, height, 1, use_time))
                elif type(picture) is not cv2.VideoCapture and len(picture.shape) == 3:
                    width, height, channel = picture.shape
                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'time: {:.6f}'.format(width, height, channel, use_time))
                else:
                    width, height, count, fps, brightness, contrast, saturation, hue, exposure = \
                        int(picture.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                        int(picture.get(cv2.CAP_PROP_FRAME_HEIGHT)), \
                        picture.get(cv2.CAP_PROP_FRAME_COUNT), \
                        picture.get(cv2.CAP_PROP_FPS), \
                        picture.get(cv2.CAP_PROP_BRIGHTNESS), \
                        picture.get(cv2.CAP_PROP_CONTRAST), \
                        picture.get(cv2.CAP_PROP_SATURATION), \
                        picture.get(cv2.CAP_PROP_HUE), \
                        picture.get(cv2.CAP_PROP_EXPOSURE)

                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'count: {}\n'
                                           'fps: {}\n'
                                           'brightness: {}\n'
                                           'contrast: {}\n'
                                           'saturation: {}\n'
                                           'hue: {}\n'
                                           'exposure: {}'.format(width, height, 3, count, fps, brightness, contrast,
                                                                 saturation, hue, exposure))

        self.tooptip_timer.timeout.connect(ToolTip)
        self.tooptip_timer.start()

    #######################鼠标划过已执行区事件#################

    def Picture_Enter(self, item):
        def ToolTip():
            pos = QCursor.pos()
            local_pos = self.PictureList.viewport().mapFromGlobal(pos)  # 从全局指向变为self.List的内部坐标
            if self.PictureList.itemAt(
                    local_pos) == item and 0 < local_pos.x() < self.PictureList.width() and 0 < local_pos.y() < self.PictureList.height():
                number = self.PictureList.indexFromItem(item).row()
                if item.parent():
                    parent_row = self.PictureList.indexOfTopLevelItem(item.parent())
                    picture = self.pictures_imgs[parent_row][number]
                    use_time = self.pictures_info[parent_row][number+1][-1]
                else:
                    picture = self.pictures_imgs[number][-1]
                    use_time = self.pictures_info[number][-1]
                if type(picture) is not cv2.VideoCapture and len(picture.shape) < 3:
                    height, width = picture.shape
                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'time: {:.6f}'.format(width, height, 1, use_time))
                elif type(picture) is not cv2.VideoCapture and len(picture.shape) == 3:
                    height, width, channel = picture.shape
                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'time: {:.6f}'.format(width, height, channel, use_time))
                else:
                    width, height, count, fps, brightness, contrast, saturation, hue, exposure =  \
                                                     int(picture.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                                                     int(picture.get(cv2.CAP_PROP_FRAME_HEIGHT)), \
                                                     picture.get(cv2.CAP_PROP_FRAME_COUNT), \
                                                     picture.get(cv2.CAP_PROP_FPS), \
                                                     picture.get(cv2.CAP_PROP_BRIGHTNESS), \
                                                     picture.get(cv2.CAP_PROP_CONTRAST), \
                                                     picture.get(cv2.CAP_PROP_SATURATION), \
                                                     picture.get(cv2.CAP_PROP_HUE), \
                                                     picture.get(cv2.CAP_PROP_EXPOSURE)

                    QToolTip.showText(pos, 'shape: ({},{})\n'
                                           'channel: {}\n'
                                           'count: {}\n'
                                           'fps: {}\n'
                                           'brightness: {}\n'
                                           'contrast: {}\n'
                                           'saturation: {}\n'
                                           'hue: {}\n'
                                           'exposure: {}'.format(width, height, 3, count, fps, brightness, contrast, saturation, hue, exposure))
        self.tooptip_timer.timeout.connect(ToolTip)
        self.tooptip_timer.start()
