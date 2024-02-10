from pywt import *
from module.Morphology_old import *
import module.UserDefine as User
from functools import partial
import cv2
import numpy as np


def DWT(image, level, mode, callback=None, now=1):
    if now == level:
        if callback:
            return callback(dwt2(image, mode), now, mode)
        return dwt2(image, mode)
    else:
        cA, (cH, cV, cD) = dwt2(image, mode)
        if callback:
            cA, (cH, cV, cD) = callback((cA, (cH, cV, cD)), now, mode)
        return *DWT(cA, level, mode, callback, now+1), (cH, cV, cD)


def IDWT(coeffs, level, mode):
    dst = coeffs[0]
    for i in range(1, level+1):
        dst = idwt2((dst, coeffs[i]), mode)
    return dst


def Erode_Filter(args, level, mode):
    """
    :param args: cA, (cH, cV, cD)
    :param level:
    :param mode:
    :return: cA, (cH, cV, cD)
    """
    cA, (cH, cV, cD) = args
    mask_h = cH < 0
    mask_v = cV < 0
    mask_d = cD < 0
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    # cv2.imshow('h1', cH.astype('uint8'))
    if level == 1:
        width, height = cH.shape
        cH_pre = cv2.resize(cH, (800, 800))
        cV_pre = cv2.resize(cV, (800, 800))
        cD_pre = cv2.resize(cD, (800, 800))
        # cv2.imshow('h1', cH_pre.clip(0, 255).astype('uint8'))
        # cH = ERODE(cH, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cV = ERODE(cV, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cD = ERODE(cD, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cH = DILATE(cH, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cV = DILATE(cV, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cD = DILATE(cD, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cH = cv2.medianBlur(cH_pre.astype('uint8'), 9)
        # cV = cv2.medianBlur(cV_pre.astype('uint8'), 9)
        # cD = cv2.medianBlur(cD_pre.astype('uint8'), 9)
        cH = ERODE(cH_pre, ('Line', (15, 16, 2), (0, 180, 30), None))
        cV = ERODE(cV_pre, ('Line', (15, 16, 2), (0, 180, 30), None))
        cD = ERODE(cD_pre, ('Line', (15, 16, 2), (0, 180, 30), None))

        cH = Imreconstruct(cH, cH_pre, cv2.MORPH_DILATE, (3, 1))
        cV = Imreconstruct(cV, cV_pre, cv2.MORPH_DILATE, (1, 3))
        # cD = Imreconstruct(cD, cD_pre, cv2.MORPH_DILATE, (3, 3))

        # cH = DILATE(cH, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cV = DILATE(cV, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cD = DILATE(cD, ('Line', (15, 16, 2), (0, 180, 15), None))
        cH = cv2.resize(cH, (width, height))
        cV = cv2.resize(cV, (width, height))
        cD = cv2.resize(cD, (width, height))
    elif level == 2:
        width, height = cH.shape
        cH_pre = cv2.resize(cH, (800, 800))
        cV_pre = cv2.resize(cV, (800, 800))
        cD_pre = cv2.resize(cD, (800, 800))
        # cv2.imshow('h2', cH_pre.clip(0, 255).astype('uint8'))
        # cH = cv2.medianBlur(cH_pre.astype('uint8'), 9)
        # cV = cv2.medianBlur(cV_pre.astype('uint8'), 9)
        # cD = cv2.medianBlur(cD_pre.astype('uint8'), 9)
        # cH = ERODE(cH, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cV = ERODE(cV, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cD = ERODE(cD, ('Line', (15, 16, 2), (0, 180, 15), None))
        # cH = DILATE(cH, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cV = DILATE(cV, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cD = DILATE(cD, ('Line', (5, 6, 2), (0, 180, 45), None))
        cH = ERODE(cH_pre, ('Line', (11, 12, 2), (0, 180, 30), None))
        cV = ERODE(cV_pre, ('Line', (11, 12, 2), (0, 180, 30), None))
        cD = ERODE(cD_pre, ('Line', (11, 12, 2), (0, 180, 30), None))

        cH = Imreconstruct(cH, cH_pre, cv2.MORPH_DILATE, (3, 1))
        cV = Imreconstruct(cV, cV_pre, cv2.MORPH_DILATE, (1, 3))
        # cD = Imreconstruct(cD, cD_pre, cv2.MORPH_DILATE, (3, 3))
        # cH = DILATE(cH, ('Line', (9, 10, 2), (0, 180, 15), None))
        # cV = DILATE(cV, ('Line', (9, 10, 2), (0, 180, 15), None))
        # cD = DILATE(cD, ('Line', (9, 10, 2), (0, 180, 15), None))
        # cv2.imshow('h4', cH_pre.clip(0, 255).astype('uint8'))
        # cv2.waitKey(0)
        cH = cv2.resize(cH, (width, height))
        cV = cv2.resize(cV, (width, height))
        cD = cv2.resize(cD, (width, height))
    elif level == 3:
        width, height = cH.shape
        cH_pre = cv2.resize(cH, (800, 800))
        cV_pre = cv2.resize(cV, (800, 800))
        cD_pre = cv2.resize(cD, (800, 800))
        # cv2.imshow('h3', cH_pre.clip(0,255).astype('uint8'))
        # cv2.waitKey(0)
        # cH = cv2.medianBlur(cH_pre.astype('uint8'), 9)
        # cV = cv2.medianBlur(cV_pre.astype('uint8'), 9)
        # cD = cv2.medianBlur(cD_pre.astype('uint8'), 9)
        # cH = DILATE(cH, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cV = DILATE(cV, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cD = DILATE(cD, ('Line', (5, 6, 2), (0, 180, 45), None))
        cH = ERODE(cH_pre, ('Line', (7, 8, 2), (0, 180, 30), None))
        cV = ERODE(cV_pre, ('Line', (7, 8, 2), (0, 180, 30), None))
        cD = ERODE(cD_pre, ('Line', (7, 8, 2), (0, 180, 30), None))

        cH = Imreconstruct(cH, cH_pre, cv2.MORPH_DILATE, (3, 1))
        cV = Imreconstruct(cV, cV_pre, cv2.MORPH_DILATE, (1, 3))
        # cD = Imreconstruct(cD, cD_pre, cv2.MORPH_DILATE, (3, 3))
        # cH = DILATE(cH, ('Line', (7, 9, 2), (0, 180, 15), None))
        # cV = DILATE(cV, ('Line', (7, 9, 2), (0, 180, 15), None))
        # cD = DILATE(cD, ('Line', (7, 9, 2), (0, 180, 15), None))

        # cv2.imshow('h2', cH.clip(0,255).astype('uint8'))
        # cv2.waitKey(0)

        cH = cv2.resize(cH, (width, height))
        cV = cv2.resize(cV, (width, height))
        cD = cv2.resize(cD, (width, height))
    elif level == 4:
        width, height = cH.shape
        cH_pre = cv2.resize(cH, (800, 800))
        cV_pre = cv2.resize(cV, (800, 800))
        cD_pre = cv2.resize(cD, (800, 800))
        # cH = DILATE(cH, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cV = DILATE(cV, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cD = DILATE(cD, ('Line', (5, 6, 2), (0, 180, 45), None))
        # cH = cv2.medianBlur(cH_pre.astype('uint8'), 5)
        # cV = cv2.medianBlur(cV_pre.astype('uint8'), 5)
        # cD = cv2.medianBlur(cD_pre.astype('uint8'), 5)
        cH = ERODE(cH_pre, ('Line', (7, 8, 2), (0, 180, 30), None))
        cV = ERODE(cV_pre, ('Line', (7, 8, 2), (0, 180, 30), None))
        cD = ERODE(cD_pre, ('Line', (7, 8, 2), (0, 180, 30), None))


        cH = Imreconstruct(cH, cH_pre, cv2.MORPH_DILATE, (3, 1))
        cV = Imreconstruct(cV, cV_pre, cv2.MORPH_DILATE, (1, 3))
        # cD = Imreconstruct(cD, cD_pre, cv2.MORPH_DILATE, (3, 3))
        # cH = DILATE(cH, ('Line', (7, 9, 2), (0, 180, 15), None))
        # cV = DILATE(cV, ('Line', (7, 9, 2), (0, 180, 15), None))
        # cD = DILATE(cD, ('Line', (7, 9, 2), (0, 180, 15), None))

        cH = cv2.resize(cH, (width, height))
        cV = cv2.resize(cV, (width, height))
        cD = cv2.resize(cD, (width, height))
    # cv2.imshow('h2', cH.astype('uint8'))
    # cv2.waitKey(0)
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    return cA, (cH, cV, cD)


