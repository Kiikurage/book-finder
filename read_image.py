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
book_img_leftside = cv2.cvtColor(book_img_leftside, cv2.COLOR_BGR2HSV)

#色の平均値の計算（RGB)
average_color = np.zeros((3, )).astype(np.uint8)
for channel in range(channels):
    average_color[channel] = np.sum(book_img_leftside[:, :, channel]) / (height * int(width / 10))
#print(average_color)

average_color_image = np.ones((100, 100, 3)).astype(np.uint8)
for channel in range(channels):
    average_color_image[:, :, channel] *= average_color[channel]

target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2HSV)
alpha = 10
print((np.ones(target_img[0].shape) * (average_color[0] - alpha)).shape)
print(target_img[0].shape)
mask_img1 = np.ones(target_img[0].shape) * (average_color[0] - alpha) < target_img[0]
mask_img2 = target_img[0] < np.ones(target_img[0].shape) * (average_color[0] + alpha)
mask_img = (mask_img1 * mask_img2).astype(np.uint8) * 255

segmentator = cv2.ximgproc.segmentation.createGraphSegmentation(sigma=0.5, k=1000, min_size=3000)
segment = segmentator.processImage(target_img).astype(np.uint8)
print(segment.shape, segment.dtype)
#mask = segment.reshape(list(segment.shape) + [1]).repeat(3, axis=2)
#masked = np.ma.masked_array(target_img, fill_value=0)
#for i in range(np.max(segment)):
#    masked.mask = mask != i
#    y, x = np.where(segment == i)
#    top, bottom, left, right = min(y), max(y), min(x), max(x)
#    dst = masked.filled()[top : bottom + 1, left : right + 1]
#    cv2.imwrite('segment_{num}.jpg'.format(num=i), dst)


#画像の表示
target_img = segment
resized_target_img = cv2.resize(target_img, (int(target_img.shape[0]/5), int(target_img.shape[1]/5)))
#cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.namedWindow("resized_image", cv2.WINDOW_NORMAL)
cv2.namedWindow("average_color_image", cv2.WINDOW_NORMAL)
#cv2.imshow('image', mask_img)
cv2.imshow('resized_image', resized_target_img)
cv2.imshow('average_color_image', average_color_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
