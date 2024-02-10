import cv2
import numpy as np
from math import pi,tan

# 自定义任意角度的线段结构元素
def strel(l, angle):
    theta = angle / 180 * pi
    model = np.zeros((l, l), dtype='uint8')
    mid = l // 2
    for i in range(l):
        for j in range(l):
            y_ = (i - mid) * np.cos(theta) + (j - mid) * np.sin(theta)
            if abs(y_) < 0.5:
                model[i][j] = 1
    return model

    # def Angle(l, angle):
    #     model = np.zeros((l, l), dtype='uint8')
    #     a = abs(tan(angle / 180 * pi))
    #     #找到中心点
    #     x, y = l // 2, l // 2
    #     model[x, y] = 1
    #     if angle == 0 or angle == 180:
    #         model[y, 0:l] = 1
    #         return model
    #     if angle == 90:
    #         model[0:l, x] = 1
    #         return model
    #     for i in range(x + 1, l):
    #         left, right = 1, l // 2 + 1
    #         #采用二分类直到值最接近对应角度的正切值
    #         while left <= right:
    #             mid = (left + right) // 2
    #             if (y - mid) / (i - x) < a:
    #                 right = mid - 1
    #             else:
    #                 left = mid + 1
    #         model[left - 1, i] = 1
    #         model[2 * x - left + 1, 2 * y - i] = 1
    #     return model
    #
    # if angle <= 45:
    #     return Angle(l, angle)
    # elif angle <= 90:
    #     model = Angle(l, 90 - angle)
    #     return model.T
    # elif angle <= 135:
    #     model = Angle(l, angle - 90)
    #     return model[::-1].T
    # else:
    #     model = Angle(l, 180 - angle)
    #     return model[::-1]

def Kernal(name, size):
    kernal = None
    if name == 'ELLIPSE':
        kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
    elif name == 'RECT':
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, size)
    elif name == 'CROSS':
        kernal = cv2.getStructuringElement(cv2.MORPH_CROSS, size)
    return kernal


# 形态学重建 由于需要设置两个图片为变量，且图片位置在内外部都有可能，暂时无法在软件内提供
def Imreconstruct(marker, mask, op, SE=np.ones([3, 3])):
    """
    描述：以mask为约束，连续膨胀marker，实现形态学重建，其中mask >= marker

    参数：
        - marker 标记图像，单通道/三通道图像
        - mask   模板图像，与marker同型
        - conn   联通性重建结构元，参照matlab::imreconstruct::conn参数，默认为8联通
    """
    marker_pre = mask.copy()
    marker_now = marker.copy()
    temp = 0
    while True:
        kernal = cv2.getStructuringElement(cv2.MORPH_CROSS, SE)
        dilation = cv2.morphologyEx(marker_now, op, SE)
        if op == cv2.MORPH_DILATE:
            marker_now = np.min((dilation, mask), axis=0)
        elif op == cv2.MORPH_ERODE:
            marker_now = np.max((dilation, mask), axis=0)
        cur = np.sum((marker_pre == marker_now)) / (marker.shape[0] * marker.shape[1])
        if cur > 0.99 or cur == temp:
            break
        temp = cur
    return marker_now


# 腐蚀
def ERODE(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.erode(image, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.where(dst > imgs[i], dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_ERODE, kernal, *args[2:])


# 膨胀
def DILATE(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.dilate(image, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.where(dst < imgs[i], dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_DILATE, kernal, *args[2:])


# 开运算
def OPEN(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.morphologyEx(image, cv2.MORPH_OPEN, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.minimum(dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernal, *args[2:])


# 闭运算
def CLOSE(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.maximum(dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal, *args[2:])


# 顶帽
def TOPHAT(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.where(dst > imgs[i], dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernal, *args[2:])


# 黑帽
def BLACKHAT(image, args):
    if args[0] == 'Line':
        kernals = [strel(args[1][0], angle) for angle in
                   range(args[2][0], args[2][1], args[2][2])]
        imgs = []
        for kernal in kernals:
            imgs.append(cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernal, *args[3:]))
        dst = imgs[0]
        for i in range(1, len(kernals)):
            dst = np.where(dst < imgs[i], dst, imgs[i])
        return dst
    else:
        kernal = Kernal(args[0], args[1])
        return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernal, *args[2:])