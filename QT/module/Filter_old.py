from HomomorphicFilter import HomomorphicFilter
from GuidedFilter import GuidedFilter
from math import sqrt, tan, pi
import cv2
import numpy as np


# NLM去噪
def NLM(image, args):
    return cv2.fastNlMeansDenoising(image, -1, *args)


# 同态滤波
def HomoFilter(image, args):
    def H(image, YH=1.5, YL=0.5, filter_params=(30, 2), filter='gaussian'):
        hf = HomomorphicFilter(YH, YL)
        return hf.filter(image, filter_params=filter_params, filter=filter)

    return H(image, *args)


# 双边滤波
def BilateralFilter(image, args):
    return cv2.bilateralFilter(image, *args)


# 高斯滤波
def GaussianBlur(image, args):
    return cv2.GaussianBlur(image, *args)


# 均值滤波
def Blur(image, args=(3, 3)):
    return cv2.blur(image, args)


# 中值滤波
def MedianBlur(image, args):
    return cv2.medianBlur(image, args[0])


def LowPassFilter(img, args):
    threshold = args[0]
    img = img.astype(np.float32)

    rows, cols = img.shape
    crow, ccol = int(rows / 2), int(cols / 2)  # 中心位置

    n1, m1 = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    img = cv2.copyMakeBorder(img, 0, n1 - rows, 0, m1 - cols, cv2.BORDER_CONSTANT)

    dft = cv2.dft(img, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)
    dft = cv2.magnitude(dft[:, :, 0], dft[:, :, 1])
    ph = cv2.phase(dft[:, :, 0], dft[:, :, 1])
    dft_shift = np.fft.fftshift(dft)

    mask = np.zeros((rows, cols, 2), np.uint8)
    for i in range(crow - threshold, crow + threshold):
        for j in range(ccol - threshold, ccol + threshold):
            if sqrt((i - crow) ** 2 + (j - ccol)**2) < threshold:
                mask[i, j] = 1

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    dst = cv2.idft(cv2.polarToCart(f_ishift, ph), flags=cv2.DFT_INVERSE | cv2.DFT_REAL_OUTPUT)
    # dst = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1]).clip(0, 255)

    return dst.astype("uint8")


def HighPassFilter(img, args):
    threshold = args[0]
    w = args[1]
    img = img.astype(np.float32)

    rows, cols = img.shape
    crow, ccol = int(rows / 2), int(cols / 2)  # 中心位置

    dft = cv2.dft(img, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)
    ph = cv2.phase(dft[:, :, 0], dft[:, :, 1])
    mag = cv2.magnitude(dft[:, :, 0], dft[:, :, 1])
    dft_shift = np.fft.fftshift(mag)
    mask = np.ones((rows, cols), np.float32) * 1.0 if w is None else w
    for i in range(crow - threshold, crow + threshold):
        for j in range(ccol - threshold, ccol + threshold):
            if sqrt((i - crow) ** 2 + (j - ccol) ** 2) < threshold:
                mask[i, j] = 0
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    dst = cv2.idft(cv2.merge(cv2.polarToCart(f_ishift, ph)), flags=cv2.DFT_INVERSE | cv2.DFT_REAL_OUTPUT).clip(0, 255)
    return dst.astype("uint8")


def IdealBandFilter(image, args):
    """
    :param image:
    :param args:
    0 W
    1 D0
    2 type:
        0:Pass 带通
        1:Stop 带阻
    :return:
    """
    width, height = image.shape
    dst = np.fft.fftshift(np.fft.fft2(image))
    cur = np.zeros_like(dst)
    for i in np.arange(width):
        for j in np.arange(height):
            distance = np.sqrt((i - width / 2) ** 2 + (j - height / 2) ** 2)
            if (args[1] - args[0] / 2) <= distance <= (args[1] + args[0] / 2):
                cur[i, j] = 1
            else:
                cur[i, j] = 0

    if args[2] == 1:
        cur = 1 - cur
    dst *= cur
    s = np.fft.ifftshift(dst)
    return np.real(np.fft.ifft2(s)).astype('uint8')


def ButterworthBandFilter(image, args):
    """
    :param image:
    :param args:
    0 Radius
    1 N
    2 type:
        0:Pass 带通
        1:Stop 带阻
    :return:
    """
    width, height = image.shape
    dst = np.fft.fftshift(np.fft.fft2(image))
    cur = np.zeros_like(dst)
    for i in np.arange(width):
        for j in np.arange(height):
            distance = np.sqrt((i - width / 2) ** 2 + (j - height / 2) ** 2)
            cur[i, j] = 1 / (1 + (distance / args[0]) ** (2 * args[1]))
    if args[2] == 1:
        cur = 1 - cur
    dst *= cur
    s = np.fft.ifftshift(dst)
    return np.real(np.fft.ifft2(s)).astype('uint8')


