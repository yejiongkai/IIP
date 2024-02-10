import cv2
import numpy as np
from matplotlib import pyplot as plt
from GuidedFilter import GuidedFilter
from mpl_toolkits.mplot3d import Axes3D


def GrayToBGR(b, g, r, coef1, coef2, coef3):
    if b.shape == g.shape == r.shape and len(b.shape) == 2:
        dst = cv2.merge([(b.astype('float') * coef1).clip(0, 255).astype('uint8'),
                         (g.astype('float') * coef2).clip(0, 255).astype('uint8'),
                         (r.astype('float') * coef3).clip(0, 255).astype('uint8')])
        return dst
    return False


def GrayToHSV(h, s, v, coef1, coef2, coef3):
    if h.shape == s.shape == v.shape and len(h.shape) == 2:
        dst = cv2.merge([(h.astype('float') * coef1).clip(0, 255).astype('uint8'),
                         (s.astype('float') * coef2).clip(0, 255).astype('uint8'),
                         (v.astype('float') * coef3).clip(0, 255).astype('uint8')])
        return cv2.cvtColor(dst, cv2.COLOR_HSV2BGR_FULL)
    return False


def GrayToYUV(y, u, v, coef1, coef2, coef3):
    if y.shape == u.shape == v.shape and len(y.shape) == 2:
        dst = cv2.merge([(y.astype('float') * coef1).clip(0, 255).astype('uint8'),
                         (u.astype('float') * coef2).clip(0, 255).astype('uint8'),
                         (v.astype('float') * coef3).clip(0, 255).astype('uint8')])
        return cv2.cvtColor(dst, cv2.COLOR_YUV2BGR)
    return False


def Maximum(image1, image2):
    return np.maximum(image1, image2).astype('uint8')


def Minimum(image1, image2):
    return np.minimum(image1, image2).astype('uint8')


# 两图片相减
def Subtract(image1, image2, coef1, coef2):
    # return (image1.astype('float')*coef1 - image2.astype('float')*coef2).clip(0, 255).astype('uint8')
    return cv2.normalize((image1.astype('float') * coef1 - image2.astype('float') * coef2).clip(0, 255), -1, 0, 255,
                         cv2.NORM_MINMAX).astype('uint8')


def Add(image1, image2, coef1, coef2, mode=0):
    if mode == 0:
        all = coef1 + coef2
        return (coef1 / all * image1.astype('float') + coef2 / all * image2.astype('float')).astype('uint8')
    if mode == 1:
        return (coef1 * image1.astype('float') + coef2 * image2.astype('float')).clip(0, 255).astype('uint8')


# 灰度直方图
def Plot_Demo(image):
    # numpy的ravel函数功能是将多维数组降为一维数组
    fig = plt.figure('直方图')
    plt.hist(image.ravel(), 256, [0, 256])
    plt.show()
    plt.draw()


# 彩色直方图
def image_hist_demo(image):
    color = {"blue", "green", "red"}
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据下标和数据，一般用在 for 循环当中。
    for i, color in enumerate(color):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.show()
    plt.draw()


# 三维图像显示
def Display3D(image, args):
    """

    :param image:
    :param args: ((-1,-1),(-1,-1),1)
    x: 需要查看x坐标范围 ps:(10,20),默认全局
    y: 需要查看y坐标范围 默认全局
    step: 范围每个采点的距离
    :return:
    """
    x, y = None, None
    l = 1 if len(image.shape) == 2 else image.shape[2]
    color = ["blue", "green", "red"] if l > 1 else ['gray']
    for i in range(l):
        if l == 1:
            img = image.copy()
        else:
            img = image[:, :, i].copy()
        if args[0] == (-1, -1) or args[1] == (-1, -1):
            Y = np.arange(0, np.shape(img)[0], args[2])
            X = np.arange(0, np.shape(img)[1], args[2])
            x, y = [0, img.shape[0]], [0, img.shape[1]]

        else:
            Y = np.arange(args[0][0], args[0][1], args[2])
            X = np.arange(args[1][0], args[1][1], args[2])
            x, y = [args[0][0], args[0][1]], [args[1][0], args[1][1]]
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure(num=color[i])
        ax = plt.axes(projection="3d")
        ax.plot_surface(X, Y, img[x[0]:x[1]:args[2], y[0]:y[1]:args[2]], cmap='gist_rainbow')  # cmap='hot'
    plt.show()


def Resize(image, args):
    """
    :param image:
    :param args:
        0 dsize（宽，高）
        1 dst
        2 fx
        3 fy
        4 interpolation
    :return:
    """
    return cv2.resize(image, *args)


# 归一化
def Normalize(image, args):
    """
    :param image:
    :param args:alpha=None, beta=None, norm_type=None, dtype=None, mask=None
    :return:
    """
    dst = image.astype('float')
    return cv2.normalize(dst, -1, *args).astype('uint8')


def LUT(image, args):
    """
    :param image:
    :param args:
        0 [色素区间]
        1 [R的区间]
        2 [G的区间]
        3 [B的区间]
    :return:
    """
    dst = None
    if len(image.shape) > 2:
        dst = image.copy()
    else:
        dst = image.reshape(*image.shape, 1)
        dst = np.tile(dst, (1, 1, 3))
    # R通道上色
    colors = [[], [], []]
    for i in range(1, len(args[0])):
        l = args[0][i] - args[0][i - 1]
        colors[0] += [j * (args[1][i] - args[1][i - 1]) // l + args[1][i - 1] for j in range(0, l)]
        colors[1] += [j * (args[2][i] - args[2][i - 1]) // l + args[2][i - 1] for j in range(0, l)]
        colors[2] += [j * (args[3][i] - args[3][i - 1]) // l + args[3][i - 1] for j in range(0, l)]
    colors = [np.array(color, dtype='uint8') for color in colors]
    dst[:, :, 0] = cv2.LUT(dst[:, :, 0], colors[2])
    dst[:, :, 1] = cv2.LUT(dst[:, :, 1], colors[1])
    dst[:, :, 2] = cv2.LUT(dst[:, :, 2], colors[0])
    return dst


def Capture(image, args):
    """
    :param image:
    :param args:
        0 色素区间
    :return:
    """
    dst = image.copy()
    mark = np.zeros_like(image)
    for left, right in args:
        mark[np.logical_and(image >= left, image <= right)] = 1
    dst[mark != 1] = 0
    dst[mark == 1] = 255
    return dst


def ELA(image, args):
    """
    :param image:
    :param args:
        0 quality
        1 scale
    :return:
    """
    dst = image.copy()
    # dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".jpg", dst, [cv2.IMWRITE_JPEG_QUALITY, args[0]])
    # get it from buffer and decode it to numpy array
    if len(image.shape) == 2:
        compressed_img = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_GRAYSCALE)
    else:
        compressed_img = cv2.imdecode(np.frombuffer(buffer, np.uint8), cv2.IMREAD_COLOR)
    dst = args[1] * (cv2.absdiff(image, compressed_img))
    return dst



