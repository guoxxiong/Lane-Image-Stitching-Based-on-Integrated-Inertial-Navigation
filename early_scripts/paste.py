import cv2

# 将img2粘贴到img1的x,y位置
def paste_photo(img1, img2, x, y):
    h, w, ch = img2.shape
    for i in range(y, y + h):
        for j in range(x, x + w):
            img1[i][j] = img2[i - y][j - x]
    return img1


if __name__ == "__main__":
    fromImg = cv2.imread("temps/temp2.jpg")
    toImg = cv2.imread("0718/photos15_rotated/243.jpg")
    finalImg = paste_photo(fromImg, toImg, 1000, 2000)
    cv2.namedWindow("result",0)
    cv2.imshow("result", fromImg)
    cv2.waitKey(0)
