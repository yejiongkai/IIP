from module.Else import *
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from UI_widget import UI_widget
import cv2


class UI_ADD(UI_widget):
    def ADD(self, name):
        if name in ['Plot_Demo', 'Display3D', 'LUT', 'Add', 'GrayToBGR', 'GrayToHSV', 'GrayToYUV',
                    'Maximum', 'Minimum', 'Subtract', 'Partial']:
            self.ADD_one(name, None)
        else:
            for number in self.numbers:
                self.ADD_one(name, number)
        
    # 当添加动作时刷新列表
    def ADD_one(self, name, number):
        import time
        ######################Else######################
        # 直方图显示不需要指定步骤
        if name == 'Plot_Demo':
            if self.now is None:
                QMessageBox.information(self, '提示', '未选中任何图片')
            else:
                if len(self.now.shape) > 2:
                    image_hist_demo(self.now)
                else:
                    Plot_Demo(self.now)
            return
        if name == 'Display3D':
            if self.now is None:
                QMessageBox.information(self, '提示', '未选中任何图片')
            # elif len(self.now.shape) > 2:
            #     QMessageBox.information(self, '提示', '当前不支持多通道的3D显示')
            else:
                parameter, bool = QInputDialog.getText(self, '设置(x, y, step)',
                                                       '请输入(x(x轴范围), y(y轴范围), step(采点距离)',
                                                       text='((-1,-1),(-1,-1),1)')
                if bool:
                    Display3D(self.now, eval(parameter))
            return

        if name == 'LUT':
            if self.now is None:
                QMessageBox.information(self, '提示', '未选中任何图片')
            else:
                parameter, bool = QInputDialog.getMultiLineText(self, '设置((色素区间),(R),(G),(B))',
                                                                '请输入((色素区间),(R),(G),(B))',
                                                                text='((0,30,50,60,100,180,256),\n'
                                                                     '  (0,40,100,148,200,235,256),\n'
                                                                     '  (0,30,30,30,100,228,256),\n'
                                                                     '  (0,5,5,5,56,139,256))')
                if bool:
                    last = time.time()
                    dst = LUT(self.now, eval(parameter))
                    self.cachepictures_info.append(
                        ['{}'.format(len(self.cachepictures_info)), parameter, time.time() - last])
                    self.cachepictures_imgs.append([dst,])
                    self.CacheRefresh()
                    cv2.namedWindow("color")
                    x, y = cv2.getWindowImageRect("color")[0:2]
                    if x < 0 or y < 0:
                        cv2.moveWindow("color", x if x > 0 else 0, y if y > 0 else 0)
                    self.Show_Picture('color', dst)
            return

        if name == 'Add':
            if len(self.cache_numbers) == 2:
                image1, image2 = self.cachepictures_imgs[self.cache_numbers[0][0]][
                    -1 if self.cache_numbers[0][1] is None else self.cache_numbers[0][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[1][0]][
                        -1 if self.cache_numbers[1][1] is None else self.cache_numbers[1][1]].copy()
            else:
                QMessageBox.warning(self, "警告", "选中图像个数不为2!")
                image1, image2 = None, None
            if image1 is not None and image2 is not None:
                mode, choose = QInputDialog.getInt(self, '请选择模式', '0:按比例相加 1:乘上系数相加', value=0, min=0, max=1)
                coef1, choose1 = QInputDialog.getDouble(self, '请选择图像1的权重', '', value=0.5, min=0, max=1)
                coef2, choose2 = QInputDialog.getDouble(self, '请选择图像2的权重', '', value=0.5, min=0, max=1)
                if not choose and not choose1 and not choose2:
                    return
                if image1.shape != image2.shape:
                    QMessageBox.information(self, '提示', '两张图片的尺度不同')
                    return
                start = time.monotonic()
                dst = Add(image1, image2, coef1, coef2, mode)
                use_time = time.monotonic() - start
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), [('Add', '({},{},{})'.format(coef1, coef2, mode)), use_time], use_time])
                self.cachepictures_imgs.append([dst, ])
                self.CacheRefresh()
                cv2.namedWindow("Add")
                x, y = cv2.getWindowImageRect("Add")[0:2]
                if x < 0 or y < 0:
                    cv2.moveWindow("Add", x if x > 0 else 0, y if y > 0 else 0)
                self.Show_Picture('Add', dst)
            return

        if name == 'GrayToBGR' or name == 'GrayToHSV' or name == 'GrayToYUV':
            if len(self.cache_numbers) == 3:
                image1, image2, image3 = self.cachepictures_imgs[self.cache_numbers[0][0]][
                    -1 if self.cache_numbers[0][1] is None else self.cache_numbers[0][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[1][0]][
                        -1 if self.cache_numbers[1][1] is None else self.cache_numbers[1][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[2][0]][
                        -1 if self.cache_numbers[2][1] is None else self.cache_numbers[2][1]].copy()
            else:
                QMessageBox.warning(self, "警告", "选中图像个数不为3!")
                image1, image2, image3 = None, None, None
            if image1 is not None and image2 is not None and image3 is not None:
                start = time.monotonic()
                dst = eval(name)(image1, image2, image3, 1, 1, 1)
                use_time = time.monotonic() - start
                if dst is False:
                    QMessageBox.information(self, '提示', '图片格式不符')
                    return
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), [name, use_time], use_time])
                self.cachepictures_imgs.append([dst, ])
                self.CacheRefresh()
                cv2.namedWindow(name)
                x, y = cv2.getWindowImageRect(name)[0:2]
                if x < 0 or y < 0:
                    cv2.moveWindow(name, x if x > 0 else 0, y if y > 0 else 0)
                self.Show_Picture(name, dst)
            return

        if name == 'Maximum':
            if len(self.cache_numbers) == 2:
                image1, image2 = self.cachepictures_imgs[self.cache_numbers[0][0]][
                    -1 if self.cache_numbers[0][1] is None else self.cache_numbers[0][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[1][0]][
                        -1 if self.cache_numbers[1][1] is None else self.cache_numbers[1][1]].copy()
            else:
                QMessageBox.warning(self, "警告", "选中图像个数不为2!")
                image1, image2 = None, None
            if image1 is not None and image2 is not None:
                if image1.shape != image2.shape:
                    QMessageBox.information(self, '提示', '两张图片的尺度不同')
                    return
                start = time.monotonic()
                dst = Maximum(image1, image2)
                use_time = time.monotonic() - start
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), ['Maximum', use_time], use_time])
                self.cachepictures_imgs.append([dst, ])
                self.CacheRefresh()
                cv2.namedWindow("Maximum")
                x, y = cv2.getWindowImageRect("Maximum")[0:2]
                if x < 0 or y < 0:
                    cv2.moveWindow("Maximum", x if x > 0 else 0, y if y > 0 else 0)
                self.Show_Picture('Maximum', dst)
            return

        if name == 'Minimum':
            if len(self.cache_numbers) == 2:
                image1, image2 = self.cachepictures_imgs[self.cache_numbers[0][0]][
                    -1 if self.cache_numbers[0][1] is None else self.cache_numbers[0][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[1][0]][
                        -1 if self.cache_numbers[1][1] is None else self.cache_numbers[1][1]].copy()
            else:
                QMessageBox.warning(self, "警告", "选中图像个数不为2!")
                image1, image2 = None, None
            if image1 is not None and image2 is not None:
                if image1.shape != image2.shape:
                    QMessageBox.information(self, '提示', '两张图片的尺度不同')
                    return
                start = time.monotonic()
                dst = Minimum(image1, image2)
                use_time = time.monotonic() - start
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)), ['Minimum', use_time], use_time])
                self.cachepictures_imgs.append([dst, ])
                self.CacheRefresh()
                cv2.namedWindow("Minimum")
                x, y = cv2.getWindowImageRect("Minimum")[0:2]
                if x < 0 or y < 0:
                    cv2.moveWindow("Minimum", x if x > 0 else 0, y if y > 0 else 0)
                self.Show_Picture('Minimum', dst)
            return

        if name == 'Subtract':
            if len(self.cache_numbers) == 2:
                image1, image2 = self.cachepictures_imgs[self.cache_numbers[0][0]][
                    -1 if self.cache_numbers[0][1] is None else self.cache_numbers[0][1]].copy(), \
                    self.cachepictures_imgs[self.cache_numbers[1][0]][
                        -1 if self.cache_numbers[1][1] is None else self.cache_numbers[1][1]].copy()
            else:
                QMessageBox.warning(self, "警告", "选中图像个数不为2!")
                image1, image2 = None, None
            if image1 is not None and image2 is not None:
                coef1, choose1 = QInputDialog.getDouble(self, '请选择图像1的权重', '', value=0.5, min=0, max=1)
                coef2, choose2 = QInputDialog.getDouble(self, '请选择图像2的权重', '', value=0.5, min=0, max=1)
                if not choose1 and not choose2:
                    return
                if image1.shape != image2.shape:
                    QMessageBox.information(self, '提示', '两张图片的尺度不同')
                    return
                start = time.monotonic()
                dst = Subtract(image1, image2, coef1, coef2)
                use_time = time.monotonic() - start
                self.cachepictures_info.append(
                    ['{}'.format(len(self.cachepictures_info)),
                     [('Subtract', '({},{})'.format(coef1, coef2)), use_time], use_time])
                self.cachepictures_imgs.append([dst, ])
                self.CacheRefresh()
                cv2.namedWindow("Subtract")
                x, y = cv2.getWindowImageRect("Subtract")[0:2]
                if x < 0 or y < 0:
                    cv2.moveWindow("Subtract", x if x > 0 else 0, y if y > 0 else 0)
                self.Show_Picture('Subtract', dst)
            return
        if name == 'Partial':
            if self.now is None:
                QMessageBox.information(self, '提示', '未选中任何图片')
                return
            parameter, bool = QInputDialog.getText(self, '设置(位置、核大小)', '请输入(位置、核大小)', text='((0,0),(50,50))')
            if not bool:
                return
            parameter = eval(parameter)
            if len(self.now.shape) < 3:
                part = self.now[parameter[0][0]:parameter[0][0] + parameter[1][0],
                           parameter[0][1]:parameter[0][1] + parameter[1][1]]
            else:
                part = self.now[parameter[0][0]:parameter[0][0] + parameter[1][0],
                            parameter[0][1]:parameter[0][1] + parameter[1][1], :]
            self.cachepictures_info.append(
                ['{}'.format(len(self.cachepictures_info)), ('Partial', parameter), 0])
            self.cachepictures_imgs.append([part, ])
            self.CacheRefresh()
            cv2.namedWindow("Partial")
            x, y = cv2.getWindowImageRect("Partial")[0:2]
            if x < 0 or y < 0:
                cv2.moveWindow("Partial", x if x > 0 else 0, y if y > 0 else 0)
            self.Show_Picture('Partial', part)
            return

        if number == [None, None]:
            QMessageBox.information(self, '提示', '请选择要设置的步骤')
            return

        # 获取文本框数字，默认steps的长度
        if number[1] is None:
            l = len(self.steps[number[0]])
        else:
            l = number[1] + 1

        if name == 'Normalize':
            parameter, bool = QInputDialog.getText(self,
                                                   '设置(alpha=None, beta=None, norm_type=None, dtype=None, mask=None )',
                                                   '请输入(alpha=None, beta=None, norm_type=None, dtype=None, mask=None )',
                                                   text='(0, 255, cv2.NORM_MINMAX)')
            if not self.pictures_imgs:
                QMessageBox.information(self, '提示', '请选择图片')
                return
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Capture':
            parameter, bool = QInputDialog.getText(self, "设置([(色素区间1),(色素区间2)])",
                                                   "请输入([(色素区间1),(色素区间2)])",
                                                   text='([(0,255)])')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Resize':
            parameter, bool = QInputDialog.getText(self, '设置(dsize,dst,fx,fy,interpolation)',
                                                   '请输入(dsize(宽,高),dst,fx,fy,interpolation)\n'
                                                   'interpolation:\n'
                                                   '0 INTER_NEAREST(最近邻)'
                                                   '1 INTER_LINEAR(双线性插值)'
                                                   '2 INTER_CUBIC(双线性插值,比上面的快些)'
                                                   '3 INTER_AREA(使用像素区域关系重新采样)',
                                                   text='((800,800),None,1,1,1)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'ELA':
            parameter, bool = QInputDialog.getText(self, '设置(quality, scale)',
                                                   '请输入(quality(压缩幅度, 100为无损), scale(拉伸因子))\n',
                                                   text='(90, 1)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return


        ###################Filter########################
        if name == 'Blur':
            parameter, bool = QInputDialog.getText(self, '设置核大小', '请输入宽和高', text='(3,3)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'MedianBlur':
            parameter, bool = QInputDialog.getInt(self, '设置核大小', '请输入长度：', value=5, min=1, step=2)
            if not bool:
                return
            if parameter % 2 == 0:
                QMessageBox.information(self, '提示', '参数不能为偶数！')
            else:
                self.steps[number[0]].insert(l + 1, (name, str((parameter, parameter))))
                self.Fill()
            return
        if name == 'GaussianBlur':
            parameter, bool = QInputDialog.getText(self, '设置(ksize, sigmaX, dst=None, sigmaY=None, borderType=None)',
                                                   '请输入(ksize,sigmaX,dst,sigmaY,borderType)', text='((7,7),0,0)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return
        if name == 'BilateralFilter':
            parameter, bool = QInputDialog.getText(self, '设置(d, sigmaColor, sigmaSpace, dst=None, borderType=None)',
                                                   '请输入(d, sigmaColor, sigmaSpace, dst=None, borderType=None)',
                                                   text='(5,100,75)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'HomoFilter':
            parameter, bool = QInputDialog.getText(self, "设置(YH=1.5, YL=0.5, filter_params=(30, 2), filter='gaussian')",
                                                   "请输入(YH=1.5, YL=0.5, filter_params=(30(方差), 2(如果使用gaussian可忽略)), filter='gaussian'(gaussian或butterworth)",
                                                   text='(1.5,0.5,(30,2),"gaussian")')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'GuideFilter':
            parameter, bool = QInputDialog.getText(self, "设置(ksize, gsize, nums=1000, omega=0.95, eps=0.0001)",
                                                   "请输入(ksize, gsize, nums=1000, omega=0.95, eps=0.0001)",
                                                   text='(60, 60, 1000, 0.95, 0.0001)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'NLM':
            parameter, bool = QInputDialog.getText(self, "设置(h=None, templateWindowSize=None, searchWindowSize=None')",
                                                   "请输入(h=None, templateWindowSize=None, searchWindowSize=None)",
                                                   text='(1,7,21)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'MatchFilter':
            parameter, bool = QInputDialog.getText(self, "设置(长度,(核角度范围，角度间隔),sigma(标准差), 阈值系数)",
                                                   "请输入(长度,(核角度范围，角度间隔),sigma(标准差),阈值系数)\n",
                                                   text='(12, (0,180,15), 2, 3)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'HighPassFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置阈值",
                                                   "请输入阈值",
                                                   text='(40,None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'LowPassFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置阈值",
                                                   "请输入阈值",
                                                   text='(40,None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'IdealBandFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(D0,W,type)",
                                                   "请输入(D0(离中心点的距离),W(以D0为边的边界),type(0:带通 1:带阻)",
                                                   text='(20,20,0)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'GaussianBandFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(D0,W,type)",
                                                   "请输入(D0(离中心点的距离),W(以D0为边的边界),type(0:带通 1:带阻)",
                                                   text='(20, 0)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'ButterworthBandFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(Radius,N,type)",
                                                   "请输入(Radius(半径),N(系统阶数),type(0:带通 1:带阻)",
                                                   text='(20,2,0)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'MaxFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(Ksize, )",
                                                   "请输入(Ksize(半径),)",
                                                   text='(20,)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'MinFilter':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(Ksize, )",
                                                   "请输入(Ksize(半径),)",
                                                   text='(20,)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'MeanShiftFilter':
            parameter, bool = QInputDialog.getText(self, '设置(sp, sr, dst=None, maxLevel=None, termcrit=None)',
                                                   '请输入(sp(空间), sr(色素), dst=None, maxLevel=None, termcrit=None)',
                                                   text='(20,30,None,None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'FloodFill':
            parameter, bool = QInputDialog.getText(self, "设置(seedPoint, newVal, loDiff=None, upDiff=None, flags=None)",
                                                   "请输入(seedPoint, newVal, loDiff=None(差值上限), upDiff=None(差值下限), flags=None)\n"
                                                   "flags:\n"
                                                   '65536 FLOODFILL_FIXED_RANGE\n'
                                                   '131072 FLOODFILL_MASK_ONLY',
                                                   text='((0,0), 255, 30, 20, 65536)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return



        #######################Enhancement#######################
        if name == 'LogChange':
            parameter, bool = QInputDialog.getText(self, '设置系数', '请输入系数', text='(1, None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'AdaptEqualizeHist':
            parameter, bool = QInputDialog.getText(self, '设置(clipLimit, tileGridSize)',
                                                   '请输入(clipLimit(颜色对比度的阈值,越大的话，对比度越大), tileGridSize(窗口大小))',
                                                   text='(2.0, (8,8))')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'EqualizeHist':
            self.steps[number[0]].insert(l + 1, (name, "(None)"))
            self.Fill()
            return

        if name == 'Negate':
            self.steps[number[0]].insert(l + 1, (name, "(None)"))
            self.Fill()
            return

        if name == 'CalcBackProject':
            parameter, bool = QInputDialog.getText(self, '设置(range, scale)',
                                                   '请输入(range(直方图边界),scale(比例系数))',
                                                   text='([0,180],1)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Gamma':
            parameter, bool = QInputDialog.getText(self, '设置系数', '请输入系数', text='(0.5, None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'ConvertScaleAbs':
            parameter, bool = QInputDialog.getText(self, '设置(alpha=None, beta=None)',
                                                   '请输入(alpha=None, beta=None)',
                                                   text='(1,0)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Threshold':
            parameter, bool = QInputDialog.getText(self, '设置(thresh, maxval, type, dst=None)',
                                                   '请输入(thresh, maxval, type, dst=None)\n'
                                                   'type:\n'
                                                   '0 THRESH_BINARY\n'
                                                   '1 THRESH_BINARY_INV\n'
                                                   '2 THRESH_TRUNC\n'
                                                   '3 THRESH_TOZERO\n'
                                                   '4 THRESH_TOZERO_INV\n'
                                                   '7 THRESH_MASK\n'
                                                   '8 0THRESH_OTSU\n'
                                                   '16 THRESH_TRIANGLE',
                                                   text='(127, 255, 0 , None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'AdaptiveThreshold':
            parameter, bool = QInputDialog.getText(self,
                                                   '设置(maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)',
                                                   '请输入(maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None)\n'
                                                   'adaptiveMethod:\n'
                                                   '0 ADAPTIVE_THRESH_MEAN_C\n'
                                                   '1 ADAPTIVE_THRESH_GAUSSIAN_C\n'
                                                   'thresholdType:\n'
                                                   '0 THRESH_BINARY\n'
                                                   '1 THRESH_BINARY_INV\n',
                                                   text='(255, 0, 0, 11, 0, None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'AdaptContrastEnhancement':
            parameter, bool = QInputDialog.getText(self, '设置(ksize, alpha, maxG)',
                                                   '请输入(ksize, alpha(系统系数), maxG(系数最大上限))',
                                                   text='(3,0.5,10)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        #######################Edge#########################
        if name == 'HoughLine':
            parameter, bool = QInputDialog.getText(self,
                                                   '设置(size, color, thickness, rho, theta, threshold, lines=None, minLineLength=None, maxLineGap=None)',
                                                   '请输入(size, color, thickness, rho, theta, threshold, lines=None, minLineLength=None, maxLineGap=None)',
                                                   text='(10, (0, 255, 0), 2, 1, np.pi /180, 5, None, 5, 5)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Laplacian':
            parameter, bool = QInputDialog.getText(self, '设置( ksize=None, scale=None, delta=None, borderType=None)',
                                                   '请输入( ksize=None, scale=None, delta=None, borderType=None)',
                                                   text='(3,1,0,cv2.BORDER_DEFAULT)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Gabor':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置((核长度范围，长度间隔),(核角度范围，角度间隔),sigma(标准差),lambd(波长),gamma, psi=None, ktype=None)",
                                                   "请输入((核长度范围，长度间隔),(核角度范围，角度间隔),sigma(标准差),lambd(波长),gamma, psi=None, ktype=None)",
                                                   text='((7,20,2),(0,180,45),1,np.pi/2,0.5,0,cv2.CV_32F)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Canny':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(threshold1, threshold2, edges=None, apertureSize=None, L2gradient=None)",
                                                   "请输入(threshold1, threshold2, edges=None, apertureSize=None, L2gradient=None)",
                                                   text='(0, 20, None, None, None)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'USM':
            parameter, bool = QInputDialog.getText(self,
                                                   "设置(alpha=1.5, beta=-0.5, gamma=0, sigma=25)",
                                                   "请输入(alpha=1.5, beta=-0.5, gamma=0, sigma=25)",
                                                   text='(1.5, -0.5, 0, 25)')
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        if name == 'Sobel':
            parameter, bool = QInputDialog.getText(self, '设置(ddepth, dx, dy, dst=None, ksize=None)',
                                                   '请输入(ddepth, dx, dy, dst=None, ksize=None)',
                                                   text='(-1,1,0,-1,3)')
            if not bool:
                return
            if eval(parameter)[-1] % 2 == 0:
                QMessageBox.information(self, '提示', 'ksize不能为偶数！')
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        #########################算子######################
        if name[0:2] == '算子':
            self.steps[number[0]].insert(l + 1, (name, self.User[int(name[2:])]))
            self.Fill()
            return

        ######################Morphology######################
        if name == 'ERODE' or name == 'DILATE' or name == 'OPEN' or name == 'CLOSE' or name == 'TOPHAT' or name == 'BLACKHAT':
            parameter, bool = QInputDialog.getText(self,
                                                   '设置(核形状,核大小,[角度]dst=None, anchor=None, iterations=None, borderType=None, borderValue=None)',
                                                   '请输入(核形状(ELLIPSE RECT CROSS Line),核大小,[角度],\ndst=None, anchor=None, iterations=None, borderType=None, borderValue=None)',
                                                   text="('Line', (10,10), (0,180,15), None)")
            if not bool:
                return
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
            return

        #####################WaveTrans####################

        if name == 'Dwt_User':
            parameter, bool = QInputDialog.getText(self, '设置参数',
                                                   '请输入参数(level, mode, callback)',
                                                   text='(2, "haar", None)')
            if bool:
                self.steps[number[0]].insert(l + 1, (name, parameter))
                self.Fill()
            return

        if name == 'Dwt_Erode':
            parameter, bool = QInputDialog.getText(self, '设置参数',
                                                   '请输入参数(level, mode)',
                                                   text='(2, "haar")')
            if bool:
                self.steps[number[0]].insert(l + 1, (name, parameter))
                self.Fill()
            return

        if name == 'Dwt_Gauss':
            parameter, bool = QInputDialog.getText(self, '设置参数',
                                                   '请输入参数(level, mode)',
                                                   text='(2, "haar")')
            if bool:
                self.steps[number[0]].insert(l + 1, (name, parameter))
                self.Fill()
            return

        if name == 'Dwt_Threshold':
            parameter, bool = QInputDialog.getText(self, '设置参数',
                                                   '请输入参数(level, mode, 类型("hard" or "soft"), value)',
                                                   text='(2, "haar", "hard", 50)')
            if bool:
                self.steps[number[0]].insert(l + 1, (name, parameter))
                self.Fill()
            return

        #####################噪声############################

        if name == 'GaussNoise':
            parameter, bool = QInputDialog.getText(self, '设置参数',
                                                   '请输入参数(mean, sigma)',
                                                   text='(0, 0.1)')
            if bool:
                self.steps[number[0]].insert(l + 1, (name, parameter))
                self.Fill()
            return

        #####################自定义函数#######################
        parameter, bool = QInputDialog.getText(self, '设置参数',
                                               '请输入参数',
                                               text='(None)')
        if bool:
            self.steps[number[0]].insert(l + 1, (name, parameter))
            self.Fill()
