import numpy as np
import cv2
import sys
import os
from geopy.distance import geodesic
from PIL import Image
import matplotlib.pyplot as plt
import math

# 解析gpfpd消息
def parse_gpfpd(gpfpdfile):
    with open(gpfpdfile, 'r') as f:
        dic1 = []
        dic2 = []
        for line in f.readlines():
            line = line.strip('\n')
            # 去掉换行符\n
            b = line.split(',')
            # 将每一行以逗号为分隔符转换成列表
            dic1.append(b)
            #print(b)
        # for i in range(len(dic1)):
        #     if i%2 == 0:
        #         dic2.append(dic1[i])
    return dic1

# 根据两个点的经纬度求解方位角
def getDegree(latA, lonA, latB, lonB):
    radLatA = math.radians(latA)
    radLonA = math.radians(lonA)
    radLatB = math.radians(latB)
    radLonB = math.radians(lonB)
    dLon = radLonB - radLonA
    y = math.sin(dLon) * math.cos(radLatB)
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(radLatB) * math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    brng = (brng + 360) % 360
    return brng


# 找出车道线在图片中的斜率，b,g,r为车道线颜色的阈值
# def find_k(filename,pb,pg,pr):
#     photo_temp = np.array(cv2.imread(filename))
#     photo_shape = np.array(photo_temp.shape)
#     print(photo_shape[1])
#     point_x_y = np.zeros([20,2])#存储求取斜率的点的坐标
#     point_count = 0
#     for i in range(0,photo_shape[0],60):
#         for j in range(0,photo_shape[1]-4):
#             if (photo_temp[i][j][0] >= pb) and (photo_temp[i][j][1] >= pg) and (photo_temp[i][j][2] >= pr) and \
#                (photo_temp[i][j+2][0] >= pb) and (photo_temp[i][j+2][1] >= pg) and (photo_temp[i][j+2][2] >= pr) and \
#                (photo_temp[i][j+4][0] >= pb) and (photo_temp[i][j+4][1] >= pg) and (photo_temp[i][j+4][2] >= pr): #增加判断条件，减少判断错误的情况
#                 point_x_y[point_count][0] = i #存储横坐标
#                 point_x_y[point_count][1] = j  #存储纵坐标
#                 print(point_x_y[point_count][0],point_x_y[point_count][1])
#                 point_count = point_count + 1
#                 break


# 在指定区域找出黑色点并替换为另一张图片的像素值并进行缝隙的修复,(x1,y1)和(x2,y2)分别为一个矩形区域左上角和右下角的的坐标
def replace_black(img1, img2, x1, y1, x2, y2):
    crack_start = 0  # 定义一个裂缝标记变量，标记裂缝是否已经过处理
    for i in range(y1, y2):
        for j in range(x1, x2):
            if (img1[i][j][0] <= 12) and (img1[i][j][1] <= 12) and (img1[i][j][2] <= 12) and (crack_start <= 660):  # 判断此处像素点是黑点的阈值设置
                # if crack_start == 0:  # 填充裂缝
                #     for s in range(1, 4):
                #         img1[i][j - s][0] = img2[i][j - s][0]
                #         img1[i][j - s][1] = img2[i][j - s][1]
                #         img1[i][j - s][2] = img2[i][j - s][2]
                #     crack_start = 1
                img1[i][j - 1][0] = img2[i][j - 1][0]
                img1[i][j - 1][1] = img2[i][j - 1][1]
                img1[i][j - 1][2] = img2[i][j - 1][2]
                img1[i][j - 2][0] = img2[i][j - 2][0]
                img1[i][j - 2][1] = img2[i][j - 2][1]
                img1[i][j - 2][2] = img2[i][j - 2][2]
            if (img1[i][j][0] <= 6) and (img1[i][j][1] <= 6) and (img1[i][j][2] <= 6):
                img1[i][j][0] = img2[i][j][0]
                img1[i][j][1] = img2[i][j][1]
                img1[i][j][2] = img2[i][j][2]
        crack_start = crack_start + 1
    return img1


# 将img2粘贴到img1的x,y位置
def paste_photo(img1, img2, x, y):
    h, w, ch = img2.shape
    for i in range(y, y + h):
        for j in range(x, x + w):
            img1[i][j] = img2[i - y][j - x]
    return img1


