import cv2
import sys
import  os

# 解析gpfpd消息
def parse_gpfpd(gpfpdfile):
    with open(gpfpdfile, 'r') as f:
        dic1 = []
        dic1.append(-1)
        dic2 = []
        dic2.append([0,0,0,0,-0.202,0,0,0,0,0,0,0,0,0,0,0])
        for line in f.readlines():
            line = line.strip('\n')
            # 去掉换行符\n
            b = line.split(',')
            # 将每一行以逗号为分隔符转换成列表
            dic1.append(b)
            #print(b)
        # 注意下列语句主要用于中间有空行的txt，
        for i in range(len(dic1)):
            if i%2 == 1:
                dic2.append(dic1[i])
    return dic2


# if __name__ == "__main__":
def rotate():
    start_index = 1
    end_index = 7366
    gpfpd = parse_gpfpd("TXT/imu1_0826.txt")
    print(gpfpd[1][1])
    print(gpfpd[2][1])

    img_dir = "PICTURE/photos1_0826_warped/"
    rotated_dir = "PICTURE/photos1_0826_rotated/"
    if not os.path.exists(rotated_dir):
        os.makedirs(rotated_dir)
    imgName_tail = ".jpg"
    # 设置图片从起始序号读取图片并进行旋转
    for i in range(start_index, end_index):
        print(i)
        img = cv2.imread(img_dir + str(i) + imgName_tail)
        rows, cols, chanel = img.shape
        # print(rows, cols)
        # rotate_angle = float(gpfpd[start_index][0])-float(gpfpd[2*i-1][0])
        # rotate_angle = float(357.71 - float(gpfpd[2 * i - 1][0]))
        rotate_angle = float(360 - float(gpfpd[i][3]))
        print(rotate_angle)
        M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), rotate_angle, 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        cv2.imwrite(rotated_dir + str(i) + imgName_tail, dst)
    return 1

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