#coding: utf-8
import numpy as np
import cv2

def line_detect(book_img, target_img, drawn_img):

    height = len(book_img)
    width = len(book_img[0])
    channels = len(book_img[0][0])

    #gray scale画像
    gray = cv2.cvtColor(target_img,cv2.COLOR_BGR2GRAY)

    #edge検出
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    #ハフ変換
    lines = cv2.HoughLines(edges,1,np.pi/180,200)

    #直線検出
    cnt = 0
    delta = 500
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
                cv2.line(drawn_img,(x1,y1),(x2,y2),(255,255,255),10)
            cnt += 1
            if cnt > 100:
                break
            print("line was drawn\n")

    return drawn_img

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
