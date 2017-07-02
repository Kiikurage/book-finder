#coding: utf-8

import numpy as np
import cv2

#探したい本の表紙画像を読み込み
book_img = cv2.imread('./images/0.jpg', 1)
target_img = cv2.imread('./images/target2.jpg', 1)

height = len(book_img)
width = len(book_img[0])
channels = len(book_img[0][0])

segmentator = cv2.ximgproc.segmentation.createGraphSegmentation(sigma=0.5, k=1000, min_size=3000)
segmented_target = segmentator.processImage(target_img).astype(np.uint8)

#mask = segment.reshape(list(segment.shape) + [1]).repeat(3, axis=2)
#masked = np.ma.masked_array(target_img, fill_value=0)
#for i in range(np.max(segment)):
#    masked.mask = mask != i
#    y, x = np.where(segment == i)
#    top, bottom, left, right = min(y), max(y), min(x), max(x)
#    dst = masked.filled()[top : bottom + 1, left : right + 1]
#    cv2.imwrite('segment_{num}.jpg'.format(num=i), dst)

#画像の表示
resized_dst = cv2.resize(segmented_target, (int(target_img.shape[0]/3), int(target_img.shape[1]/3)))
cv2.namedWindow("segmented_image", cv2.WINDOW_NORMAL)
cv2.imshow("segmented_image", resized_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
