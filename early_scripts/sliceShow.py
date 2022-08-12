import cv2
import numpy as np

circle_color = (0, 0, 255) #BGR
big_img_width = 46080
big_img_height = 64800
start_pos_x = 43520
start_pos_y = 63360

# cv2.namedWindow("birdView", 0)
cv2.namedWindow("mainPage", 0)


if __name__ == "__main__":
    bird_img = cv2.imread("FINAL/bird_views/ajoint13_bird1")
    pos_x = start_pos_x
    pos_y = start_pos_y
    while True:
        main_img = cv2.imread("FINAL/slice_up/ajoint13/x" + str(pos_x) + "y" + str(pos_y) + ".jpg")
        print(pos_x, pos_y)
        # cv2.circle(bird_img,(int(pos_x * 0.05), int(pos_y * 0.05)), 100, circle_color, 0)
        # cv2.imshow("birdView", bird_img)
        cv2.imshow("mainPage", main_img)
        key_v = cv2.waitKeyEx(100)
        if (key_v == 2424832) and ((pos_x - 1280) >= 0): # 左键
            pos_x = pos_x - 1280
            continue
        if (key_v == 2490368) and ((pos_y - 720) >= 0): # 上键
            pos_y = pos_y - 720
            continue
        if (key_v == 2555904) and ((pos_x + 1280) <= big_img_width): # 右键
            pos_x = pos_x + 1280
            continue
        if (key_v == 2621440) and ((pos_y + 720) <= big_img_height): # 下键
            pos_y = pos_y + 720
            continue
        if (key_v == 27): # ESC
            break

