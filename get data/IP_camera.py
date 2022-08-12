import cv2

url = 'xxx'
cap = cv2.VideoCapture(url)
while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.namedWindow("camera", 0)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("note/111280p.jpg", frame)
        break
cap.release()
cv2.destroyAllWindows()