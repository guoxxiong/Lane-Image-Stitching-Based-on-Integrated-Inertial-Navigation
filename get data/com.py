import time
import serial
import cv2
import os

url = 0
ser = serial.Serial('COM5', '115200')
cap1 = cv2.VideoCapture(url)
# cap2 = cv2.VideoCapture(1)
# cap3 = cv2.VideoCapture(3)
# cap4 = cv2.VideoCapture(2)
data = ''
i = 1
photoDir = "photos30/"
if not os.path.exists(photoDir):
    os.makedirs(photoDir)
txtDir = 'txt/test30.txt'

while True:
    data = ser.readline()
    res1, frame1 = cap1.read()
    # res2, frame2 = cap2.read()
    # res3, frame3 = cap3.read()
    # res4, frame4 = cap4.read()
    t1 = time.time()
    cv2.imwrite(photoDir + str(i) + ".jpg", frame1)
    t2 = time.time()
    # cv2.imwrite("photos14/%d.jpg" %i, frame2)
    # cv2.imwrite("photos15/%d.jpg" %i, frame3)
    # cv2.imshow("frame1", frame1)
    # cv2.imshow("frame2", frame2)
    # cv2.imshow("frame3", frame3)
    # cv2.imshow("frame4", frame4)
    # t = time.time()
    # ct = time.ctime(t)
    # print(ct, ':')
    print(data)
    # print(t2-t1)
    i = i+1
    #
    f = open(txtDir, 'a')
    # f.writelines(ct)
    # f.writelines(':\n')
    f.writelines(data.decode('utf-8'))
    # f.close()
    key = cv2.waitKey(1)
    # if key == 32:
    #     cv2.imwrite("note2/frame7.jpg", frame1)
    #     cv2.imwrite("note2/frame8.jpg", frame2)
    #     cv2.imwrite("note2/frame9.jpg", frame3)
    if key == 27:
        f.close()
        break
