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

def data_preprocess():
    path_read = './demo_road'
    path_write = './train_image'

    # 파일리스트 읽어오기
    file_list_read = os.listdir(path_read)
    file_list_write = os.listdir(path_write)
    # 저장할 디덱토리 비어있지 않을 경우 예외처리
    if (len(file_list_write) != 0):
        print("데이터를 저장할 디렉토리가 비어있지 않습니다.")
        return 0

    for i in range(len(file_list_read)):
        img = cv2.imread("demo_road/"+file_list_read[i])  # 이미지 읽기


        # 이미지 전처리 과정
        img_canny = filter_canny(img)
        img_sobel = filter_sobel(img)

        # 이미지 저장
        # cv2.imwrite("train_image/"+file_list_read[i], line_image)

        # 변환 중인 이미지 보여줌
        cv2.imshow("real", img)
        cv2.imshow('canny', img_canny)
        cv2.imshow('sobel', img_sobel)
        cv2.waitKey(0)

        # 변환 진행과정 표시
        print("{} of {}".format(i+1, len(file_list_read)+1))

    print("Preprocessing Complete!")


data_preprocess()