def GaussianBur_Filter(args, level, mode):
    """
    :param args: cA, (cH, cV, cD)
    :param level:
    :param mode:
    :return: cA, (cH, cV, cD)
    """
    cA, (cH, cV, cD) = args
    mask_h = cH < 0
    mask_v = cV < 0
    mask_d = cD < 0
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    if level == 1:
        cH = cv2.GaussianBlur(cH, (7,7), 0)
        cV = cv2.GaussianBlur(cV, (7,7), 0)
        cD = cv2.GaussianBlur(cD, (7,7), 0)
    elif level == 2:
        cH = cv2.GaussianBlur(cH, (5, 5), 0)
        cV = cv2.GaussianBlur(cV, (5, 5), 0)
        cD = cv2.GaussianBlur(cD, (5, 5), 0)
    elif level == 3:
        cH = cv2.GaussianBlur(cH, (3, 3), 0)
        cV = cv2.GaussianBlur(cV, (3, 3), 0)
        cD = cv2.GaussianBlur(cD, (3, 3), 0)
    elif level == 4:
        cH = cv2.GaussianBlur(cH, (3, 3), 0)
        cV = cv2.GaussianBlur(cV, (3, 3), 0)
        cD = cv2.GaussianBlur(cD, (3, 3), 0)
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    return cA, (cH, cV, cD)


