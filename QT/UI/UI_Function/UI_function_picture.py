from PyQt5.Qt import Qt, QMessageBox, QListWidgetItem, QFileDialog, QCursor, QTreeWidgetItem
from UI_Function.UI_ADD import UI_ADD
import cv2
import os
import copy
import numpy as np


class UI_function_picture(UI_ADD):

    ###############缓存区右键菜单##############
    def myCacheWidgetContext(self, point):
        self.CACHE_CHOOSE()
        if not self.cache_numbers:
            return
        number = copy.deepcopy(self.cache_numbers[0])
        number[1] = -1 if number[1] is None else number[1]
        if self.CacheList.currentItem():
            if (type(self.cachepictures_imgs[number[0]][number[1]]) is not cv2.VideoCapture and \
                    len(self.cachepictures_imgs[number[0]][number[1]].shape) > 2):
                self.CacheMenu.actions()[1].setVisible(True)
                self.CacheMenu.actions()[2].setVisible(True)
                self.CacheMenu.actions()[3].setVisible(True)
            elif (type(self.cachepictures_imgs[number[0]][number[1]]) is not cv2.VideoCapture and \
                    len(self.cachepictures_imgs[number[0]][number[1]].shape) == 2):
                self.CacheMenu.actions()[1].setVisible(False)
                self.CacheMenu.actions()[2].setVisible(False)
                self.CacheMenu.actions()[3].setVisible(False)
            elif type(self.cachepictures_imgs[number[0]][number[1]]) is cv2.VideoCapture:
                self.CacheMenu.actions()[1].setVisible(False)
                self.CacheMenu.actions()[2].setVisible(False)
                self.CacheMenu.actions()[3].setVisible(False)
            self.CacheMenu.exec_(QCursor.pos())

    ###############已执行区右键菜单#############
    def myExecutWidgetContext(self, point):
        self.PICTURES_CHOOSE()
        if self.PictureList.currentItem():
            self.Execut.exec_(QCursor.pos())

    ############将缓冲区被选中图像放到已执行区#############
    def ChooseCachePicture(self):
        number = copy.deepcopy(self.cache_numbers[0])
        number[1] = -1 if number[1] is None else number[1]
        if self.cachepictures_imgs:
            self.now = self.cachepictures_imgs[number[0]][number[1]] \
                if type(self.cachepictures_imgs[number[0]][number[1]]) is cv2.VideoCapture \
                else self.cachepictures_imgs[number[0]][number[1]].copy()

            self.pictures_info = [["0", ["新建", 0], 0],]
            self.pictures_imgs = [[self.cachepictures_imgs[number[0]][number[1]] \
                if type(self.cachepictures_imgs[number[0]][number[1]]) is cv2.VideoCapture \
                else self.cachepictures_imgs[number[0]][number[1]].copy(),],]

            self.PictureRefresh()

    ############将多通道图片拆解为BGR三通道###############
    def BGR2GRAY(self):
        if self.CacheList.currentItem():
            for number in self.cache_numbers:
                color = ['b', 'g', 'r']
                if number[1] is None:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][-1]
                else:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][number[1]]
                b, g, r = cv2.split(image)
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), ['{} \'s Channel {}'.format(num, color[0]), 0],
                     ['{} \'s Channel {}'.format(num, color[1]), 0], ['{} \'s Channel {}'.format(num, color[2]), 0], 0]
                )
                self.cachepictures_imgs.append([eval(color[0]), eval(color[1]), eval(color[2])])

            self.CacheRefresh()

    ############将多通道图片拆解为HSV三通道###############
    def HSV2GRAY(self):
        if self.CacheList.currentItem():
            for number in self.cache_numbers:
                color = ['h', 's', 'v']
                if number[1] is None:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][-1]
                else:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][number[1]]
                h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL))  # h (0, 255) s (0, 255) v(0, 255)
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), ['{} \'s Channel {}'.format(num, color[0]), 0],
                     ['{} \'s Channel {}'.format(num, color[1]), 0], ['{} \'s Channel {}'.format(num, color[2]), 0], 0]
                )
                self.cachepictures_imgs.append([eval(color[0]), eval(color[1]), eval(color[2])])
            self.CacheRefresh()

    ############将多通道图片拆解为YUV三通道###############
    def YUV2GRAY(self):
        if self.CacheList.currentItem():
            for number in self.cache_numbers:
                color = ['y', 'u', 'v']
                if number[1] is None:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][-1]
                else:
                    num, image = self.cachepictures_info[number[0]][0], self.cachepictures_imgs[number[0]][number[1]]
                y, u, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2YUV))   # y (16, 255) u (0, 255) v(0, 255)
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), ['{} \'s Channel {}'.format(num, color[0]), 0],
                     ['{} \'s Channel {}'.format(num, color[1]), 0], ['{} \'s Channel {}'.format(num, color[2]), 0], 0]
                )
                self.cachepictures_imgs.append([eval(color[0]), eval(color[1]), eval(color[2])])
            self.CacheRefresh()

    ##############删除缓冲区里除选中项外所有项##############
    def DELETE_WITHOUT_CHOOSE(self):
        if self.CacheList.currentItem():
            tmp_info = []
            tmp_imgs = []
            for number in self.cache_numbers:
                if number[1] is not None:
                    tmp_info.append(['{}'.format(len(tmp_info)),
                                                    self.cachepictures_info[number[0]][number[1] + 1],
                                                    self.cachepictures_info[number[0]][number[1] + 1][-1]])
                    tmp_imgs.append([self.cachepictures_imgs[number[0]][number[1]],])
                else:
                    tmp_info.append(['{}'.format(len(tmp_info)),
                                                    *self.cachepictures_info[number[0]][1:]])
                    tmp_imgs.append(self.cachepictures_imgs[number[0]])
            self.cachepictures_info = copy.deepcopy(tmp_info)
            self.cachepictures_imgs = copy.deepcopy(tmp_imgs)
            self.CacheRefresh()

    ##############删除缓冲区单个图片#################
    def DELCACHE(self):
        self.cache_numbers = sorted(self.cache_numbers, key=lambda x: (x[0], x[1]))
        if self.cachepictures_imgs:
            for i, number in enumerate(self.cache_numbers):
                if number[1] is None:
                    del self.cachepictures_info[number[0]]
                    del self.cachepictures_imgs[number[0]]
                    for picture in self.cachepictures_info[number[0]:]:
                        picture[0] = str(int(picture[0]) - 1)
                    for j in range(i + 1, len(self.cache_numbers)):
                        self.cache_numbers[j][0] -= 1
                else:
                    del self.cachepictures_info[number[0]][number[1]+1]
                    del self.cachepictures_imgs[number[0]][number[1]]
                    for j in range(i + 1, len(self.cache_numbers)):
                        if self.cache_numbers[j][0] == self.cache_numbers[i][0]:
                            self.cache_numbers[j][1] -= 1
                        else:
                            break

            self.CacheRefresh()

    ###############将缓存区全部清除###################
    def DELCACHEALL(self):
        del self.cachepictures_info
        del self.cachepictures_imgs
        self.cachepictures_info = []
        self.cachepictures_imgs = []
        self.time = []
        self.CacheRefresh()

    ###################将已执行步骤放入缓存###################
    def InsertCache(self):
        if self.pictures_imgs:
            for number in self.pictures_numbers:
                if number[1] is None:
                    self.cachepictures_info += [[str(len(self.cachepictures_info)),
                                                 *self.pictures_info[number[0]][1:]]]
                    self.cachepictures_imgs += [copy.deepcopy(self.pictures_imgs[number[0]]),]
                else:
                    self.cachepictures_info += [[str(len(self.cachepictures_info)),
                                                self.pictures_info[number[0]][number[1]+1],
                                                self.pictures_info[number[0]][number[1]+1][-1]]]
                    self.cachepictures_imgs += [[self.pictures_imgs[number[0]][number[1]],]]
            self.CacheRefresh()

    ###################获取列表中选中的行#####################
    def CACHE_CHOOSE(self):
        self.cache_numbers = []
        for index in self.CacheList.selectedIndexes():
            if index.parent().isValid():
                self.cache_numbers.append([index.parent().row(), index.row()])
            else:
                self.cache_numbers.append([index.row(), None])

    def PICTURES_CHOOSE(self):
        self.pictures_numbers = []
        for index in self.PictureList.selectedIndexes():
            if index.parent().isValid():
                self.pictures_numbers.append([index.parent().row(), index.row()])
            else:
                self.pictures_numbers.append([index.row(), None])

    #################显示选中的已执行区和缓存区图片##################
    def PictureChoose(self, type):
        if type == 0:
            self.PICTURES_CHOOSE()
            cv2.namedWindow("ChoosePicture")
            # x, y = cv2.getWindowImageRect("ChoosePicture")[0:2]
            # if x < 0 or y < 0:
            #     cv2.moveWindow("ChoosePicture", x if x > 0 else 0, y if y > 0 else 0)
            for number in self.pictures_numbers:
                if number[1] is None:
                    self.Show_Picture('ChoosePicture',
                                      self.pictures_imgs[number[0]][-1])
                else:
                    self.Show_Picture('ChoosePicture',
                                      self.pictures_imgs[number[0]][number[1]])
        else:
            self.CACHE_CHOOSE()
            cv2.namedWindow("ChooseCachePicture")
            # x, y = cv2.getWindowImageRect("ChooseCachePicture")[0:2]
            # if x < 0 or y < 0:
            #     cv2.moveWindow("ChooseCachePicture", x if x > 0 else 0, y if y > 0 else 0)
            for number in self.cache_numbers:
                if number[1] is None:
                    self.Show_Picture('ChooseCachePicture',
                                      self.cachepictures_imgs[number[0]][-1])
                else:
                    self.Show_Picture('ChooseCachePicture',
                                      self.cachepictures_imgs[number[0]][number[1]])

    ##############双击图片列表, 删除选中项以下的图片#############
    def DoublePictureChoose(self):
        if self.pictures_imgs:
            for number in self.pictures_numbers:
                self.now = self.pictures_imgs[number[0]][-1] \
                    if type(self.pictures_imgs[number[0]][-1]) is cv2.VideoCapture\
                    else self.pictures_imgs[number[0]][-1].copy()
                del self.pictures_info[number[0] + 1:]
                del self.pictures_imgs[number[0] + 1:]
                self.PictureRefresh()

    ###############打开原图片#####################
    def OpenOriginal(self):
        if not self.pictures_imgs:
            return
        cv2.namedWindow("Original")
        x, y = cv2.getWindowImageRect("Original")[0:2]
        if x < 0 or y < 0:
            cv2.moveWindow("Original", x if x > 0 else 0, y if y > 0 else 0)
        self.Show_Picture('Original', self.pictures_imgs[0][-1])

    ###############打开当前图片###############
    def OpenNow(self):
        if self.now is None:
            return
        cv2.namedWindow("Now")
        x, y = cv2.getWindowImageRect("Now")[0:2]
        if x < 0 or y < 0:
            cv2.moveWindow("Now", x if x > 0 else 0, y if y > 0 else 0)
        self.Show_Picture('Now', self.now)

    ##############回到原图片#####################
    def Last(self):
        if not self.pictures_imgs:
            return
        self.now = self.pictures_imgs[0][-1].copy()
        del self.pictures_imgs[1:]
        del self.pictures_info[1:]
        self.PictureRefresh()

    ##################保存图片#####################
    def SaveImage(self):
        if self.now is None:
            QMessageBox.information(self, '提示', '当前没有任何图片')
            return
        address, ok = QFileDialog.getSaveFileName(self, '保存文件', self.address,
                                                  ";;Images (*.png *.xpm *.jpg)", )
        _, t = os.path.splitext(address)

        if address:
            cv2.imencode(t, self.now)[1].tofile(address)
            # cv2.imwrite(address, self.now)

    #####################新建#######################
    def New(self, t):
        fnames, name = QFileDialog.getOpenFileNames(self, '打开文件', self.cur_image_address,
                                               "*")  # 空白等于（*）就是全部文件
        if not fnames:
            return
        for num in range(len(fnames)):
            file = None
            file_type = os.path.splitext(fnames[num])[-1][1:].lower()
            try:
                if t == 0 and file_type in ('png', 'bmp', 'jpg', 'jpeg', 'gif'):
                    file = cv2.cvtColor(cv2.imdecode(np.fromfile(fnames[num], dtype=np.uint8), cv2.COLOR_RGB2GRAY),
                                       cv2.COLOR_BGR2GRAY)
                    # img = cv2.imread(fnames[num], 0)

                elif t == 1 and file_type in ('png', 'bmp', 'jpg', 'jpeg', 'gif'):
                    file = cv2.imdecode(np.fromfile(fnames[num], dtype=np.uint8), cv2.COLOR_RGB2BGR)
                    # img = cv2.imread(fnames[num])

                elif t == 2 and file_type in ('mp4', 'avi', 'flv', 'mpg', 'mpeg', 'wmv'):
                    file = cv2.VideoCapture(fnames[num])

            except Exception as e:
                QMessageBox.warning(self, 'Error', str(e))
                continue

            else:
                if file is None:
                    QMessageBox.warning(self, 'Error', "输入文件格式不符")
                    continue

            if len(self.pictures_imgs) == 0:
                self.PictureList.clear()
                self.pictures_info.clear()
                self.pictures_imgs.clear()
                self.pictures_info.append(['0', ['新建{}'.format(num), 0], 0])
                self.pictures_imgs.append([copy.deepcopy(file) if t != 2 else file,])
                self.now = copy.deepcopy(file) if t != 2 else file  # file.copy()
            self.cachepictures_info.append(['{}'.format(len(self.cachepictures_info)), [os.path.basename(fnames[num]), 0], 0])
            self.cachepictures_imgs.append([copy.deepcopy(file) if t != 2 else file,])
        self.cur_image_address = os.path.join(fnames[0], os.pardir)
        self.PictureRefresh()
        self.CacheRefresh()
        if self.jumpshow.isChecked():
            cv2.namedWindow("Original")
            x, y = cv2.getWindowImageRect("Original")[0:2]
            if x < 0 or y < 0:
                cv2.moveWindow("Original", x if x > 0 else 0, y if y > 0 else 0)
            self.Show_Picture('Original', self.pictures_imgs[0][-1])

    ###################已执行步骤刷新#########################
    def PictureRefresh(self):
        self.PictureList.clear()
        if self.pictures_info:
            for x, picture in enumerate(self.pictures_info):
                item = QTreeWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
                item_text = picture[0]
                for i in range(len(picture[1:-1])):
                    group = QTreeWidgetItem()
                    if type(picture[i + 1][0]) is type(()):  # 如何包含参数
                        if picture[i + 1][0][0][0:2] == '算子':
                            group.setText(0, picture[i + 1][0][0])
                            item_text += ' {}'.format(picture[i + 1][0][0])
                        else:
                            group.setText(0, '{}[{}]'.format(picture[i + 1][0][0], picture[i + 1][0][1]))
                            item_text += ' {}[{}]'.format(picture[i + 1][0][0], picture[i + 1][0][1])

                    else:  # 无参数
                        group.setText(0, '{}'.format(picture[i + 1][0]))
                        item_text += ' {}'.format(picture[i + 1][0])
                    item.addChild(group)
                item.setText(0, item_text)
                self.PictureList.addTopLevelItem(item)

    ####################缓存区刷新#########################
    def CacheRefresh(self):
        self.CacheList.clear()
        if self.cachepictures_info:
            for x, picture in enumerate(self.cachepictures_info):
                item = QTreeWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
                item_text = picture[0]
                for i in range(len(picture[1:-1])):
                    group = QTreeWidgetItem()
                    if type(picture[i+1][0]) is type(()):  # 如何包含参数
                        if picture[i + 1][0][0][0:2] == '算子':
                            group.setText(0, picture[i + 1][0][0])
                            item_text += ' {}'.format(picture[i + 1][0][0])
                        else:
                            group.setText(0, '{}[{}]'.format(picture[i + 1][0][0], picture[i + 1][0][1]))
                            item_text += ' {}[{}]'.format(picture[i + 1][0][0], picture[i + 1][0][1])

                    else:  # 无参数
                        group.setText(0, '{}'.format(picture[i + 1][0]))
                        item_text += ' {}'.format(picture[i + 1][0])
                    item.addChild(group)
                item.setText(0, item_text)
                self.CacheList.addTopLevelItem(item)

    ###############
    def Cache_Item_Row_Changed(self, start, end):
        pass