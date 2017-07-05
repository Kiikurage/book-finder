# coding: utf-8
import math

import cv2
import numpy as np


def line_detect(book_img, target_img, drawn_img):
    # gray scale画像
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    # edge検出
    edges = cv2.Canny(gray, 150, 150, apertureSize=3)
    cv2.imwrite("./edges.jpg", edges)
    # exit(0)

    # ハフ変換
    lines = cv2.HoughLines(edges, 1, np.pi / 360, 200)
    if lines is None:
        return drawn_img.copy(), np.array([])

    # 直線検出
    cnt = 0
    coord_list = []

    drawn_img = target_img.copy()
    lines = list(lines[:, 0, :])

    while len(lines) > 0:
        rho, theta = lines.pop(0)
        if rho == 777:
            continue
        a = np.cos(theta)
        b = np.sin(theta)

        if b == 0:
            y0 = y1 = rho
            x0 = 0
            x1 = drawn_img.shape[1]

        elif a == 0:
            x0 = x1 = rho
            y0 = 0
            y1 = drawn_img.shape[0]

        else:
            y0 = min(max(int(rho / b), 0), drawn_img.shape[0])
            y1 = min(max(int((rho - a * drawn_img.shape[1]) / b), 0), drawn_img.shape[0])
            x0 = min(max(int((rho - b * y0) / a), 0), drawn_img.shape[1])
            x1 = min(max(int((rho - b * y1) / a), 0), drawn_img.shape[1])

        coord_list.append([x0, y0, x1, y1, rho, theta, a, b])
        cv2.line(drawn_img, (x0, y0), (x1, y1), (255, 255, 255), 5)

        for i, (rho2, theta2) in enumerate(lines):
            THRESHOLD_THETA = np.pi / 180 * 5
            THRESHOLD_RHO = ((target_img.shape[0] ** 2 + drawn_img.shape[1] ** 2) ** 0.5) * 0.01
            if abs(theta - theta2) <= THRESHOLD_THETA and abs(rho - rho2) <= THRESHOLD_RHO:
                lines[i][0] = 777

        cnt += 1
        if cnt > 100:
            break

    cv2.imwrite("./lined.jpg", drawn_img)

    return drawn_img, coord_list


def line_detect2(book_img, target_img, drawn_img):
    height = len(book_img)
    width = len(book_img[0])
    channels = len(book_img[0][0])

    # gray scale画像
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    # edge検出
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, rho=5, theta=math.pi / 180.0 * 90,
                            threshold=200, minLineLength=30, maxLineGap=5)
    # Draw detected segments on the original image.
    if lines is not None:
        cnt = 0
        for x1, y1, x2, y2 in lines[:, 0, :]:
            if cnt > 100:
                break
            cv2.line(drawn_img, (x1, y1), (x2, y2), (255, 255, 255), 10)
            cnt += 1

    return drawn_img

    """
    if lines is not None:
        for rho,theta in lines[:, 0, :]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            if (x1 - x2) ** 2 < delta * delta:
                #print(x1, y1, x2, y2)
                cv2.line(drawn_img,(x1,y1),(x2,y2),(255,255,255),10)
                coord_list.append([x1, y1, x2, y2])
            cnt += 1
            if cnt > 100:
                break
    return drawn_img, np.array(coord_list)
    #return x1, y1, x2, y2, drawn_img
    """


def main():
    # 探したい本の表紙画像を読み込み
    book_img = cv2.imread('./images/0.jpg', 1)
    target_img = cv2.imread('./images/target4.jpg', 1)

    target_img = line_detect(book_img, target_img, target_img)

    # 画像の表示
    resized_dst = cv2.resize(target_img, (int(target_img.shape[0] / 3), int(target_img.shape[1] / 3)))
    cv2.namedWindow("edge_detected_image", cv2.WINDOW_NORMAL)
    cv2.imshow("edge_detected_image", resized_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
