#coding: utf-8
import numpy as np
import cv2

def line_detect2(book_img, target_img, drawn_img):

    height = len(book_img)
    width = len(book_img[0])
    channels = len(book_img[0][0])

    #gray scale画像
    gray = cv2.cvtColor(target_img,cv2.COLOR_BGR2GRAY)

    #edge検出
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLinesP(edges, rho=5, theta=math.pi / 180.0 * 90,
                            threshold=200, minLineLength=30, maxLineGap=5)
    # Draw detected segments on the original image.
    if lines is not None:
        for (x1, y1, x2, y2) in lines[0]:
            cv2.line(drawn_image, (x1, y1), (x2, y2), (0, 255, 0), 1)

    return drawn_image

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
    #探したい本の表紙画像を読み込み
    book_img = cv2.imread('./images/0.jpg', 1)
    target_img = cv2.imread('./images/target4.jpg', 1)

    target_img = line_detect(book_img, target_img, target_img)

    #画像の表示
    resized_dst = cv2.resize(target_img, (int(target_img.shape[0]/3), int(target_img.shape[1]/3)))
    cv2.namedWindow("edge_detected_image", cv2.WINDOW_NORMAL)
    cv2.imshow("edge_detected_image", resized_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
