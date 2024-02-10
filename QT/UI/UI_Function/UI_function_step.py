from PyQt5.Qt import Qt, QMessageBox, QInputDialog, QFileDialog, QCursor, QTreeWidgetItem, QDialog
import os
import cv2
import numpy as np
from pickle import dump, load
from UI_Function.UI_ADD import UI_ADD
from UI_Export import Export
from UI_Modify import UI_Modify


class UI_function_step(UI_ADD):
    ###########自定义函数###################
    def User_Define(self):
        """
        用于识别文件中的自定义函数
        函数格式应为 function(image, args)
        注意：args应为一个元组
        """
        address, ok = QFileDialog.getOpenFileName(self, '选择文件', self.address)
        if address:
            try:
                with open(address, 'r+') as f, open('QT/module/UserDefine.py', 'a+') as e:
                    e.write('\n')
                    e.writelines(f.readlines())
            except Exception as error:
                QMessageBox.information(self, '警告', '{}'.format(error))
            self.User_Init()

    ####################导出步骤#######################
    def ExportStep(self):
        for number in self.numbers:
            if len(self.steps[number[0]]) <= 1:
                QMessageBox.information(self, '提示', '所选步骤为空')
                return
            address, _ = QFileDialog.getSaveFileName(self, '保存文件', self.address,
                                                     "(*.py)", )
            if address:
                choose = QMessageBox.information(self, '选择', '是否在每步后面添加#imshow', QMessageBox.Yes | QMessageBox.No)
                if choose == QMessageBox.Yes:
                    if number[1] is None:
                        export = Export(address, self.steps[number[0]], True)
                    else:
                        export = Export(address, [None, self.steps[number[0]][number[1] + 1]], True)
                else:
                    if number[1] is None:
                        export = Export(address, self.steps[number[0]], False)
                    else:
                        export = Export(address, [None, self.steps[number[0]][number[1] + 1]], False)
                export.export()

    #####################切换步骤##############################
    def SwitchStep(self):
        choose = QMessageBox.warning(self, '提示', '确定要切换步骤吗？', QMessageBox.Yes | QMessageBox.No)
        if choose == QMessageBox.No:
            return False
        if self.address_step and os.path.exists(self.address_step):
            with open(self.address_step, 'rb+') as f:
                try:
                    cur = load(f)
                    if cur != self.steps:
                        choose = QMessageBox.information(self, '提示', '你的步骤已被修改，是否保存当前步骤？',
                                                         QMessageBox.Yes | QMessageBox.No)
                        if choose == QMessageBox.Yes:
                            self.SAVE()
                except EOFError:
                    pass
        return True

    #####################新建步骤文件###################
    def MakeStepProject(self):
        choose = self.SwitchStep()
        if not choose:
            return
        fname, bool = QInputDialog.getText(self, '设置名称', '请输入名称', text='')
        if bool:
            fname = os.path.join(self.address, fname)
            with open(fname + '.step', 'wb+') as f:
                self.address_step = fname + '.step'
                self.steps = []
                self.numbers = []
                self.StepInit()
                address = os.path.split(self.address_step)[-1]
                self.step_label.setText(address)
                self.step_label.setToolTip(self.address_step)

    #####################打开步骤文件#####################
    def OpenStepProject(self):
        choose = self.SwitchStep()
        if not choose:
            return
        fname, t = QFileDialog.getOpenFileName(self, '打开步骤文件', self.cur_step_address,
                                               "(*.step)")  # 空白等于（*）就是全部文件
        if not fname:
            return
        if fname[-4:] != 'step':
            QMessageBox.information(self, '提示', '请选择step后缀的文件')
            return
        with open(fname, 'rb+') as f:
            try:
                self.cur_step_address = os.path.join(fname, os.pardir)
                cur = load(f)
                self.steps = cur
            except EOFError:
                self.steps = []
        self.address_step = fname
        self.numbers = []
        address = os.path.split(self.address_step)[-1]
        self.step_label.setText(address)
        self.step_label.setToolTip(self.address_step)
        self.StepInit()

    #######################步骤列表的右键菜单##################
    def myListWidgetContext(self, point):
        self.STEP_CHOOSE()
        if self.List.currentItem():
            self.Menu.exec_(QCursor.pos())

    ######################右键菜单功能########################
    def COPY(self):
        self.STEP_CHOOSE()
        self.copy = []
        for number in self.numbers:
            if number[1] is None:
                self.copy += self.steps[number[0]][1:].copy()
            else:
                self.copy += [self.steps[number[0]][number[1] + 1]]

    def PASTE(self):
        if not self.copy:
            return
        self.STEP_CHOOSE()
        for number in self.numbers:
            if number[1] is None:
                self.steps[number[0]] += self.copy
            else:
                self.steps[number[0]] = self.steps[number[0]][:number[1] + 2] + \
                                        self.copy + self.steps[number[0]][number[1] + 2:]
        self.Fill()

    def Modify(self):
        for number in self.numbers:
            if len(self.steps[number[0]]) < 2:
                continue
            if number[1] is None:
                modify = UI_Modify(self.steps[number[0]][1:], self)
                if modify.exec_() == QDialog.Accepted:
                    self.steps[number[0]][1:] = modify.result.copy()
                    self.Fill()
                # parameter, bool = QInputDialog.getMultiLineText(self, '修改内容', '请输入修改内容(一定要按格式修改)',
                #                                                 text=str(self.steps[number[0]][1:]))
                # if bool:
                #     try:
                #         cur = eval(parameter)
                #     except Exception as e:
                #         QMessageBox.information(self, '提示', str(e))
                #         return
                #     self.steps[number[0]][1:] = cur
                #     self.Fill()
            else:
                modify = UI_Modify([self.steps[number[0]][number[1] + 1]], self)
                if modify.exec_() == QDialog.Accepted:
                    self.steps[number[0]][number[1] + 1] = modify.result[0]
                    self.Fill()
                # parameter, bool = QInputDialog.getMultiLineText(self, '修改内容', '请输入修改内容(一定要按格式修改)',
                #                                                 text=str(self.steps[number[0]][number[1] + 1]))
                # if bool:
                #     try:
                #         cur = eval(parameter)
                #     except NameError:
                #         self.steps[number[0]][number[1] + 1] = parameter
                #         self.Fill()
                #         return
                #     except SyntaxError as e:
                #         QMessageBox.information(self, '警告', str(e))
                #         return
                #     self.steps[number[0]][number[1] + 1] = cur
                #     self.Fill()

    ####################删除整行#######################
    def DELETELINE(self):
        self.numbers = sorted(self.numbers, key=lambda x: (x[0], x[1]))
        for i, number in enumerate(self.numbers):
            if not self.steps or number == [None, None]:
                QMessageBox.information(self, '提示', '并未选中任何项目')
                return
            elif number[1] is None:
                self.steps.pop(number[0])
                for step in self.steps[number[0]:]:
                    step[0] = str(int(step[0]) - 1)
                self.StepInit()
                if number[0] >= len(self.steps):
                    self.numbers = []
                for j in range(i + 1, len(self.numbers)):
                    self.numbers[j][0] -= 1
            else:
                self.steps[number[0]].pop(number[1] + 1)
                self.One_Step_Changed((number[0], number[1]))
                for j in range(i + 1, len(self.numbers)):
                    if self.numbers[j][0] == self.numbers[i][0]:
                        self.numbers[j][1] -= 1
                    else:
                        break
            if number[0] >= 0:
                self.List.setCurrentItem(self.List.topLevelItem(number[0]))
        self.STEP_CHOOSE()

    ########################删除###########################
    # def DELETE(self):  # 注意第一个元素是行号
    #     if not self.steps or number == [None, None]:
    #         QMessageBox.information(self, '提示', '并未选中任何项目')
    #     elif len(self.steps[number[0]]) > 2:
    #         if number[1] is None:
    #             if self.line.text().isdigit() or self.line.text() == '':
    #                 l = int(self.line.text()) if (self.line.text() != '') else -1
    #                 if l == 0:
    #                     l = 1
    #                 if l < len(self.steps[number[0]]):
    #                     self.steps[number[0]].pop(l)
    #                 else:
    #                     self.steps[number[0]].pop()
    #             else:
    #                 QMessageBox.information(self, '提示', '要删除步骤请输入数字')
    #         else:
    #             self.steps[number[0]].pop(number[1] + 1)
    #         self.Fill()
    #     elif len(self.steps[number[0]]) <= 2:
    #         self.steps.pop(number[0])
    #         for i in self.steps[number[0]:]:
    #             i[0] = str(int(i[0]) - 1)
    #         self.StepInit()
    #         number = [None, None]

    ##################将已执行步骤放到步骤列表中################
    def DONETOSTEP(self):
        if len(self.pictures_info) > 1:
            l = len(self.steps)
            step = [step for picture in self.pictures_info[1:]
                         for step_list in picture[1:-1]
                         for step in step_list[:1] if step is not None]
            self.steps.append([str(len(self.steps))] + step)
            self.Insert_Fill(l)

    ########################保存步骤#####################
    def SAVE(self):
        if self.steps:
            if self.address_step:
                with open(self.address_step, 'wb+') as f:
                    dump(self.steps, f)
            else:
                address, _ = QFileDialog.getSaveFileName(self, '保存步骤文件', self.address, "(*.step)",)
                if address:
                    self.address_step = address
                    with open(self.address_step, 'wb+') as f:
                        dump(self.steps, f)
                    self.step_label.setText(os.path.split(address)[-1])

        else:
            if self.address_step:
                with open(self.address_step, 'wb+'):
                    pass

    #########################添加项目到步骤文件######################
    def MAKE(self):
        if not self.numbers:
            self.steps.append([str(len(self.steps))])
            number = [len(self.steps) - 1, 0]
            self.Insert_Fill(number[0])
        else:
            self.numbers = sorted(self.numbers, key=lambda x: (x[0], x[1]))
            for i, number in enumerate(self.numbers):
                self.steps.insert(number[0] + 1, [str(number[0] + 1)])
                for step in self.steps[number[0] + 2:]:
                    step[0] = str(int(step[0]) + 1)
                for j in range(i + 1, len(self.numbers)):
                    self.numbers[j][0] += 1
                self.StepInit()
                self.List.setCurrentItem(self.List.topLevelItem(number[0] + 1))
                self.numbers[i][0] += 1

    ###########################获取列表中选中的行#############################
    def STEP_CHOOSE(self):
        self.numbers = []
        for index in self.List.selectedIndexes():
            if index.parent().isValid():
                self.numbers.append([index.parent().row(), index.row()])
            else:
                self.numbers.append([index.row(), None])

    #################操作步骤的各种情况####################

    # 初始化
    def StepInit(self):
        self.List.clear()
        if self.steps:
            x = 0
            for step in self.steps:
                item = QTreeWidgetItem(self.List)
                item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
                item_text = step[0]
                for i in range(len(step[1:])):
                    group = QTreeWidgetItem(item)
                    if type(step[i + 1]) is type(()):  # 如何包含参数
                        if step[i + 1][0][0:2] == '算子':
                            group.setText(0, step[i + 1][0])
                            item_text += ' {}'.format(step[i + 1][0])
                        else:
                            # if step[i+1][0] == 'DILATE' or step[i+1][0] == 'ERODE' or step[i+1][0] == 'TOPHAT' or step[i+1][0] == 'OPEN' or step[i+1][
                            #     0] == 'CLOSE' or step[i+1][0] == 'BLACKHAT':
                            #     s = eval(step[i+1][1])
                            #     if s[0] == 'Line':
                            #         k = (step[i+1][0], str(('Line', (s[1][0], s[1][0]), s[2], s[3])))
                            #         print(k)
                            #         print(self.steps[x][i+1])
                            #         self.steps[x][i+1] = k
                            if not isinstance(eval(step[i+1][1]), tuple) and eval(step[i+1][1]) is not None:
                                self.steps[x][i+1] = (step[i+1][0], "(" + step[i+1][1] + ", None)")
                            group.setText(0, '{}[{}]'.format(step[i + 1][0], step[i + 1][1]))
                            item_text += ' {}[{}]'.format(step[i + 1][0], step[i + 1][1])

                    else:  # 无参数
                        k = (step[i+1], "(None)")
                        self.steps[x][i+1] = k
                        group.setText(0, '{}[{}]'.format(step[i + 1][0], step[i+1][1]))
                        item_text += ' {}[{}]'.format(step[i + 1][0], step[i+1][1])
                    # item.addChild(group)
                item.setText(0, item_text)
                # self.List.addTopLevelItem(item)
                x += 1

    def One_Step_Changed(self, position: list):
        str = self.steps[position[0]][0]
        steps = self.steps[position[0]][1:]
        while self.List.topLevelItem(position[0]).childCount() < len(steps):
            self.List.topLevelItem(position[0]).addChild(QTreeWidgetItem())
        while self.List.topLevelItem(position[0]).childCount() > len(steps):
            self.List.topLevelItem(position[0]).removeChild(self.List.topLevelItem(position[0]).child(0))
        for j in range(len(steps)):
            if type(steps[j]) is type(()):
                if steps[j][0][0:2] == '算子':
                    self.List.topLevelItem(position[0]).child(j).setText(0, steps[j][0])
                    str += ' {}'.format(steps[j][0])
                else:
                    self.List.topLevelItem(position[0]).child(j).setText(0, '{}[{}]'.format(steps[j][0], steps[j][1]))
                    str += ' {}[{}]'.format(steps[j][0], steps[j][1])
            else:
                self.List.topLevelItem(position[0]).child(j).setText(0, steps[j])
                str += ' {}'.format(steps[j])
        self.List.topLevelItem(position[0]).setText(0, str)

    # 刷新单个步骤的修改
    def Fill(self):
        for number in self.numbers:
            self.One_Step_Changed(number)

    # 插入步骤列表的刷新, 发现速度很慢, 目前只能用在最后加
    def Insert_Fill(self, l):
        item = QTreeWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
        self.List.insertTopLevelItem(l, item)
        self.List.setCurrentItem(item)
        self.numbers = [[l, None]]
        self.Fill()
        # for i in range(l + 1, len(self.steps)):
        #     text = self.List.topLevelItem(i).text(0).split()
        #     text[0] = str(int(text[0]) + 1)
        #     self.List.topLevelItem(i).setText(0, ' '.join(text))

    # 获取步骤文件
    def Information_Step(self):
        if self.address_step and os.path.exists(self.address_step):
            if os.path.exists(self.address_step):
                with open(self.address_step, 'rb+') as f:
                    try:
                        self.steps = load(f)
                    except EOFError:
                        return
            else:
                with open(self.address_step, 'wb+'):
                    pass

    # 列表中节点次序改变
    def Step_Item_Row_Changed(self, start, end):
        """
            同级：交换， 上级向下级：覆盖  下级向上级：添加
        """
        start_priority, end_priority = 0, 0
        for i in range(len(start)):
            if start[i] is not None:
                start_priority += 1
            if end[i] is not None:
                end_priority += 1

        # 如果同级 交换
        if start_priority == end_priority:
            if start[1] is None:
                self.steps[start[0]][1:], self.steps[end[0]][1:] = self.steps[end[0]][1:], self.steps[start[0]][1:]
            else:
                self.steps[start[0]][start[1] + 1], self.steps[end[0]][end[1] + 1] = \
                    self.steps[end[0]][end[1] + 1], self.steps[start[0]][start[1] + 1]

            self.One_Step_Changed(start)
            self.One_Step_Changed(end)

        # 上级向下级:覆盖
        elif start_priority < end_priority:
            self.steps[end[0]].pop(end[1] + 1)
            self.steps[end[0]] = self.steps[end[0]][:end[1] + 1] + self.steps[start[0]][1:] + self.steps[end[0]][
                                                                                              end[1] + 1:]
            self.One_Step_Changed(end)

        # 下级向上级：添加
        elif start_priority > end_priority:
            self.steps[end[0]].append(self.steps[start[0]][start[1] + 1])
            self.One_Step_Changed(end)
