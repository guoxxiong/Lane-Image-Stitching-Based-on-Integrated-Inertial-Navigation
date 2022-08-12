import numpy as np
import sys
import os
import math
import time

lane_center = 'XY_AXIS/center1.txt'
picture_axis = 'XY_AXIS/picture_axis.txt'

# 返回类型为[[编号]，[坐标]]形式
def parse_lane_center(lane_center_file):
    with open(lane_center_file, 'r') as f:
        dic = []
        for line in f.readlines():
            line = line.strip('\n')
            b = line.split(' ')   # 将每一行以' '为分隔符转换成列表
            b.pop(-1)
            dic.append(b)
    return  dic

# 返回类型为[[编号]，[坐标]]形式
def parse_picture_axis(picture_axis_file):
    with open(picture_axis_file, 'r') as f:
        dic = []
        dic.append([-1])
        for line in f.readlines():
            line = line.strip('\n')
            b = line.split(' ')
            dic.append(b)
    return dic

# 注：lanePosition的像素点坐标需要除以5转化成跟大图分辨率相匹配的分辨率，图像拼接时采用的每张小图的尺寸是128*96，车道线提取处理采用的图片是640*480
def cal_position(lane_position, picture_position):
    picturePosition = np.zeros([len(picture_position), 2])
    lanePosition = np.zeros([len(lane_position), 21])
    for i in range(1, len(picture_position) - 1):
        lanePosition[i][0] = i
        if not lane_position[i][1] == '':
            picturePosition[i][0] = int(picture_position[i][1]) - 64  # 根据图像中心点算出左上角起始坐标
            picturePosition[i][1] = int(picture_position[i][2]) - 48
            # print(picturePosition[i])
            for j in range(1, len(lane_position[i]), 2):
                lanePosition[i][j] = round((picturePosition[i][0] + int(lane_position[i][j]) / 5) / 19.26, 3)  # 按照像素点与实际长度的比例关系算出实际长度并保留三位小数
                lanePosition[i][j+1] = round((420 * 96 - (picturePosition[i][1] + int(lane_position[i][j+1]) / 5)) / 19.26, 3)
    return  lanePosition



if __name__ == "__main__":
    laneCenter = parse_lane_center(lane_center)
    pictureAxis = parse_picture_axis(picture_axis)
    xyInBigPic = cal_position(laneCenter, pictureAxis)

    with open(r'XY_AXIS/point2d.txt', 'w') as f:
        for i in range(1, len(xyInBigPic)):
            print(xyInBigPic[i])
            for j in range(0, 20):
                if not xyInBigPic[i][j] == 0:
                    f.write(str(xyInBigPic[i][j]))
                    if not xyInBigPic[i][j+1] == 0:
                        f.write(',')
            f.write('\n')
        f.close()
