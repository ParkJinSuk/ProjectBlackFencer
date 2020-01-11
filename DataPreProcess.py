"""
코드 작성일시 : 2020년 1월 11일
작성자 : Park Jinsuk
코드 내용 : 특정색깔을 검출하기 위한 함수들을 작성
"""

import cv2

# 색상 범위 - HSV - 색상(Hue), 채도(Saturation), 명도(Value)
lower_orange = (8, 50, 50)
upper_orange = (20, 255, 255)

lower_white = (0, 0, 210)
upper_white = (255, 255, 255)


# 차선의 주황색을 검출하기 위한 함수 #
def find_line_orange(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선의 하얀색을 검출하기 위한 함수 #
def find_line_white(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위를 제한하여 mask 생성
    img_mask = cv2.inRange(img_hsv, lower_white, upper_white)

    # 원본 이미지를 가지고 Object 추출 이미지로 생성
    img_result = cv2.bitwise_and(img, img, mask=img_mask)

    return img_result


# 차선들의 이미지를 합치고 하늘배경을 제거하는 함수 #
# img1, img2 인자는 합성할 이미지
# pixel 은 이미지 위에서부터 제거할 픽셀수
def merge_lines(img1, img2, pixel):
    img_result = cv2.bitwise_or(img1, img2)

    for i in range(pixel):
        for j in range(160):
            img_result[i, j] = [0, 0, 0]  # 검은색으로 채움

    return img_result
