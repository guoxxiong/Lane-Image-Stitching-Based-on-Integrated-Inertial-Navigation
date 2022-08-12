import rotate
from tkinter import *
import cv2

if __name__ == '__main__':
    root = Tk()
    root.title('ImStitch') # 显示窗口标题
    w = Label(root, text = 'hello')
    w.pack()
    root.mainloop()

    # rotatestate = rotate.rotate()
    # if rotatestate == 1:
    #     print('Photos have been rotated successfully...')
