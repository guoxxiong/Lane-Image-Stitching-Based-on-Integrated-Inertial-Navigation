import cv2


# 二值化
def binaryzation(img):
    h, w, ch = img.shape()
    for i in range(0, h):
        for j in range(0, w):
            if (img[i][j][0] < 200) or (img[j][j][1] < 200) or (img[i][j][2] < 200):
                img[i][j] = [0, 0, 0]
            else:
                img[i][j] = [255, 255, 255]
    return img


if __name__ == "__main__":
    cv2.imread()