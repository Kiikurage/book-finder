#coding: utf-8

import numpy as np
import cv2

#探したい本の表紙画像を読み込み

def segmentation(target_img):
    segmentator = cv2.ximgproc.segmentation.createGraphSegmentation(sigma=0.5, k=1000, min_size=3000)
    segmented_target = segmentator.processImage(target_img).astype(np.uint8)

    return segmented_target
    #mask = segment.reshape(list(segment.shape) + [1]).repeat(3, axis=2)
    #masked = np.ma.masked_array(target_img, fill_value=0)
    #for i in range(np.max(segment)):
    #    masked.mask = mask != i
    #    y, x = np.where(segment == i)
    #    top, bottom, left, right = min(y), max(y), min(x), max(x)
    #    dst = masked.filled()[top : bottom + 1, left : right + 1]
    #    cv2.imwrite('segment_{num}.jpg'.format(num=i), dst)

#画像の表示
def main():
    book_img = cv2.imread('./images/0.jpg', 1)
    target_img = cv2.imread('./images/target5.jpg', 1)
    segmented_target = segmentation(target_img)

    resized_dst = cv2.resize(segmented_target, (int(target_img.shape[0]/3), int(target_img.shape[1]/3)))
    cv2.namedWindow("segmented_image", cv2.WINDOW_NORMAL)
    cv2.imshow("segmented_image", resized_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
