import cv2
import os

# 读取视频
video = cv2.VideoCapture("AVI/undist1/log_data_ID5_S2_undist.avi")
#video.set(cv2.CAP_PROP_POS_MSEC, 66000)
count_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
#fps = video.get(cv2.CAP_PROP_FPS)
fps=25
# w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
# h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
# size0 = (w,h)
# size = (h, w)
size = (video.get(cv2.CAP_PROP_FRAME_WIDTH),video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc(*'XVID')  # avi对应XVID,mp4对应mp4v
# out = cv2.VideoWriter('video_0730/log_data_ID25_S8-warp.avi', fourcc, fps, (800,1600))

if not os.path.exists('PICTURE/log_data_ID5_S2_undist/'):  # 生成文件夹
    os.makedirs('PICTURE/log_data_ID5_S2_undist/')

num_frame=0
num_frame_detect = 0
num_frame_not_detect = 0
time = 0

# 每帧进行处理
while True:
    for _ in range(1):
        ret, frame = video.read()
    if not ret:
        break

    num_frame +=1
    print('num_frame=',num_frame)
    print('第{}帧'.format(num_frame))
    time +=1/ fps
    print('time=',time)
    #frame = gamma_trans(frame, 2)  # 伽马变换
    # warp = cv2.warpPerspective(frame, m, warp_shape, flags=cv2.INTER_LINEAR)

    # print('显示车道线的帧数=',num_frame_detect)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow("frame",frame)
    # cv2.namedWindow('warp', cv2.WINDOW_NORMAL)
    # cv2.imshow("warp", warp)
    #if num_frame % 10==0:
    cv2.imwrite(r'PICTURE/log_data_ID5_S2_undist/{}.jpg'.format(num_frame), frame)  # 存储为图像
    #out.write(frame)
    key = cv2.waitKey(1)
    if key == 27:  #ASCII码27：ESC
        break
    elif key == 32: #ASCII码27：Space
        while True:
            if cv2.waitKey(100) == 27:
                break

cv2.destroyAllWindows()
video.release()
# out.release()