if __name__ == "__main__":
    start_index = 243
    end_index = 920
    gpfpd = parse_gpfpd("0718/txt/photos15.txt")

    # print(gpfpd)
    # print(len(gpfpd))
    # print(gpfpd[0][6],gpfpd[0][7])
    # 每一个列表的第7,8,两个元素是经纬度
    # level_distance = geodesic((gpfpd[185][6], gpfpd[185][7]), (gpfpd[186][6], gpfpd[186][7])).m
    # vertical_distance = float(gpfpd[186][8]) - float(gpfpd[185][8])
    # 计算两个位置的高度差
    # true_distance = pow((pow(level_distance,2)+pow(vertical_distance,2)),0.5)
    # print(level_distance)
    # print(true_distance)
    # print(gpfpd[0][3])
    distance = np.zeros(len(gpfpd))

    for i in range(start_index, end_index):
        level_distance = geodesic((gpfpd[i-1][6], gpfpd[i-1][7]), (gpfpd[i][6], gpfpd[i][7])).m #跟据经纬度求解两点之间的距离
        distance[i] = level_distance
        # print(distance[i])

    # img_dir = "0718/photos15_warped/"
    # rotated_dir = "0718/photos15_rotated/"
    # imgName_tail = ".jpg"
    # # 设置图片从起始序号读取图片并进行旋转
    # for i in range(start_index, end_index):
    #     img = cv2.imread(img_dir + str(i) + imgName_tail)
    #     rows, cols, chanel = img.shape
    #     print(rows, cols)
    #     rotate_angle = float(gpfpd[start_index][3])-float(gpfpd[i][3])
    #     print(rotate_angle)
    #     M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), rotate_angle, 1)
    #     dst = cv2.warpAffine(img, M, (cols, rows))
    #     cv2.imwrite(rotated_dir + str(i) + imgName_tail, dst)

    # 将图片以第一张图片为基准转正
    # for i in range(start_index, end_index):
    #     img = cv2.imread(rotated_dir + str(i) + imgName_tail)
    #     rows, cols, chanel = img.shape
    #     print(rows, cols)
    #     rotate_angle = 2
    #     print(rotate_angle)
    #     M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), rotate_angle, 1)
    #     dst = cv2.warpAffine(img, M, (cols, rows))
    #     cv2.imwrite("photo7_rotated_vertical/" + str(i) + imgName_tail, dst)

    # find_k("rotated_photos/187.jpg",172,172,172)
    # show = cv2.imread("rotated_photos/187.jpg")
    # print(show.shape)
    # for i in range(0,len(show[1])):
    #     print(i)
    #     print(show[660][i])

    # 图片拼接
    a = 30  # 定义底板的高的系数
    b = 15  # 定义底板的宽的系数
    a_offset = 640
    b_offset = 500
    temp = np.zeros([480*a, 640*b, 3])  # 定义拼接图像的底板
    cv2.imwrite("temps/temp2.jpg", temp)
    toImg = Image.open("temps/temp2.jpg")
    # cv2.imwrite("opr/lastImg.jpg", temp)
    ## finalImg = Image.open("temps/temp1.jpg")
    ## last_posA = 7200 - a_offset
    ## last_posB = b_offset
    for j in range(start_index, end_index):
        fromImg = Image.open("0718/photos15_rotated/" + str(j) + ".jpg")

        ## lastImg = toImg
        ## lastImg_cv = np.asanyarray(lastImg)
        ## lastImg_cv.flags.writeable = True
        # lastImg_cv = cv2.imread("opr/lastImg.jpg")
        toImg.paste(fromImg, (b_offset + int(distance[j]*math.sin(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1), 480*a - (a_offset + int(distance[j]*math.cos(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1))))
        ## toImg_cv = np.asanyarray(toImg)
        ## toImg_cv.flags.writeable = True

        # toImg.save("opr/toImg.jpg")
        # toImg_cv = cv2.imread("opr/toImg.jpg")
        # if j != start_index:
        #     toImg_cv = replace_black(toImg_cv, lastImg_cv, b_offset + int(distance[j]*math.sin(float(gpfpd[j-1][3]) - float(gpfpd[j][3]))*100*0.2), last_posA, \
        #                              1280 + last_posB, 720*a - (a_offset + int(distance[j]*math.cos(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1.2)) + 720)
        #     cv2.imwrite("opr/toImg.jpg", toImg_cv)
        #     toImg = Image.open("opr/toImg.jpg")
            ## for k in range(last_posA, 720*a - (a_offset + int(distance[j]*math.cos(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*0.7 )) + 720):
            ##     for l in range(b_offset + int(distance[j]*math.sin(float(gpfpd[j-1][3]) - float(gpfpd[j][3]))*100*0.1), 1280 + last_posB):
            ##         toImg_cv[k][l] = lastImg_cv[k][l]
        # last_posB = b_offset + int(distance[j]*math.sin(float(gpfpd[j-1][3]) - float(gpfpd[j][3]))*100*0.2)
        # last_posA = 720*a - (a_offset + int(distance[j]*math.cos(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1.2))

        ## toImg.save("src/src2.jpg")
        ## toImg = Image.open("temps/temp1.jpg")
        ## src2 = cv2.imread("src/src2.jpg")
        ## src1 = cv2.imread("temps/temp1.jpg")
        ## src1 = cv2.addWeighted(src1, 0.7, src2, 0.3, 0)
        ## toImg = Image.open("temps/temp1.jpg")

        b_offset = b_offset + int(distance[j]*math.sin(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1)
        a_offset = a_offset + int(distance[j]*math.cos(float(gpfpd[j][3]) - float(gpfpd[j-1][3]))*100*1)

        ## toImg = Image.fromarray(np.uint8(toImg_cv))
        # toImg.save("opr/lastImg.jpg")

    toImg.save("0718/result/joint1.jpg")
    ## cv2.imwrite("finalImg/final.jpg",src2)
    ## finalImg = Image.open("finalImg/final.jpg")
    ## finalImg.save("result/joint21.jpg")













