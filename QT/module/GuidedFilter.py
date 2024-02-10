import cv2
import numpy as np
import math
from Morphology_old import *

class GuidedFilter:
    def __init__(self, im, ksize, gsize, nums=1000, omega=0.95, eps=0.0001):
        img = im.copy()
        img = img.reshape(*img.shape,1)
        img = np.tile(img, (1,1,3))
        I = img.astype('float64') / 255
        dark = self.DarkChannel(I, ksize)
        A = self.AtmLight(I, dark, nums)
        te = self.TransmissionEstimate(I, A, ksize, omega)  # 这一步获取的是粗透射率
        self.t = self.TransmissionRefine(img, te, gsize, eps)

    #获得暗通道
    def DarkChannel(self, img, ksize):
        b, g, r = cv2.split(img)
        dc = cv2.min(cv2.min(r, g), b)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
        dark = cv2.erode(dc, kernel)
        dark = DILATE(dark, ('Line', (7,8,2), (0,180,15), None))
        return dark

    def AtmLight(self, img, dark, nums=1000):
        [h, w, _] = np.shape(img)
        imsz = h * w  # 获取全部像素个数
        numpx = int(max(math.floor(imsz / nums), 1))  # 获取imsz//1000个像素点
        darkvec = np.reshape(dark, (imsz, 1))         # 将暗通道降维成1维
        imvec = np.reshape(img, (imsz, 3))            # 将图像降维成1维
        indi = darkvec.argsort(axis=0)
        indi = indi[imsz - numpx::]                   # 获得暗通道前imsz//1000个最大像素值（这里是倒着取值）
        atmsum = np.zeros([1, 3])
        for ind in range(1, numpx):
            atmsum = atmsum + imvec[indi[ind]]        # 根据暗通道获得图像imsz//1000个像素值的和
        A = atmsum / numpx
        return A

    #求解粗透射率
    def TransmissionEstimate(self, img, A, ksize, omega=0.95):
        omega = omega
        im3 = np.empty(img.shape, img.dtype)

        for ind in range(0, 3):
            im3[:, :, ind] = img[:, :, ind] / A[0, ind]

        transmission = omega * self.DarkChannel(im3, ksize)
        return transmission

    #细化透射率
    def TransmissionRefine(self, img, et, gsize, eps=0.0001):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float64(gray) / 255
        r = gsize  # radius of filter
        eps = eps  # regularization parameter
        t = self.Guidedfilter(gray, et, r, eps)
        return t

    def Guidedfilter(self, img, p, r, eps):
        # 先均值滤波, 为了下面协方差的计算做准备, 之所以用均值滤波是为了提高运行效率
        mean_I = cv2.boxFilter(img, cv2.CV_64F, (r, r))
        mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
        mean_Ip = cv2.boxFilter(img * p, cv2.CV_64F, (r, r))

        # 计算 I和p 的协方差
        cov_Ip = mean_Ip - mean_I * mean_p
        mean_II = cv2.boxFilter(img * img, cv2.CV_64F, (r, r))

        var_I = mean_II - mean_I * mean_I
        a = cov_Ip / (var_I + eps)
        b = mean_p - a * mean_I

        mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
        mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))
        q = mean_a * img + mean_b
        return (q * 255).clip(0, 255).astype('uint8')
