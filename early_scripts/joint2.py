import numpy as np
import cv2
import sys
import os
import geopy.distance
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import math


# 解析gpfpd消息
def parse_gpfpd(gpfpdfile):
    with open(gpfpdfile, 'r') as f:
        dic1 = []
        dic1.append(-1)
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


# 根据惯导经纬度及姿态角推算出相机经纬度,direction为相机与惯导连线与惯导y轴夹角（逆时针为正方向）
def get_distance_point(Gpfpd, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    cam_pos = np.zeros([len(Gpfpd),2])
    for ipos in range(1,len(Gpfpd)):
        lat = float(Gpfpd[ipos][6])
        lon = float(Gpfpd[ipos][7])
        start = geopy.Point(lat, lon)
        dire = float(gpfpd[ipos][3]) - direction
        d = geopy.distance.VincentyDistance(meters=distance)
        dst = d.destination(point=start, bearing=dire)
        cam_pos[ipos][0] = dst.latitude
        cam_pos[ipos][1] = dst.longitude
    return cam_pos


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
    for index_i in range(y, y + h):
        for index_j in range(x, x + w):
            if (img1[index_i][index_j][0] <= 20) and (img1[index_i][index_j][1] <= 20) and (img1[index_i][index_j][2] <= 20):
                img1[index_i][index_j] = img2[index_i - y][index_j - x]
    return img1


if __name__ == "__main__":
    start_index = 243
    end_index = 1200
    gpfpd = parse_gpfpd("0718/txt/photos15.txt")
    camPos = get_distance_point(gpfpd, pow(pow(0.4, 2) + pow(9, 2), 0.5), math.atan2(0.4, 9) * 180 / math.pi)  #
    print(camPos[0],camPos[1],camPos[6],camPos[7])
    distance = np.zeros(len(gpfpd))
    degree = np.zeros(len(gpfpd))

    for i in range(start_index, end_index):
        if i > start_index:
            level_distance = geodesic((camPos[i-1][0], camPos[i-1][1]), (camPos[i][0], camPos[i][1])).m #跟据经纬度求解两点之间的距离
            distance[i] = level_distance
            degree[i] = getDegree(float(camPos[i-1][0]),float(camPos[i-1][1]),float(camPos[i][0]),float(camPos[i][1]))

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


    # 图片拼接
    a = 20  # 定义底板的高的系数
    b = 10  # 定义底板的宽的系数
    temp = np.zeros([480*a, 640*b, 3])  # 定义拼接图像的底板
    Img = cv2.imread("0718/photos15_rotated/" + str(start_index + 1) + ".jpg")
    paste_photo(temp, Img, 640, 480*a - 1500)
    # cv2.imwrite("r1.jpg",temp)
    last_x = 640
    last_y = 1500
    for j in range(start_index + 1, end_index):
        print(distance[j],degree[j],gpfpd[j-1][3])
        Img = cv2.imread("0718/photos15_rotated/" + str(j) + ".jpg")
        paste_photo(temp, Img, last_x + int(distance[j] * math.sin((degree[j] - float(gpfpd[start_index][3])) * math.pi /180) * 100*1),480*a - (last_y + int(distance[j] * math.cos((degree[j] - float(gpfpd[start_index][3])) * math.pi /180) * 100*1)))
        last_x = last_x + int(distance[j] * math.sin((degree[j] - float(gpfpd[start_index][3])) * math.pi /180) * 100*1)
        last_y = last_y + int(distance[j] * math.cos((degree[j] - float(gpfpd[start_index][3])) * math.pi /180) * 100*1)
    # cv2.namedWindow("joint",0)
    # cv2.imshow("joint",temp)
    # cv2.waitKey(0)
    cv2.imwrite("0718/result/joint13.jpg",temp)

