"""
코드 작성일시 : 2020년 1월 11일
코드 내용 : 각종 테스트를 위한 임시코드들
"""
import os

path = './test_image'

for root, dirs, files in os.walk(path):
    for fname in files:
        full_fname = os.path.join(root, fname)

        print(full_fname)
        # print(len(full_fname))

print("other code")

file_list = os.listdir(path)
print("file_list: {}".format(file_list))
print("file_count: {}".format(len(file_list)))