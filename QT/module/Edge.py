import cv2
import numpy as np


# Hough直线检测
def HoughLine(image, args):
    """
    :param image:
    :param args:
        0 size 窗口尺寸
        1 color
        2 线段粗细 1/2/3
        后面都是cv2.HoughLinesP的参数
    :return:
    """
    width, height = image.shape
    size = args[0]
    dst = image.copy()
    for i in range(0, width - size, size):
        for j in range(0, height - size, size):
            img_region_ij = image[i:i + size, j:j + size]  # 提取 小窗口内图像
            lines = cv2.HoughLinesP(img_region_ij, *args[3:])  # 1, np.pi / 180, 5, minLineLength=5, maxLineGap=5
            if (lines is None) or (len(lines) == 0):
                continue  # 小窗口内无直线，继续到下一个窗口
            else:
                for x1, y1, x2, y2 in lines[0]:
                    cv2.line(dst, (i + x1, j + y1), (i + x2, j + y2), args[1], args[2])
    return dst


# 二阶拉普拉斯算子
def Laplacian(image, args):
    return cv2.Laplacian(image, -1, *args)


# Gabor算子
def Gabor(image, args):
    """
    :param image:
    :param args
        0（核长度范围，长度间隔）
        1（核角度范围，角度间隔）
        2 sigma(标准差)
        3 lambd(波长)
        4: gamma, psi=None, ktype=None

    :return:
    """

    # Gabor特征提取
    def getGabor(img, filters):
        accum = np.zeros_like(img)  # 滤波结果
        for filter in filters:
            for kern in filter:
                fimg = cv2.filter2D(img, cv2.CV_8UC1, kern)
                accum += fimg
        accum = accum / accum.max() * 255
        accum = np.clip(accum.astype(np.uint8), 0, 255)
        return accum

    filters = []
    ksize = [l for l in range(args[0][0], args[0][1], args[0][2])]
    lamda = args[3]  # 波长
    for theta in np.arange(args[1][0] / 180 * np.pi, args[1][1] / 180 * np.pi, args[1][2] / 180 * np.pi):
        filters.append([])
        for K in range(len(ksize)):
            kern = cv2.getGaborKernel((ksize[K], ksize[K]), args[2], theta, lamda, *args[4:])
            kern /= np.sum(np.abs(kern))
            filters[-1].append(kern)
    return getGabor(image, filters)

# Robert算子
def Robert(Image):
    # 图像的高，宽
    Kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
    Kernely = np.array([[0, -1], [1, 0]], dtype=int)

    x = cv2.filter2D(Image, -1, Kernelx)
    y = cv2.filter2D(Image, -1, Kernely)

    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Roberts


def Prewitt(Image):
    kernelx = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    kernely = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])

    x = cv2.filter2D(Image, -1, kernelx)
    y = cv2.filter2D(Image, -1, kernely)

    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Prewitt = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Prewitt


def Sobel(image, arg):
    return cv2.Sobel(image, *arg)


# 自定义算子
def UserDefined(image, args):
    return cv2.filter2D(image, -1, args)


# Canny滤波
def Canny(image, args):
    return cv2.Canny(image, *args)


# Canny滤波
def USM(image, args):
    alpha, beta, gamma, sigma = args[0], args[1], args[2], args[3]
    g_img = cv2.GaussianBlur(image, (0, 0), sigma)
    dst = cv2.addWeighted(image, alpha, g_img, beta, gamma)
    return dst