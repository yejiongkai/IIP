from math import sqrt, tan, pi
import cv2
import numpy as np


def GaussNoise(image, args):
    """
        添加高斯噪声
       :param image: 输入的图像
       :param args: mean  sigma
       """
    mean = args[0]
    sigma = args[1]
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, sigma, image.shape)
    gauss_noise = image + noise
    gauss_noise = np.clip(gauss_noise, 0, 1.0)
    gauss_noise = np.uint8(gauss_noise * 255)
    return gauss_noise
