"""
코드 작성일시 : 2020년 1월 11일
작성자 : Park Jinsuk
코드 내용 : 특정색깔을 검출하기 위한 함수들을 작성

수정 날짜 : 2020년 1월 12일
           추가 = 머신러닝을 위한 이미지 전처리 함수 작성
"""

import cv2
import os
import numpy as np

# 색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

lower_white = (0, 0, 210)
upper_white = (255, 255, 255)

# ROI 설정하는 함수 (ROI영역이 사각형이 아니더라도 가능함)
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

def filter_canny(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    img = cv2.Canny(img, threshold1=150, threshold2=100)
    img = cv2.GaussianBlur(img, (5, 5), 0)

    for i in range(120):
        for j in range(640):
            img[i, j] = 0  # 검은색으로 채움
    return img

def filter_sobel(img):
    height, width = img.shape[:2]  # 이미지 높이, 너비

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 입력 받은 화면 Gray로 변환
    height_cut = 150

    # ROI 영역
    vertices = np.array(
        [[(0, height),
          (0, height_cut),
          (width, height_cut),
          (width, height)]],
        dtype=np.int32)

    img = region_of_interest(img, vertices)  # ROI 설정

    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    img = cv2.convertScaleAbs(img)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2HLS)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, np.array([0, 0, 40]), np.array([255, 255, 255]))
    img = cv2.bitwise_and(img, img, mask=mask)

    return img

# yolo에서 받은 좌표와 물체크기를 이미지 합성
def image_object(img, center_x, center_y, width, height):
    center_x = int(center_x)
    center_y = int(center_y)

    width_half = int(width) / 2
    height_half = int(height) / 2

    # ROI 영역
    vertices = np.array(
        [[(center_x - width_half, center_y - height_half),
          (center_x - width_half, center_y + height_half),
          (center_x + width_half, center_y + height_half),
          (center_x + width_half, center_y - height_half)]],
        dtype=np.int32)
    cv2.fillPoly(img, vertices, (255, 255, 0))

    return img

def yolo_arr2flat(yolo_location):
    '''
    yolo좌표(중심높이좌표, 중심너비좌표, 가로길이, 세로길이)
    를 받아서 한줄로 flat하게 만들어 주는 함수
    :param yolo_location: yolo로부터 받는 좌표
    :return: flat yolo데이터
    '''
    x = yolo_location[0] # 위에서 아래로 중심 높이
    y = yolo_location[1] # 왼쪽에서 오른쪽으로 중심 너비
    w = yolo_location[2]
    h = yolo_location[3]

    width = 640
    height = 480

    flat_yolo = np.zeros((width*height), dtype=np.int8)

    for i in range(10):
        for j in range(10):
            if (i+1 >= x-h/2) and (i+1 <= x+h/2):
                if (j+1 >= y-w/2) and (j+1 <= y+w/2):
                    flat_yolo[i*width + j] = 1

    return flat_yolo

def image_het2flat(image_het):
    '''
    카메라 이미지에 mapping이 된 온도이미지를
    한줄로 flat하게 만들어주는 함수
    :param image_het: mapping이 된 온도이미지
    :return: flat 온도데이터
    '''

    width = 640
    height = 480

    img_het = cv2.resize(image_het, (width, height), interpolation=cv2.INTER_CUBIC)
    result = np.zeros((width * height), dtype=np.int8)

    for i in range(height):
        for j in range(width):
            if img_het[i, j] is (255, 100, 100):
                result[i*width + j] = (1)
            elif img_het[i, j] is (255, 200, 200):
                result[i*width + j] = (1)
            elif img_het[i, j] is (255, 255, 255):
                result[i*width + j] = (1)
            else:
                result[i*width + j] = (0)

    return result

def Find_BlackIce(het, yolo):
    '''
    flat형식의 온도데이터(het), yolo좌표(yolo)의 데이터를
    인덱스를 비교해가면서 둘다 1일때, 블랙아이스 리스트의
    값을 0에서 1로 바꿔준다.
    :param het: flat 온도데이터
    :param yolo: flat yolo데이터
    :return: flat 블랙아이스
    '''

    width = 640
    height = 480

    blackice = np.zeros((width*height), dtype=np.int8)
    #print(het[4], yolo[4])
    #print(het[4].dtype, yolo[4].dtype)
    for index in range(len(het)):
        if (het[index] is 1) and (yolo[index] is 1):
            blackice[index] = 1
            #print(blackice[index])
    #print(blackice)
    return blackice


def image_blackice(list_blackice):
    result = np.zeros(shape=(480, 640, 3), dtype="uint8")
    width = 640
    height = 480

    for i in range(height):
        for j in range(width):
            if list_blackice[i*640+j] == 1:
                result[i, j] = (255, 255, 255)
            else:
                result[i, j] = (0, 0, 0)

    return result