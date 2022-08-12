import cv2
import numpy as np

def replace_black(img1, img2, x1, y1, x2, y2):
    for i in range(y1, y2):
        crack_start = 0  # 定义一个裂缝标记变量，标记裂缝是否已经过处理
        for j in range(x1, x2):
            if (img1[i][j][0] <= 6) and (img1[i][j][1] <= 6) and (img1[i][j][2] <= 6):  # 判断此处像素点是黑点的阈值设置
                if crack_start == 0:  # 填充裂缝
                    for s in range(1, 5):
                        img1[i][j - s][0] = img2[i][j - s][0]
                        img1[i][j - s][1] = img2[i][j - s][1]
                        img1[i][j - s][2] = img2[i][j - s][2]
                    crack_start = 1
                img1[i][j][0] = img2[i][j][0]
                img1[i][j][1] = img2[i][j][1]
                img1[i][j][2] = img2[i][j][2]
    return img1


if __name__ == "__main__":
    im1 = cv2.imread("rotated_vertical/80.jpg")
    # for i in range(0,im1.shape[0]):
    #     for j in range(0,im1.shape[1]):
    #         print(im1[i][j])
    im2 = cv2.imread("rotated_vertical/119.jpg")
    # print(im2)
    im = replace_black(im1, im2, 0, 0, 1279, 719)
    cv2.namedWindow("replaced", 0)
    cv2.imshow("replaced",im)
    cv2.waitKey(0)
