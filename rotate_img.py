import cv2
import numpy as np

def rotate_img(imgPath: str, imgName: str, savePath: list):
    image = cv2.imread(imgPath + "/" + imgName)
    imgH, imgW = image.shape[0], image.shape[1]
    rotated_img_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 瞬时针旋转90度
    rotated_img_180 = cv2.rotate(image, cv2.ROTATE_180)
    rotated_img_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)# 逆向时针旋转90度

    cv2.imwrite(savePath[0] + "/" + imgName, rotated_img_90)
    cv2.imwrite(savePath[1] + "/" + imgName, rotated_img_180)
    cv2.imwrite(savePath[2] + "/" + imgName, rotated_img_270)
    return imgW, imgH
