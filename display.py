'''

코드 내용 : 라즈베리파이 디스플레이에 보여줄 영상처리
Lane_detect_sobel.py 리메이크
[수정 - 2020년1월20일]
 - het iamge image 합성함수 추가
 - yolo박스 image 합성함수 추가
'''

import cv2
import numpy as np
import os
import time  # 시간 측정을 위한 라이브러

def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅
    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def filter_edge(img):
    height, width = img.shape[:2]  # 이미지 높이, 너비

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, 45),
          (width, 45),
          (width, height)]],
        dtype=np.int32)

    img = region_of_interest(img, vertices)  # ROI 설정

    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    img = cv2.convertScaleAbs(img)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2HLS)

    return img

# 온도센서로부터 이미지를 받아서 특정좌표에 이미지 합성
def image_het(img, img_het, center_x, center_y):
    w = 80
    h = 50

    # ROI 영역
    vertices = np.array(
        [[(center_x - w/2, center_y - h/2),
          (center_x - w/2, center_y + h/2),
          (center_x + w/2, center_y + h/2),
          (center_x + w/2, center_y - h/2)]],
        dtype=np.int32)
    cv2.fillPoly(img, vertices, (0, 0, 0))

    roi_het = img[center_y - 25: center_y + 25, center_x - 40: center_x + 40]
    img_het = cv2.resize(img_het, (w, h), interpolation=cv2.INTER_CUBIC)
    _img_roi = cv2.add(img_het, roi_het)
    np.copyto(roi_het, _img_roi)

    return img

# yolo에서 받은 좌표와 물체크기를 이미지 합성
def image_object(img, center_x, center_y, width, height):

    # ROI 영역
    vertices = np.array(
        [[(center_x - width / 2, center_y - height / 2),
          (center_x - width / 2, center_y + height / 2),
          (center_x + width / 2, center_y + height / 2),
          (center_x + width / 2, center_y - height / 2)]],
        dtype=np.int32)
    cv2.fillPoly(img, vertices, (255, 255, 0))

    return img

def display():
    print("## function display start ##")

    # 파일리스트 읽어오기
    path_read = './test_image2'
    file_list_read = os.listdir(path_read)
    process_time = time.time()  # 프로세스 진행시간 측정

    # ## 임시방편 임의의 온도배열 생성 12x6
    # hetadata = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #                      [10, 20, 30, 40, 50, 60, 70, 80, 90, 10, 11, 12],
    #                      [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]])
    het_image = cv2.imread("het_image.JPG")

    for i in range(len(file_list_read)):
        one_process_time = time.time()  # 프로세스 하나 진행시간 측정

        image = cv2.imread("test_image2/" + file_list_read[i])  # 이미지 읽기

        img = filter_edge(image)
        img = cv2.resize(img, (800, 480), interpolation=cv2.INTER_CUBIC)

        # 이미지 좀더 선명하게 처리 #######
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, np.array([0, 0, 100]), np.array([255, 255, 255]))
        img_2 = cv2.bitwise_and(img, img, mask=mask)
        ###################################

        # 온도 이미지 합성
        img_het = image_het(img_2, het_image, 300, 300)
        img_het_object = image_object(img_het, 300, 200, 100, 50)

        #cv2.imshow('그냥 이미지', img)
        cv2.imshow('het image', img_het_object)
        print("{} of {} : {}\ttime : {}".format(i + 1, len(file_list_read) + 1, file_list_read[i],
                                                round(time.time() - one_process_time, 4)))

        cv2.waitKey(0)

    print("process total time : {}".format(time.time() - process_time))  # 프로세스 진행시간 표시



if __name__ == '__main__':
    print("##### main start #####")

    display()

    print("#### main end ####")