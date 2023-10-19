import cv2
import numpy as np

def pepperNoise(imgName, savePath, number):
    prob = 0.02
    image = cv2.imread(imgName)
    salt = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.rand()
            if rdn < prob:
                salt[i][j] = 0
            elif rdn > thres:
                salt[i][j] = 255
            else:
                salt[i][j] = image[i][j]

    cv2.imwrite(savePath + "/" + str(number) + ".jpg", salt)


def gaussianNoise(imgName, savePath, number):
    mu = 0.1 #均值
    sigma = 0.08 #标准差
    img = cv2.imread(imgName)

    image = np.array(img / 255, dtype=float)
    noise = np.random.normal(mu, sigma, image.shape)
    gauss_noise = image + noise
    if gauss_noise.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    gauss_noise = np.clip(gauss_noise, low_clip, 1.0)
    gauss_noise = np.uint8(gauss_noise * 255)
    cv2.imwrite(savePath + "/" + str(number) + ".jpg", gauss_noise)



