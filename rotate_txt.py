import os
import numpy as np
import cv2


#读取一个文件夹内的所有txt文件
def getAllTxt(txtDirPath: str, resultTxtPath: list):
    imgW, imgH = 4344, 5792
    txt_files = os.listdir(txtDirPath)
    print(txt_files)
    for txt in txt_files:
        f = open(txtDirPath + "/" + txt, "r", encoding='utf-8')
        boxes = f.read().splitlines()
        getRotateTxt(resultTxtPath, txt, imgW, imgH, boxes)

# 按行读取每个txt中的内容,每一行对应一个标注框
def getRotateTxt(savePath: list, txtName: str, imgW, imgH, pos):
    txt90 = open(savePath[0] + "/" + txtName, mode='a')
    txt180 = open(savePath[1] + "/" + txtName, mode='a')
    txt270 = open(savePath[2] + "/" + txtName, mode='a')
    for pos_i in pos:
        pos_i = pos_i.split(' ')
        x_center = float(pos_i[1]) * imgW + 1  # 得到标注框的中心x坐标
        y_center = float(pos_i[2]) * imgH + 1  # 得到标准框的中心y坐标
        # 得到标准框左上角的坐标
        x1 = int(x_center - 0.5 * float(pos_i[3]) * imgW)
        y1 = int(y_center - 0.5 * float(pos_i[4]) * imgH)

        # 得到标准框的右下角坐标
        x4 = int(x_center + 0.5 * float(pos_i[3]) * imgW)
        y4 = int(y_center + 0.5 * float(pos_i[4]) * imgH)

        # 得到标注框的宽高
        w = x4 - x1
        h = y4 - y1

        center_x, center_y, nw, nh = rotate90(imgW, imgH, x1, y1, w, h, x_center, y_center)
        txt90.write(pos_i[0] + " " + str("{:f}".format(center_x)) + " " + str("{:f}".format(center_y)) + " " + str("{:f}".format(nw)) + " " + str("{:f}".format(nh)) + "\n")
        center_x, center_y, nw, nh = rotate180(imgW, imgH, x1, y1, w, h, x_center, y_center)
        txt180.write(pos_i[0] + " " + str("{:f}".format(center_x)) + " " + str("{:f}".format(center_y)) + " " + str("{:f}".format(nw)) + " " + str("{:f}".format(nh)) + "\n")
        center_x, center_y, nw, nh = rotate270(imgW, imgH, x1, y1, w, h, x_center, y_center)
        txt270.write(pos_i[0] + " " + str("{:f}".format(center_x)) + " " + str("{:f}".format(center_y)) + " " + str("{:f}".format(nw)) + " " + str("{:f}".format(nh)) + "\n")

    txt90.close()
    txt180.close()
    txt270.close()

def rotate90(imgW, imgH, x1, y1, w, h, x_center, y_center):
    nx1 = imgH - (h + y1)
    ny1 = x1
    nimgW = imgH
    nimgH = imgW
    nw = h
    nh = w
    nx_center = imgH - y_center
    ny_center = x_center
    center_x = (nx_center - 1) / nimgW
    center_y = (ny_center - 1) / nimgH

    sw = nw / nimgW
    sh = nh / nimgH

    return center_x, center_y, sw, sh


def rotate180(imgW, imgH, x1, y1, w, h, x_center, y_center):
    nx1 = imgW - (w + x1)
    ny1 = imgH - (y1 + h)
    nimgW = imgW
    nimgH = imgH
    nw = w
    nh = h
    nx_center = imgW - x_center
    ny_center = imgH - y_center

    center_x = (nx_center - 1) / nimgW
    center_y = (ny_center - 1) / nimgH

    sw = nw / nimgW
    sh = nh / nimgH

    return center_x, center_y, sw, sh


def rotate270(imgW, imgH, x1, y1, w, h, x_center, y_center):
    nx1 = y1
    ny1 = imgW - (x1 + w)
    nimgW = imgH
    nimgH = imgW
    nw = h
    nh = w
    nx_center = y_center
    ny_center = imgW - x_center

    center_x = (nx_center - 1) / nimgW
    center_y = (ny_center - 1) / nimgH

    sw = nw / nimgW
    sh = nh / nimgH

    return center_x, center_y, sw, sh

