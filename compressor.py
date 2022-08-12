import cv2
import os

if __name__ == "__main__":
    sourceDir = "PICTURE/photos1_0826_rotated/"
    dstDir = "PICTURE/photos1_0826_compressed01/"
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    for i in range(1,7366):
        temp = cv2.imread(sourceDir + str(i) + ".jpg")
        cpres = cv2.resize(temp, (0, 0), fx=0.10, fy=0.10, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(dstDir + str(i) + ".jpg", cpres)
        print(i)