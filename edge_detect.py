#coding: utf-8
import numpy as np
import cv2

#探したい本の表紙画像を読み込み
book_img = cv2.imread('./images/0.jpg', 1)
target_img = cv2.imread('./images/target.jpg', 1)

height = len(book_img)
width = len(book_img[0])
channels = len(book_img[0][0])

gray = cv2.cvtColor(target_img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
lines = cv2.HoughLines(edges,1,np.pi/180,200)
cnt = 0
for rho,theta in lines[:, 0, :]:
    cnt += 1
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(target_img,(x1,y1),(x2,y2),(255,255,255),10)
    if cnt > 100:
        break
    print("line was drawn\n")

#画像の表示
resized_dst = cv2.resize(target_img, (int(target_img.shape[0]/5), int(target_img.shape[1]/5)))
cv2.namedWindow("edge_detected_image", cv2.WINDOW_NORMAL)
cv2.imshow("edge_detected_image", resized_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