def GaussianBandFilter(image, args):
    """
    :param image:
    :param args:
    0 Radius
    1 type:
        0:Pass 带通
        1:Stop 带阻
    :return:
    """
    sigma = args[0]
    height, width = image.shape
    dst = np.fft.fftshift(np.fft.fft2(image))
    x, y = np.meshgrid(np.arange(height), np.arange(width))

    # 计算距离中心点的平方距离
    distance = (x - height//2) ** 2 + (y - width//2) ** 2

    # 根据高斯函数的定义计算模板
    mask = np.exp(-distance / (2 * sigma ** 2))
    dst *= mask
    s = np.fft.ifftshift(dst)
    return np.real(np.fft.ifft2(s)).astype('uint8')


def MatchFilter(image, args):
    """
    :param image:
    :param args:
        0 L 长度
        1 (start,end,step) 角度从start开始到end结束 以step为间隔
        2 sigma
        3 coef
    :return:
    """

    def build_filters2(sigma=1, YLength=10, coef=3):
        filters = []
        widthOfTheKernel = np.ceil(np.sqrt((6 * np.ceil(sigma) + 1) ** 2 + YLength ** 2))  # 获取核的宽度
        if np.mod(widthOfTheKernel, 2) == 0:
            widthOfTheKernel = widthOfTheKernel + 1
        widthOfTheKernel = int(widthOfTheKernel)
        # print(widthOfTheKernel)
        for thetas in np.arange(*args[1]):
            theta = thetas / 180 * np.pi
            # theta = np.pi/4
            matchFilterKernel = np.zeros((widthOfTheKernel, widthOfTheKernel), dtype=np.float)  # 构建卷积核
            for x in range(widthOfTheKernel):  # 这里面的循环是为了获取对应角度的匹配滤波核
                for y in range(widthOfTheKernel):
                    halfLength = (widthOfTheKernel - 1) / 2  # 将卷积核的中间位置作为零点
                    x_ = (x - halfLength) * np.cos(theta) + (y - halfLength) * np.sin(theta)  # 将图像旋转对应角度
                    y_ = -(x - halfLength) * np.sin(theta) + (y - halfLength) * np.cos(theta)
                    if abs(x_) > coef * np.ceil(sigma):  # 这里有筛选
                        matchFilterKernel[x][y] = 0
                    elif abs(y_) > (YLength - 1) / 2:
                        matchFilterKernel[x][y] = 0
                    else:
                        matchFilterKernel[x][y] = -np.exp(-.5 * (x_ / sigma) ** 2) / (np.sqrt(2 * np.pi) * sigma)
            m = 0.0
            for i in range(matchFilterKernel.shape[0]):
                for j in range(matchFilterKernel.shape[1]):
                    if matchFilterKernel[i][j] < 0:
                        m = m + 1
            mean = np.sum(matchFilterKernel) / m  # 负的
            for i in range(matchFilterKernel.shape[0]):
                for j in range(matchFilterKernel.shape[1]):
                    if matchFilterKernel[i][j] < 0:
                        matchFilterKernel[i][j] = matchFilterKernel[i][j] - mean
            # matchFilterKernel = matchFilterKernel[matchFilterKernel.any(axis=1), :]
            # matchFilterKernel = matchFilterKernel[:, matchFilterKernel.any(axis=0)]
            # print(matchFilterKernel)
            # import matplotlib.pyplot as plt
            # plt.plot(matchFilterKernel)
            # plt.show()
            filters.append(matchFilterKernel)

        return filters

    def process(img, filters):
        accum = np.zeros_like(img)
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8U, kern, borderType=cv2.BORDER_REPLICATE)
            np.maximum(accum, fimg, accum)
        return accum

    filters = build_filters2(args[2], args[0], args[3])
    dst = process(image, filters)
    return dst


def MinFilter(img, args):
    K_size = args[0]
    H, W = img.shape
    pad = K_size // 2  # 使滤波器中心能与图像边缘对齐
    out = np.zeros((H + 2 * pad, W + 2 * pad))
    out[pad:pad + H, pad:pad + W] = img.copy()

    tem = out.copy()

    # 进行滤波
    for x in range(H):
        for y in range(W):
            out[x + pad, y + pad] = np.min(tem[x:x + K_size, y:y + K_size])

    return out.astype('uint8')


def MaxFilter(img, args):
    K_size = args[0]
    H, W = img.shape
    pad = K_size // 2  # 使滤波器中心能与图像边缘对齐
    out = np.zeros((H + 2 * pad, W + 2 * pad))
    out[pad:pad + H, pad:pad + W] = img.copy()

    tem = out.copy()

    # 进行滤波
    for x in range(H):
        for y in range(W):
            out[x + pad, y + pad] = np.max(tem[x:x + K_size, y:y + K_size])

    return out.astype('uint8')


# 均值平移
def MeanShiftFilter(image, args):
    dst = np.tile(image.reshape(*image.shape, 1), 3)
    return cv2.pyrMeanShiftFiltering(dst, *args)[:, :, 0]


# 漫水填充
def FloodFill(image, args):
    dst = image.copy()
    width, height = dst.shape[0] + 2, dst.shape[1] + 2
    mask = np.zeros((width, height), dtype='uint8')
    cv2.floodFill(dst, mask, *args)
    return dst


# 指导性滤波
def GuideFilter(image, args):
    guide = GuidedFilter(image, *args)
    return guide.t
