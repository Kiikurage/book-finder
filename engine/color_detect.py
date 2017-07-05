# coding: utf-8
import cv2
import numpy as np
from PIL import ImageFilter, Image


def color_detect(book_img, target_img):

    # HSV色空間に変換
    target_img_hsv = cv2.cvtColor(target_img, cv2.COLOR_BGR2HSV)
    book_img_hsv = cv2.cvtColor(book_img, cv2.COLOR_BGR2HSV)

    # 色の平均値の計算
    average_color = np.sum(book_img_hsv, axis=(0, 1)) / (book_img_hsv.shape[0] * book_img_hsv.shape[1])
    print(average_color)
    # mask画像の作成: 条件=h(色相)が範囲内
    threshold = 5
    mask_img = np.abs(target_img_hsv[:, :, 0] - average_color[0]) < 5
    mask_img = np.bitwise_and(mask_img, np.abs(target_img_hsv[:, :, 1] - average_color[1]) < 50)
    mask_img = np.bitwise_and(mask_img, np.abs(target_img_hsv[:, :, 2] - average_color[2]) < 50)
    # cv2.imwrite("./tmp.jpg", mask_img.astype(np.uint8) * 255)

    # 縮小処理でノイズ除去
    mask_img = Image.fromarray(mask_img.astype(np.uint8))
    mask_img = mask_img.filter(ImageFilter.MinFilter(size=9))
    mask_img = mask_img.filter(ImageFilter.MaxFilter(size=9))
    mask_img = np.array(mask_img)
    cv2.imwrite("./color_mask.jpg", mask_img.astype(np.uint8) * 255)
    # cv2.imwrite("./tmp.jpg", mask_img.astype(np.uint8) * 255)

    # target画像にmask画像をかける
    masked_target_img = target_img * mask_img[:, :, None]
    cv2.imwrite("./color_masked.jpg", masked_target_img.astype(np.uint8))
    # exit(0)

    return mask_img, masked_target_img
