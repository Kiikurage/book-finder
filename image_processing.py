#coding: utf-8
import numpy as np
import cv2
from color_detect import color_detect
from line_detect import line_detect

def main():
    book_img = cv2.imread('./images/0.jpg', 1)
    target_img = cv2.imread('./images/target5.jpg', 1)

    mask_img, masked_target_img = color_detect(book_img, target_img)
    masked_target_img = line_detect(book_img, target_img, masked_target_img)

    #画像の表示
    resized_origin = cv2.resize(masked_target_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
    resized_dst = cv2.resize(mask_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
    cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask_image", cv2.WINDOW_NORMAL)
    cv2.imshow("original_image", resized_origin)
    cv2.imshow("mask_image", resized_dst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
