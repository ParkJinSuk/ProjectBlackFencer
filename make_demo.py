import cv2
import os
import numpy as np
import DataPreProcess as dpp

path_read_frame = './demo_road'
path_read_het = './demo_het'

path_write = './demo_save'

# 파일리스트 읽어오기
file_list_read_frame = os.listdir(path_read_frame)
file_list_read_het = os.listdir(path_read_het)
file_list_write = os.listdir(path_write)

for i in range(len(file_list_read_frame)):
    frame = cv2.imread("demo_road/" + file_list_read_frame[i])  # 이미지 읽기
    frame_het = cv2.imread("demo_het/" + file_list_read_het[i])  # 이미지 읽기

    ##### 이미지 전처리 과정 ###########
    _frame = dpp.filter_sobel(frame) # 차선검출

    frame_het = cv2.GaussianBlur(frame_het, (5, 5), 0) # 온도이미지 가우시안블러
    frame_display = cv2.add(_frame, frame_het)


    # 이미지 저장
    # cv2.imwrite("train_image/"+file_list_read[i], line_image)

    # 변환 중인 이미지 보여줌
    cv2.imshow("frame", frame)
    cv2.imshow('frame_het', frame_het)
    cv2.imshow('display', frame_display)
    cv2.waitKey(0)

    # 변환 진행과정 표시
    print("{} of {}".format(i + 1, len(file_list_read_frame) + 1))