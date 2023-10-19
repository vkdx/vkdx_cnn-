import os
import cv2
import shutil

from DataAugmentation.noise import pepperNoise, gaussianNoise
from DataAugmentation.rotate_img import rotate_img
from DataAugmentation.rotate_txt import getRotateTxt


def getDirFilesSort(dirPath: str, fileClass: str, isSort: bool, isAbPath: bool) -> list:
    filesList = []
    for filename in os.listdir(dirPath):
        if filename.endswith(fileClass):
            # print(filename)
            filesList.append(filename)  # 得到图片名称
    if isSort:
        filesList.sort(key=lambda x: int(x[:-4]))  # 提取.jpg前面地图片名称转换为int类型进行升序排列

    if isAbPath:
        # 添加完整的图像路径
        for i in range(len(filesList)):
            filesList[i] = dirPath + "/" + filesList[i]

    return filesList


def merge(imgNameList, txtNameList, allImgDir, allTxtDir):
    i = 0
    for imgName in imgNameList:
        print("\033[1;32m Image merging:\033[0m \033[1;35m{0}\033[0m \033[1;36m{1}.jpg\033[0m".format(imgName, i))
        img = cv2.imread(imgName)
        cv2.imwrite(allImgDir + "/" + str(i) + ".jpg", img)
        i = i + 1

    i = 0
    for txtName in txtNameList:
        print("\033[1;32m Txt merging:\033[0m \033[1;35m{0}\033[0m \033[1;36m{1}.txt\033[0m".format(txtName, i))
        shutil.copy(txtName, allTxtDir + "/" + str(i) + ".txt")
        i = i + 1


def addNoise(allImgList: list, allTxtList: list, l: int, imgSavePath, txtSavePath):
    i = 0
    for img, txt in zip(allImgList, allTxtList):
        pepperNoise(img, imgSavePath, l + i)
        shutil.copy(txt, txtSavePath + "/" + str(l + i) + ".txt")
        print("\033[1;32m Pepper noise:\033[0m \033[1;35m{0} {1}\033[0m \033[1;36m{2}.jpg {3}.txt\033[0m".format(img, txt, l+i, l+i))
        i = i + 1

    l = l + i
    i = 0
    for img, txt in zip(allImgList, allTxtList):
        gaussianNoise(img, imgSavePath, l + i)
        shutil.copy(txt, txtSavePath + "/" + str(l + i) + ".txt")
        print("\033[1;32m Gaussian noise:\033[0m \033[1;35m{0} {1}\033[0m \033[1;36m{2}.jpg {3}.txt\033[0m".format(img, txt, l+i, l+i))
        i = i + 1

if __name__ == '__main__':
    originImgDir = "datasets/img" #原始图像数据文件夹
    originTxtDir = "datasets/txt" #原始图像数据标注txt文件

    #三种旋转方式图像保存文件
    rotateImgDirList = ["datasets/90/img", "datasets/180/img", "datasets/270/img"]
    rotateTxtDirList = ["datasets/90/txt", "datasets/180/txt", "datasets/270/txt"]

    #最终图像数据保存文文件夹
    allImgDir = "datasets/allDataSets/img"
    allTxtDir = "datasets/allDataSets/txt"

    for imgDir, txtDir in zip(rotateImgDirList, rotateTxtDirList):
        if not os.path.exists(imgDir):
            os.makedirs(imgDir)
        if not os.path.exists(txtDir):
            os.makedirs(txtDir)

    if not os.path.exists(allImgDir):
        os.makedirs(allImgDir)
    if not os.path.exists(allTxtDir):
        os.makedirs(allTxtDir)

    oriImgNameList = getDirFilesSort(originImgDir, ".jpg", True, False)
    oriTxtNameList = getDirFilesSort(originTxtDir, ".txt", True, False)

    if len(oriImgNameList) != len(oriTxtNameList):
        print("\033[1;31m The number of images does not match the number of txt files! \033[0m")
    else:

        print("\033[1;34m Image number is:{} \033[0m".format(len(oriImgNameList)))
        print("\033[1;34m Start rotation! \033[0m")
        for img, txt in zip(oriImgNameList, oriTxtNameList):
            if img[:-4] != txt[:-4]:
                print("\033[1;31m Error! \033[0m")
            else:
                print("\033[1;32m Rotating:\033[0m \033[1;35m{0}\033[0m \033[1;36m{1}\033[0m".format(img, txt))
                imgW, imgH = rotate_img(originImgDir, img, rotateImgDirList)
                f = open(originTxtDir + "/" + txt, "r", encoding='utf-8')
                boxes = f.read().splitlines()
                getRotateTxt(rotateTxtDirList, txt, imgW, imgH, boxes)
        print("\033[1;34m Rotate end! \033[0m")

        print("\033[1;34m Start merging! \033[0m")

        oriImgNameList = getDirFilesSort(originImgDir, ".jpg", True, True)
        oriTxtNameList = getDirFilesSort(originTxtDir, ".txt", True, True)

        rot90_ImgNameList = getDirFilesSort(rotateImgDirList[0], ".jpg", True, True)
        rot180_ImgNameList = getDirFilesSort(rotateImgDirList[1], ".jpg", True, True)
        rot270_ImgNameList = getDirFilesSort(rotateImgDirList[2], ".jpg", True, True)

        rot90_TxtNameList = getDirFilesSort(rotateTxtDirList[0], ".txt", True, True)
        rot180_TxtNameList = getDirFilesSort(rotateTxtDirList[1], ".txt", True, True)
        rot270_TxtNameList = getDirFilesSort(rotateTxtDirList[2], ".txt", True, True)

        allImgList = oriImgNameList + rot90_ImgNameList + rot180_ImgNameList + rot270_ImgNameList
        allTxtList = oriTxtNameList + rot90_TxtNameList + rot180_TxtNameList + rot270_TxtNameList

        merge(allImgList, allTxtList, allImgDir, allTxtDir)
        print("\033[1;34m Merge ended! \033[0m")

        print("\033[1;34m Start adding noise! \033[0m")
        allImgList = getDirFilesSort(allImgDir, ".jpg", True, True)
        allTxtList = getDirFilesSort(allTxtDir, ".txt", True, True)

        lenImgList = len(allImgList)
        lenTxtList = len(allTxtList)
        if lenImgList != lenTxtList:
            print("\033[1;31m The number of images does not match the number of txt files! \033[0m")
        else:
            addNoise(allImgList, allTxtList, lenImgList, allImgDir, allTxtDir)
        print("\033[1;34m End of noise addition! \033[0m")