###################################################
# 코드 작성일시 : 2020년 1월 11일
# 코드 내용 : 전반적인 코드
###################################################

import cv2
import DataPreProcess as DPP


if __name__ == '__main__':
    print("this is main")

    image = cv2.imread('test_image/1_cam-image_array_.jpg')  # 이미지 읽기

    a = DPP.find_line_orange(image)
    b = DPP.find_line_white(image)

    cv2.imshow('result', a)
    cv2.imshow('result', b)
    cv2.waitKey(0)