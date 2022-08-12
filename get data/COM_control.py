import serial
import pygame

ser = serial.Serial('COM5', '115200')
data = ''

while True:
    data = ser.readline()
    print(data)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_1]:  # 10Hz
        ser.write("$cmd,output,com0,gpfpd,0.1*ff")
    if keys_pressed[pygame.K_2]:  # 20Hz
        ser.write("$cmd,output,com0,gpfpd,0.05*ff")
    if keys_pressed[pygame.K_3]:  # 25Hz
        ser.write("$cmd,output,com0,gpfpd,0.04*ff")
