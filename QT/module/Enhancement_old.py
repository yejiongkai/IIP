from AdaptContrastEnhancement import adaptContrastEnhancement
import cv2
import numpy as np


# 阈值处理
def Threshold(image, args):
    return cv2.threshold(image, *args)[1]


#自适应阈值
def AdaptiveThreshold(image, args):
    return cv2.adaptiveThreshold(image, *args)


# 直方图均衡化
def EqualizeHist(image, args):
    dst = image.copy()
    if len(image.shape) == 2:
        return cv2.equalizeHist(dst)
    else:
        ycrcb = cv2.cvtColor(dst, cv2.COLOR_BGR2YCR_CB)
        channels = cv2.split(ycrcb)
        cv2.equalizeHist(channels[0], channels[0])
        cv2.merge(channels, ycrcb)
        cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, dst)
        return dst


# 自适应直方图均衡化
def AdaptEqualizeHist(image, args):
    """
    :param image:
    :param args:
     0   clipLimit：越大的话，对比度越低
     1   tileGridSize:划分每个区域块的大小
    :return:
    """
    dst = image.copy()
    clahe = cv2.createCLAHE(*args)
    if len(dst.shape) == 2:
        return clahe.apply(dst)
    else:
        ycrcb = cv2.cvtColor(dst, cv2.COLOR_BGR2YCR_CB)
        channels = list(cv2.split(ycrcb))
        channels[0] = clahe.apply(channels[0])
        cv2.merge(channels, ycrcb)
        cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, dst)
        return dst


# 灰度线性变换
def LinearGrayTran(Image, callback):
    image = Image.copy()
    width = image.shape[0]
    height = image.shape[1]
    for i in range(width):
        for j in range(height):
            if (i - 400) ** 2 + (j - 400) ** 2 >= 400 ** 2:
                image[i][j] = 255
            else:
                image[i][j] = callback(image[i][j])
    return image


# 对数变换
def LogChange(image, args):
    c = args[0]
    img2 = np.log1p(image.astype('float64')+1) * c
    return cv2.normalize(img2, -1, 0, 255, cv2.NORM_MINMAX).astype('uint8')


# 自适应对比度增强
def AdaptContrastEnhancement(image, args):
    return adaptContrastEnhancement(image, *args)


# 调节亮度和对比度
def ConvertScaleAbs(image, args):
    return cv2.convertScaleAbs(image, -1, *args)


def Gamma(image, args):
    gamma = args[0]
    # 具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # 实现映射用的是Opencv的查表函数
    return cv2.LUT(image, gamma_table)


# 取反
def Negate(image, args):
    return 255 - image


# 直方图反向投影
def CalcBackProject(image, args):
    """
    :param image:
    :param args:
    0 ranges 直方图边界
    1 scale 输出反向投影的可选比例因子
    :return:
    """
    hist = cv2.calcHist([image], [0], None, [12], [0,12])
    return cv2.calcBackProject([image], [0], hist, *args)

