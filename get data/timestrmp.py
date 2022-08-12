import time
import serial

ser = serial.Serial("COM5", 230400)
data = ""
f = open("txt/test.txt", "a")
while True:
    # data = ser.readline()
    t = time.time()
    print(t)
    # print(data)
    f.writelines(str(t) + "\n")
    