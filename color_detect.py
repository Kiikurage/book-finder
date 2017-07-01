#coding: utf-8
import numpy as np
import cv2

#探したい本の表紙画像を読み込み
book_img = cv2.imread('./images/0.jpg', 1)
target_img = cv2.imread('./images/target2.jpg', 1)
target_img_hsv = cv2.cvtColor(target_img, cv2.COLOR_BGR2HSV)

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

alpha = 5
mask_img1 = np.ones(target_img_hsv[:, :, 0].shape) * (average_color[0] - alpha) < target_img_hsv[:, :, 0]
mask_img2 = target_img_hsv[:, :, 0] < np.ones(target_img_hsv[:, :, 0].shape) * (average_color[0] + alpha)
mask_img = (mask_img1 * mask_img2).astype(np.uint8) * 255
print(mask_img1.shape, mask_img2.shape, mask_img.shape, book_img.shape, target_img_hsv.shape)

#画像の表示
resized_origin = cv2.resize(target_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
resized_dst = cv2.resize(mask_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
cv2.namedWindow("mask_image", cv2.WINDOW_NORMAL)
cv2.imshow("original_image", resized_origin)
cv2.imshow("mask_image", resized_dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
