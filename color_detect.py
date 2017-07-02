#coding: utf-8
import numpy as np
import cv2

#探したい本の表紙画像を読み込み
book_img = cv2.imread('./images/0.jpg', 1)
target_img = cv2.imread('./images/target5.jpg', 1)
target_img_hsv = cv2.cvtColor(target_img, cv2.COLOR_BGR2HSV)

height = len(book_img)
width = len(book_img[0])
channels = len(book_img[0][0])

#左端のみ切り取り
book_img_leftside = book_img[:, 0:int(width/10), :]
#HSV色空間に変換
book_img_leftside = cv2.cvtColor(book_img_leftside, cv2.COLOR_BGR2HSV)

#色の平均値の計算
average_color = np.zeros((3, )).astype(np.uint8)
for channel in range(channels):
    average_color[channel] = np.sum(book_img_leftside[:, :, channel]) / (height * int(width / 10))

#mask画像の作成
alpha = 5
mask_img1 = np.ones(target_img_hsv[:, :, 0].shape) * (average_color[0] - alpha) < target_img_hsv[:, :, 0]
mask_img2 = target_img_hsv[:, :, 0] < np.ones(target_img_hsv[:, :, 0].shape) * (average_color[0] + alpha)
mask_img = (mask_img1 * mask_img2).astype(np.uint8) * 255

# 8近傍の定義
neiborhood8 = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]],
                        np.uint8)

# 8近傍で縮小処理
mask_img = cv2.erode(mask_img, neiborhood8, iterations=5)
mask_img = cv2.dilate(mask_img, neiborhood8, iterations=5)

#target画像にmask画像をかける
masked_target_img = np.zeros(target_img.shape).astype(np.uint8)
for channel in range(channels):
    masked_target_img[:, :, channel] = ((target_img[:, :, channel] * ((mask_img == 255).astype(np.uint8))))

#画像の表示
resized_origin = cv2.resize(masked_target_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
resized_dst = cv2.resize(mask_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
cv2.namedWindow("mask_image", cv2.WINDOW_NORMAL)
cv2.imshow("original_image", resized_origin)
cv2.imshow("mask_image", resized_dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
