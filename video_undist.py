#对视频进行畸变矫正，将去畸变程序加进来：先读视频，然后对每一帧进行处理。
#即将flip函数换成畸变校正函数。得给定内参矩阵。

import numpy as np
import cv2
#usb1080
# cammtx =  np.array([[1.34845229e+03,0.00000000e+00,9.77390484e+02],
#                     [0.00000000e+00,1.34840275e+03,5.59358513e+02],
#                     [0.00000000e+000,00000000e+00,1.00000000e+00]])
#
# camdist = np.array([-4.27490871e-01,2.06365663e-01,9.34180839e-05, -9.00038258e-04,-2.16294861e-02])

# newcammtx = np.array([[1.00695982e+03,0.00000000e+00,9.74177332e+02],
#                      [0.00000000e+00,1.00654011e+03,5.59744426e+02],
#                      [0.00000000e+00,0.00000000e+00,1.00000000e+00]])
#web3 720
cammtx =  np.array([[1.01400136e+03,0.00000000e+00,6.38469236e+02],
                    [0.00000000e+00,1.01256729e+03,3.28379251e+02],
                    [0.00000000e+000,00000000e+00,1.00000000e+00]])

camdist = np.array([-3.56756830e-01, 1.06751304e-01, 1.68798888e-04, 6.08272330e-04, 2.09347793e-01])
#
# newcammtx = np.array([[882.53606696,0.00000000e+00,639.4543506],
#                      [0.00000000e+00, 884.67690797,329.92114628],
#                      [0.00000000e+00,0.00000000e+00,1.00000000e+00]])


cap = cv2.VideoCapture('AVI/log_data_ID5_S2.avi')

fps = 25 #30
# 获取视频的大小
size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# size = (1280,720)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  #avi对应XVID,mp4对应mp4v
out = cv2.VideoWriter('AVI/undist1/log_data_ID5_S2_undist.avi', fourcc, fps, size)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        h=720
        w=1280
        newcammtx, roi = cv2.getOptimalNewCameraMatrix(cammtx, camdist, (w, h), 1, (w, h),centerPrincipalPoint=1)
        dst = cv2.undistort(frame, cammtx, camdist, None, newcammtx)
        dst = dst[0: h, 0: w]
        # write the flipped frame
        out.write(dst)
        cv2.imshow('frame',dst)
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == 32:
            while True:
                if cv2.waitKey(100) == 27:
                    break
    else:
        break
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()