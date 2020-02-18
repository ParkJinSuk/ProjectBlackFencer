import cv2
import os
import numpy as np
import DataPreProcess as dpp
import csv
import time


path_read_frame = './demo_road'
path_read_het = './demo_het'
path_read_het_data = './demo_het_data'
path_write = './demo_save'
path_read_yolo = 'demo_yolo.csv'

# 파일리스트 읽어오기
file_list_read_frame = os.listdir(path_read_frame)
file_list_read_het = os.listdir(path_read_het)
file_list_read_het_data = os.listdir(path_read_het_data)
file_list_write = os.listdir(path_write)

# 온도 csv 파일 읽어오기
with open('demo_yolo.csv', encoding='UTF8') as file:
    csv_data = []
    for line in file.readlines():
        line = line.strip()
        csv_data.append(line.split(','))
#print("yolo 시작프레임번호 : ", csv_data[0][0])
#print("yolo 끝프레임번호 : ", csv_data[96][0])

for i in range(97):
    for j in range(5):
        csv_data[i][j] = int(csv_data[i][j])
csv_data = np.array(csv_data)


'''
# 온도 txt 파일 읽어오기
for i in range(len(file_list_read_het_data)):
    with open('demo_het_data/' + file_list_read_het_data[i], encoding='UTF8') as file:
        hetdata = []
        for line in file.readlines():
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.strip()
            hetdata.append(line.split())
    for x in range(32):
        for y in range(24):
            hetdata[x][y] = int(hetdata[x][y])
    hetdata = np.array(hetdata)
    print(hetdata)
'''

for i in range(len(file_list_read_frame)):

    frame = cv2.imread("demo_road/" + file_list_read_frame[i])  # 이미지 읽기
    frame_het = cv2.imread("demo_het/" + file_list_read_het[i])  # 이미지 읽기

    ##### 온도 이미지 생성 #############
    # 온도 txt 파일 읽어오기
    hetdata = []
    with open('demo_het_data/' + file_list_read_het_data[i], encoding='UTF8') as file:
        for line in file.readlines():
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.strip()
            hetdata.append(line.split())
    for x in range(32):
        for y in range(24):
            hetdata[x][y] = int(hetdata[x][y]) - 15
    hetdata = np.array(hetdata)
    #print(hetdata)
    image_het = dpp.het_arr2img(hetdata)
    frame_het = dpp.image_het_mapping(image_het)
    #print(image_het)
    ##### 이미지 전처리 과정 ###########
    _frame = dpp.filter_sobel(frame) # 차선검출


    frame_het = cv2.GaussianBlur(frame_het, (5, 5), 0) # 온도이미지 가우시안블러
    frame_display = cv2.add(_frame, frame_het)

    '''
    # yolo 좌표값 발생히면 이미지 처리
    for num in range(97):
        if i == csv_data[num][0]:
            yolo_loaction = [csv_data[num][1], csv_data[num][2], csv_data[num][3], csv_data[num][4]]
            list_yolo = dpp.yolo_arr2flat(yolo_loaction)
            list_het = dpp.image_het2flat(frame_het)
            list_blackice = dpp.Find_BlackIce(list_het, list_yolo)
            frame_blackice = dpp.image_blackice(list_blackice)
            cv2.imshow('blaic', frame_blackice)
            frame_display = dpp.image_object(frame_display, csv_data[num][1], csv_data[num][2], csv_data[num][3], csv_data[num][4])
    '''
    # 이미지 저장
    # cv2.imwrite("train_image/"+file_list_read[i], line_image)

    # 변환 중인 이미지 보여줌
    cv2.imshow("het image", image_het)
    #cv2.imshow("frame", frame)
    #cv2.imshow('frame_het', frame_het)
    cv2.imshow('display', frame_display)
    cv2.waitKey(2)

    # 변환 진행과정 표시
    print("{} of {}".format(i + 1, len(file_list_read_frame) + 1))

print("######## end ##########")