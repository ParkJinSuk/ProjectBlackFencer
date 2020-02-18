import cv2
import os
import numpy as np
import DataPreProcess as dpp
import csv
import time


path_read_frame = './demo_save'
file_list_frame = os.listdir(path_read_frame)

for i in range(len(file_list_frame)):
     print("frame{}".format(i+1))
     frame = cv2.imread("demo_save/" + file_list_frame[i])  # 이미지 읽기
     frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC)

     cv2.imshow("frame", frame)
     if 0 <= i < 500:
          cv2.waitKey(10)
     elif 500 <= i < 750:
          cv2.waitKey(40)
     elif 750 <= i < 900:
          cv2.waitKey(80)
     elif 900 <= i < 1000:
          cv2.waitKey(20)
     elif 1000 <= i < 1250:
          cv2.waitKey(80)
     elif 1250 <= i < 2100:
          cv2.waitKey(10)
     # elif i > 1100:
     #      cv2.waitKey(80)
     # elif i > 1500:
     #      cv2.waitKey(5)
     else:
          cv2.waitKey(0)

cv2.destroyAllWindows()