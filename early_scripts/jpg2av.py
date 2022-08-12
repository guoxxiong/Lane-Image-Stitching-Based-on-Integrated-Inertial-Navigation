import os
import cv2
import numpy as np

path = 'PICTURE/photos1_0826/'

fps = 10 #视频每秒24帧
size = (640, 480) #需要转为视频的图片的尺寸
#可以使用cv2.resize()进行修改

videoWriter = cv2.VideoWriter("aosen.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
#视频保存在当前目录下
# cv2.namedWindow("transforming",1)

for i in range(1, 7366):
    img = cv2.imread(path + str(i) + ".jpg")
    print(img)
    videoWriter.write(img)

videoWriter.release()
cv2.destroyAllWindows()