def Threshold_Filter(t, value, args, level=None, mode=None):
    """
    :param args: cA, (cH, cV, cD)
    :param level:
    :param mode:
    :param t:
    :param value:
    :return:
    """
    cA, (cH, cV, cD) = args
    mask_h = cH < 0
    mask_v = cV < 0
    mask_d = cD < 0
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    if t == 'hard':
        cH[cH < value] = 0
        cV[cV < value] = 0
        cD[cD < value] = 0
    elif t == 'soft':
        cH[cH < value] = 0
        cH[cH >= value] = cH[cH >= value] - value
        cV[cV < value] = 0
        cV[cV >= value] = cV[cV >= value] - value
        cD[cD < value] = 0
        cD[cD >= value] = cD[cD >= value] - value
    cH[mask_h] = -cH[mask_h]
    cV[mask_v] = -cV[mask_v]
    cD[mask_d] = -cD[mask_d]
    return cA, (cH, cV, cD)


def Dwt_Erode(image, args):
    level, mode = args
    dst = DWT(image, level, mode, Erode_Filter)
    dst = IDWT(dst, level, mode)
    return dst.clip(0, 255).astype('uint8')


def Dwt_Gauss(image, args):
    level, mode = args
    dst = DWT(image, level, mode, GaussianBur_Filter)
    dst = IDWT(dst, level, mode)
    return dst.clip(0, 255).astype('uint8')


def Dwt_Threshold(image, args):
    level, mode, t, value = args
    dst = DWT(image, level, mode, partial(Threshold_Filter, t, value))
    dst = IDWT(dst, level, mode)
    return dst.clip(0, 255).astype('uint8')


def Dwt_User(image, args):
    level, mode, callback = args  # callback是字符串
    if callback:
        dst = DWT(image, level, mode, eval('User.'+callback))
    else:
        dst = DWT(image, level, mode, None)
    dst = IDWT(dst, level, mode)
    return dst.clip(0, 255).astype('uint8')