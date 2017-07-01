#coding: utf-8
import numpy as np
import cv2

#探したい本の表紙画像を読み込み
book_img = cv2.imread('./images/0.jpg', 1)
target_img = cv2.imread('./images/target.jpg', 1)

height = len(book_img)
width = len(book_img[0])
channels = len(book_img[0][0])

#左端のみ切り取り
book_img_leftside = book_img[:, 0:int(width/10), :]
#HSV色空間に変換
book_img_leftside = cv2.cvtColor(book_img_leftside, cv2.COLOR_BGR2HSV)

#色の平均値の計算（RGB)
average_color = np.zeros((3, )).astype(np.uint8)
for channel in range(channels):
    average_color[channel] = np.sum(book_img_leftside[:, :, channel]) / (height * int(width / 10))

#色の平均値の表示
average_color_image = np.ones((100, 100, 3)).astype(np.uint8)
for channel in range(channels):
    average_color_image[:, :, channel] *= average_color[channel]

cv2.namedWindow("average_color_image", cv2.WINDOW_NORMAL)
cv2.imshow("average_color_image", average_color_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
