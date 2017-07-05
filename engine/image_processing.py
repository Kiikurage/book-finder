# coding: utf-8
import argparse
import math
import os

import cv2
import numpy as np
from PIL import Image

from color_detect import color_detect
from line_detect import line_detect


def load_image(path):
    img = Image.open(path)
    img = np.array(img)[:, :, [2, 1, 0]]  # opencvはBGRオーダー
    return img


def main():
    parser = argparse.ArgumentParser(description='detect book from target image')
    parser.add_argument('book_image', type=str, help='path to the image of book')
    parser.add_argument('target_image', type=str, help='path to the image of bookshelf')
    parser.add_argument('result_image', type=str, help='path to the destination image')
    args = parser.parse_args()

    book_img = load_image(args.book_image)
    target_img = load_image(args.target_image)

    mask_img, masked_target_img = color_detect(book_img, target_img)
    masked_target_img, coord_list = line_detect(book_img, target_img, masked_target_img)

    count = 0
    coord_list = sorted(coord_list, key=lambda x: x[4])
    best_rect = None
    best_score = 100000000
    total_mask = mask_img.sum()
    for i1, (_, _, _, _, r1, t1, a1, b1) in enumerate(coord_list):
        print(i1, len(coord_list))
        for i2 in range(i1 + 1, len(coord_list)):
            if min(abs(coord_list[i2][5] - t1), abs(abs(coord_list[i2][5] - t1) - np.pi)) > np.pi / 180 * 10:
                # line[i1] と line[i2]は平行ではない
                continue
            r2, t2, a2, b2 = coord_list[i2][4:]

            for i3 in range(i1 + 1, len(coord_list)):
                if abs(np.pi / 2 - min(
                        abs(coord_list[i3][5] - t1),
                        abs(abs(coord_list[i3][5] - t1) - np.pi)
                )) > np.pi / 180 * 30:
                    # line[i1] と line[i3]は垂直ではない
                    continue
                r3, t3, a3, b3 = coord_list[i3][4:]

                for i4 in range(i3 + 1, len(coord_list)):
                    if min(abs(coord_list[i4][5] - t3), abs(abs(coord_list[i4][5] - t3) - np.pi)) > np.pi / 180 * 5:
                        # line[i3] と line[i4]は並行ではない
                        continue
                    r4, t4, a4, b4 = coord_list[i4][4:]

                    left_top_x = int((r1 * b3 - r3 * b1) / (a1 * b3 - a3 * b1))
                    left_top_y = int((r1 * a3 - r3 * a1) / (b1 * a3 - b3 * a1))
                    right_bottom_x = int((r2 * b4 - r4 * b2) / (a2 * b4 - a4 * b2))
                    right_bottom_y = int((r2 * a4 - r4 * a2) / (b2 * a4 - b4 * a2))

                    x0 = min(left_top_x, right_bottom_x)
                    y0 = min(left_top_y, right_bottom_y)
                    x1 = max(left_top_x, right_bottom_x)
                    y1 = max(left_top_y, right_bottom_y)

                    # 本の高さは厚みの6倍以上有るはず（適当）
                    height = max(abs(x1 - x0), abs(y1 - y0))
                    width = min(abs(x1 - x0), abs(y1 - y0))
                    if height < width * 6:
                        continue

                    # 本の幅は画像の1/10以下
                    if width > max(target_img.shape[1], target_img.shape[0]) / 10:
                        continue

                    score = np.log(1 + np.abs(total_mask - mask_img[y0:y1, x0:x1].sum())) + np.log(1 + max(0, ((y1 - y0) * (x1 - x0) - total_mask * 2)))
                    if score < best_score:
                        best_score = score
                        best_rect = (x0, y0, x1, y1)

    target_img = target_img.copy()
    y0 = (best_rect[1] + best_rect[3]) // 2
    y1 = min(y0 + 100, target_img.shape[0])
    x0 = (best_rect[0] + best_rect[2]) // 2
    x1 = min(x0 + 100, target_img.shape[1])

    cvArrow(target_img, (x1, y1), (x0, y0), (0, 0, 255), thickness=10)

    os.makedirs(os.path.dirname(args.result_image), exist_ok=True)
    cv2.imwrite(args.result_image, target_img)

    """
    cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("segmented_image", cv2.WINDOW_NORMAL)
    cv2.imshow("original_image", resized_origin)
    cv2.imshow("mask_image", resized_dst)
    cv2.imshow("segmented_image", resized_dst2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """


def cvArrow(img, pt1, pt2, color, thickness=1, lineType=8, shift=0):
    cv2.line(img, pt1, pt2, color, thickness, lineType, shift)
    vx = pt2[0] - pt1[0]
    vy = pt2[1] - pt1[1]
    v = math.sqrt(vx ** 2 + vy ** 2)
    ux = vx / v
    uy = vy / v
    # 矢印の幅の部分
    w = 20
    h = 30
    ptl = (int(pt2[0] - uy * w - ux * h), int(pt2[1] + ux * w - uy * h))
    ptr = (int(pt2[0] + uy * w - ux * h), int(pt2[1] - ux * w - uy * h))
    # 矢印の先端を描画する
    cv2.line(img, pt2, ptl, color, thickness, lineType, shift)
    cv2.line(img, pt2, ptr, color, thickness, lineType, shift)


if __name__ == "__main__":
    main()
