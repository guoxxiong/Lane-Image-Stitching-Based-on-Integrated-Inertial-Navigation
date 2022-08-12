import cv2
import serial
import threading

# ser = serial.Serial('COM5', 115200)

url = ''
cap = cv2.VideoCapture(url)
fps = 25
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
sz = (1920, 1080)
vout = cv2.VideoWriter()
vout.open('video/lane1080p_23.avi', fourcc, fps, sz)
# f = open('txt/test1.txt', 'a')
# data = ''
while True:
    # data = ser.readline()
    ret, frame = cap.read()
    # f.writelines(data.decode('utf-8'))
    # print(data)
    vout.write(frame)



# f.close()
vout.release()
cap.release()

