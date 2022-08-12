import matplotlib.image as mping
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
import os

# 透视变换函数
def getMat():
    # chess_image = cv2.imread("0718/note2/frame2.jpg")  # 读外参标定照片
    # #ret, corners = cv2.findChessboardCorners(chess_image, (6, 9), None)  # 寻找棋盘格角点，看图片的起点（红色）和走线，确定顺序，
    # ret, corners = cv2.findChessboardCorners(chess_image, (4,6), None)  # 寻找棋盘格角点，看图片的起点（红色）和走线，确定顺序，
    # if ret:
    #     # 设置终止条件，迭代30次或移动0.001#
    #     criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    #     # show chessboard corners 绘制图案，展示角点
    #     cv2.drawChessboardCorners(chess_image, (4, 6), corners, ret)
    #     cv2.imshow("chess_image", chess_image)
    #     cv2.waitKey(100)
    # else:
    #     print("ERROR: Chessboard corners not found!")
    #     quit()
    # src = np.float32([corners[-1], corners[-6], corners[5], corners[0]])  # 四个顶点的角点，conners[-1]倒数第一个元素
    # src = np.float32([[237+6, 354-1], [352+6, 352+1], [226-5, 396-1], [368-5, 394+1]])  # 唯实园区透视变换参数
    # src = np.float32([[572+1, 556+1], [689-5+8, 556+2], [557+4, 605], [701+10, 603+2+2]])  # 奥森弯道变道透视变换参数1,0808
    # src = np.float32([[466-2, 423], [778-2, 422-2], [250, 491], [985, 490-2]])  # 奥森弯道变道透视变换参数2
    src = np.float32([[155, 366], [458, 360], [1, 473], [638, 468]])  # 奥森弯道变道透视变换参数3,0827
    print(src)
    width, height = 400, 520
    # width, height = 750, 750 #用以做透视变换，8格24.68

   ori_x,  ori_y = 120, 220
    # ori_x, ori_y = 272, 0  
    #目标画布
    #dst = np.float32([[ori_x, ori_y], [ori_x - width, ori_y], [ori_x, ori_y - height], [ori_x - width, ori_y - height]])
    dst = np.float32([[ori_x, ori_y], [ori_x + width, ori_y], [ori_x, ori_y + height], [ori_x + width, ori_y + height]])

    # get perspective transform matrix
    m = cv2.getPerspectiveTransform(src, dst)  # 通过两组顶点组成的矩形进行透视变换，得变换矩阵
    m_inv = cv2.getPerspectiveTransform(dst, src)
    # print(m)
    return m

# 主函数
# if __name__ == "__main__":
def warping():
    file_path = "PICTURE/photos1_0826/"
    file_tail = ".jpg"
    store_path = "PICTURE/photos1_0826_warped/"
    if not os.path.exists(store_path):  # 生成文件夹
        os.makedirs(store_path)
    m = getMat()
    for i in range(1, 7367):
        origin_img = cv2.imread(file_path + str(i) + file_tail)
        warp_img = cv2.warpPerspective(origin_img, m, (640, 480))
        # cv2.namedWindow("warped",0)
        # cv2.imshow("warped",warp_img)
        # cv2.waitKey(0)
        cv2.imwrite(store_path + str(i) + file_tail, warp_img)
        print(i)
    return 1



