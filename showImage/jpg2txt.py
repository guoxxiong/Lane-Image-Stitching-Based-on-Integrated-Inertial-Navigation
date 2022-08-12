from PIL import Image
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

# 需要先设置内存限制，不然仍然会报错内存溢出
Image.MAX_IMAGE_PIXELS = None
img = io.imread("images/ajoint40_2.jpg")
# img = Image.open("images/ajoint40.jpg")
# plt.imshow(img)
print("read img successfully...img shape:", img.shape)

f = open(r"TXT/ajoint40_4.txt", mode='w')
x, y, z = 0, 0, 0
r, g, b = 0, 0, 0

height, width, chanel = img.shape
f.write(str(height) + "," + str(width) + "," + str(chanel) + "\n")
for i in range(0, height, 2):
    for j in range(0, width, 20):
        r = img[i][j][2]
        g = img[i][j][1]
        b = img[i][j][0]
        if (r > 20) or (g > 20) or (b > 20):
            for k in range(j - 20, width, 2):
                x = float(k / 19.26)
                y = float((height - i) / 19.26)
                r = img[i][k][2]
                g = img[i][k][1]
                b = img[i][k][0]
                f.write(str(round(x, 2)) + " " + str(round(y, 2)) + " " + str(r) + " " + str(g) + " " + str(b) + "\n")
                print(x, y, z, r, g, b)
                if (r < 20) and (g < 20) and (b < 20):
                    j = k
                    break
    print(i)
f.close()

