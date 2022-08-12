import numpy as np
import cv2
import sys
import os
import geopy.distance
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import math


# 解析gpfpd消息，根据不同的txt注意修改函数返回变量
def parse_gpfpd(gpfpdfile):
    with open(gpfpdfile, 'r') as f:
        dic1 = []
        dic1.append(-1)
        dic2 = []
        # 先添加一个小列表，用以填充大列表第一个元素，方便后边索引
        dic2.append([0,0,0,0,-0.202,0,0,0,0,0,0,0,0,0,0,0])
        for line in f.readlines():
            line = line.strip('\n')
            # 去掉换行符\n
            b = line.split(',')
            # 将每一行以逗号为分隔符转换成列表
            dic1.append(b)
            #print(b)
        for i in range(len(dic1)):
            if i%2 == 1:
                dic2.append(dic1[i])
    return dic2


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


# 根据惯导经纬度及姿态角推算出透视变换中心经纬度,direction为相机与惯导连线与惯导y轴夹角（逆时针为正方向）
def get_distance_point(Gpfpd, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    cam_pos = np.zeros([len(Gpfpd),2], dtype = np.float64)
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


# 由经纬度变换出在图片坐标系中对应的坐标，注：y轴正方向为北，x轴正方向为东，x0,y0为第一张图片的位置
def lat_to_axis(camPos0, x0, y0, lat0, lon0):
    picture_axis = np.zeros([len(camPos0),2],dtype = np.int)
    picture_axis[0][0] = y0
    picture_axis[0][1] = x0
    for camPos0_index in range(1, len(camPos0)):
        # 将单位转换成厘米 , 420p大约0.1916个像素代表一厘米，这是像素坐标与实际坐标的比例系数k，详解见DOC
        picture_axis[camPos0_index][0] = int((camPos0[camPos0_index][0] - lat0) * 111 * 100000*0.1916)
        # 40.02按照北京地区的纬度计算经度每相差一度的实际距离
        picture_axis[camPos0_index][1] = int((camPos0[camPos0_index][1] - lon0) * 111 * 100000 * math.cos(camPos0[camPos0_index][0] * math.pi / 180)*0.1916)
    return picture_axis


# 将img2粘贴到img1的x,y位置
def paste_photo(img1, img2, x, y):
    h, w, ch = img2.shape
    for index_i in range(y - int(h/2), y + int(h/2)):
        for index_j in range(x - int(w/2), x + int(w/2)):
            if (img1[index_i][index_j][0] <= 20) and (img1[index_i][index_j][1] <= 20) and (img1[index_i][index_j][2] <= 20):
                img1[index_i][index_j] = img2[index_i - y + int(h/2)][index_j - x + int(w/2)]
    return img1


# 在拼接好的图上画出惯导的轨迹
def drawImuTrack(canvas, imu_picture_pos):
    for ipp in range(1, len(imu_picture_pos)):
        canvas[int(96*420 - 1920 - imu_picture_pos[ipp][0])][int(128*100 + imu_picture_pos[ipp][1])] = np.array([0, 0, 255],dtype=np.uint8)
        canvas[int(96*420 - 1920 - imu_picture_pos[ipp][0] - 1)][int(128*100 + imu_picture_pos[ipp][1] - 1)] = np.array([0, 0, 255],dtype=np.uint8)
        canvas[int(96*420 - 1920 - imu_picture_pos[ipp][0] - 1)][int(128*100 + imu_picture_pos[ipp][1] + 1)] = np.array([0, 0, 255],dtype=np.uint8)
        canvas[int(96*420 - 1920 - imu_picture_pos[ipp][0] + 1)][int(128*100 + imu_picture_pos[ipp][1] - 1)] = np.array([0, 0, 255],dtype=np.uint8)
        canvas[int(96*420 - 1920 - imu_picture_pos[ipp][0] + 1)][int(128*100 + imu_picture_pos[ipp][1] + 1)] = np.array([0, 0, 255],dtype=np.uint8)
        # print(ipp)


# 将惯导图片上的轨迹坐标保存为txt
def saveTrackAsTxt(f, imu_picture_pos, gpd):
    for ipp in range(1, len(imu_picture_pos)):
        f.write(str(round(((int(128*100 + imu_picture_pos[ipp][1]))/19.26), 3)) + "," + str(round(((int(1920 + imu_picture_pos[ipp][0]))/19.26), 3)) + "," + str(gpd[ipp][3]))
        f.write('\n')


if __name__ == "__main__":
    start_index = 1
    end_index = 7360
    img_imputDir = "PICTURE/photos1_0826_compressed02/"
    img_outputDir = "FINAL/bird_views/"
    gpfpd = parse_gpfpd("TXT/imu1_0826.txt")
    fwp = open(r'TXT/imu_track.txt', 'w')
    fwxy = open(r'XY_AXIS/picture_axis.txt', 'w')
    camPos = get_distance_point(gpfpd, pow(pow(0.5, 2) + pow(12, 2), 0.5), math.atan2(0.5, 12) * 180 / math.pi) # 8.5,4.5
    pic_axis = lat_to_axis(camPos, 0, 0, camPos[1][0], camPos[1][1])
    imuPos = np.zeros([len(gpfpd),2])
    for igp in range(len(gpfpd)):
        imuPos[igp][0] = gpfpd[igp][6]
        imuPos[igp][1] = gpfpd[igp][7]
    imu_axis = lat_to_axis(imuPos, 0, 0, camPos[1][0], camPos[1][1])
    saveTrackAsTxt(fwp, imu_axis, gpfpd)
    fwp.close()

    # 图像拼接
    # 定义底板的高的系数
    a = 420
    # 定义底板的宽的系数
    b = 380
    # 定义横向纵向偏移量，保证图片拼接不会超出边界
    x_offset = 128*100
    y_offset = 96*420 - 1920
    # 定义拼接图像的底板
    temp = np.zeros([96*a, 128*b, 3], dtype = np.uint8)
    # temp = cv2.imread("FINAL/ajoint11.jpg")
    Img = cv2.imread(img_imputDir + str(start_index + 1) + ".jpg")


    for j in range(start_index + 1, end_index):
        Img = cv2.imread(img_imputDir + str(j) + ".jpg")
        # paste_photo(img1, img2, x, y)将img2贴到img1上，注意这里y是像素坐标点，方向与正北相反，需要用大底图的高减去原本的y值
        paste_photo(temp, Img, int(x_offset + pic_axis[j][1]), int(y_offset - pic_axis[j][0]))
        # 生成每张图片在大图中的位置坐标，用以地图自动生成时每张图片的参考坐标
        fwxy.write(str(j) + ' ' + str(int(128*100 + pic_axis[j][1])) + ' ' + str(int(96*a - 1920 - pic_axis[j][0])))
        fwxy.write('\n')
        print(int(128*100 + pic_axis[j][1]), int(96*a - 1920 - pic_axis[j][0]), j)
    fwxy.close()

    # 绘制惯导轨迹
    drawImuTrack(temp, imu_axis)

    # 按比例缩放
    # bird_view1 = cv2.resize(temp, (0, 0), fx=0.05, fy=0.05, interpolation=cv2.INTER_NEAREST)
    # bird_view2 = cv2.resize(temp, (0, 0), fx=0.02, fy=0.02, interpolation=cv2.INTER_NEAREST)
    bird_view3 = cv2.resize(temp, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    bird_view4 = cv2.resize(temp, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
    # bird_view5 = cv2.resize(temp, (0, 0), fx=0.75, fy=0.75, interpolation=cv2.INTER_NEAREST)
    # bird_view6 = cv2.resize(temp, (0, 0), fx=0.10, fy=0.10, interpolation=cv2.INTER_NEAREST)

    # 可以根据需求保存缩放后的图片，需手动修改输出文件名
    # cv2.imwrite(img_outputDir + "ajoint24_bird005.jpg", bird_view1)
    # cv2.imwrite(img_outputDir + "ajoint24_bird002.jpg", bird_view2)
    cv2.imwrite(img_outputDir +"ajoint42_bird05.jpg", bird_view3)
    cv2.imwrite(img_outputDir + "ajoint42_bird025.jpg", bird_view4)
    # cv2.imwrite(img_outputDir + "ajoint24_bird075.jpg", bird_view5)
    # cv2.imwrite(img_outputDir + "ajoint24_bird010.jpg", bird_view6)
    cv2.imwrite(img_outputDir + "ajoint42.jpg",temp)

