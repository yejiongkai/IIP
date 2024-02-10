import os
import shutil

class Export:
    def __init__(self, address: str, steps: list, every_show=False):
        self.headers = ['from module.Filter import *', 'from module.Enhancement import *', 'from module.Morphology import *',
                        'from module.Else import *', 'from module.Edge import *', 'import cv2', 'import numpy as np']
        self.address = address
        self.steps = steps
        self.every_show = every_show

    def export(self):
        with open(self.address, 'w+') as f:
            x = 0
            f.writelines([header+'\n' for header in self.headers])
            f.write('\n')
            f.write('img = cv2.imread("address")\n')
            step = self.steps[1]
            if type(step) is type(()):  # 如果有一堆数据
                if step[0][0:2] == '算子':
                    f.write('result{} = {}({},{})\n'.format(x, 'UserDefined', 'img', 'np.array({})'.format(step[1])))
                else:
                    f.write('result{} = {}({},{})\n'.format(x, step[0], 'img', str(step[1])))
            else:  # 没有参数
                f.write('result{} = {}({})\n'.format(x, step, 'img'))
            if self.every_show or len(self.steps) <= 2:
                f.write('#cv2.imshow("result{0}", result{0})\n'.format(x))
            x += 1
            for step in self.steps[2:]:
                if type(step) is type(()):  # 如果有一堆数据
                    if step[0][0:2] == '算子':
                        f.write('result{} = {}({},{})\n'.format(x, step[0], 'result{}'.format(x-1), 'np.array({})'.format(step[1])))
                    else:
                        f.write('result{} = {}({},{})\n'.format(x, step[0], 'result{}'.format(x-1), str(step[1])))
                else:  # 没有参数
                    f.write('result{} = {}({})\n'.format(x, step, 'result{}'.format(x-1)))
                if self.every_show:
                    f.write('#cv2.imshow("result{0}", result{0})\n'.format(x))
                x += 1
            if not self.every_show and len(self.steps) > 2:
                f.write('cv2.imshow("result{0}", result{0})\n'.format(x-1))
            f.write('cv2.waitKey(0)')


if __name__ == '__main__':
    a = Export('E:result.py',[['1','hellow',(1,2,3)],['2','hi',(3,2,1)]])
    a.export()
