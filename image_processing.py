#coding: utf-8
import numpy as np
import cv2
from color_detect import color_detect
from line_detect import line_detect, line_detect2
from segmentation import segmentation

def main():
    target = './images/target5.jpg'

    book_img = cv2.imread('./images/0.jpg', 1)
    target_img = cv2.imread(target, 1)

    mask_img, masked_target_img = color_detect(book_img, target_img)
    #masked_target_img = line_detect2(book_img, target_img, masked_target_img)
    masked_target_img, coord_list = line_detect(book_img, target_img, masked_target_img)
    sorted_index = np.argsort(coord_list[:, 0], axis=0)

    var_max = 0
    index1 = index2 = None
    indexes = None
    for index in sorted_index:
        index2 = index1
        index1 = index
        print(index2, index1)
        if index2 is not None:
            tmp = np.sum(mask_img[:, coord_list[index2][0]:coord_list[index1][0]])
            print(tmp)
            if tmp > var_max:
                var_max = tmp
                indexes = (index1, index2)

    index1, index2 = indexes
    mask3d = np.zeros(target_img.shape).astype(np.uint8)
    mask3d[:, coord_list[index2][0]:coord_list[index1][0], :] = np.ones(mask3d[:, coord_list[index2][0]:coord_list[index1][0], :].shape).astype(np.uint8)

    masked_target_img = target_img * mask3d
    segmented_img = segmentation(target_img)
    print(segmented_img.shape)
    #print(masked_target_img.dtype)

    mask = np.zeros(segmented_img.shape).astype(np.uint8)
    mask[:, coord_list[index2][0]:coord_list[index1][0]] = np.ones(mask[:, coord_list[index2][0]:coord_list[index1][0]].shape).astype(np.uint8)
    print(mask.shape)
    masked_segmented_img = segmented_img * mask

    height = len(target_img)
    width = len(target_img[0])
    buf = 50
    target_img = cv2.rectangle(target_img, (coord_list[index2][0], buf), (coord_list[index1][0], height - buf), (0, 0, 255), 20)

    #画像の表示
    resized_origin = cv2.resize(target_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
    resized_dst = cv2.resize(mask_img, (int(mask_img.shape[0]/3), int(mask_img.shape[1]/3)))
    resized_dst2 = cv2.resize(masked_segmented_img, (int(masked_segmented_img.shape[0]/3), int(masked_segmented_img.shape[1]/3)))
    cv2.namedWindow("original_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("mask_image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("segmented_image", cv2.WINDOW_NORMAL)
    cv2.imshow("original_image", resized_origin)
    cv2.imshow("mask_image", resized_dst)
    cv2.imshow("segmented_image", resized_dst2)

    cv2.waitKey(0)
    cv2.imwrite("target5.jpg", resized_origin)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
