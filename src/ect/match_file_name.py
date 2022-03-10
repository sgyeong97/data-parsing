import os
import sys
import shutil
from os import listdir, rename
from os.path import isfile, join
#img와 yolo 파일명을 맞추는 코드

yolo_path = 'D:\신지영_업무\dataset\\0723_dataset(아산and성남)\아산토탈\end'
image_path = 'D:\신지영_업무\dataset\\0723_dataset(아산and성남)\아산토탈\end'

img_list = []
yolo_list = []
name_list = []

for x in os.listdir(yolo_path):
    if x.endswith('.txt'):
        empty = os.path.join(yolo_path, x)
        yolo_list.append(empty)
for x in os.listdir(image_path):
    if x.endswith('.jpg'):
        empty = os.path.join(image_path, x)
        img_list.append(empty)

yolo_list.sort()
img_list.sort()
name_count = 37164
count = 0


#xml의 경우 수량이 맞지 않음
for x in range(1, len(yolo_list)):
    name = 'backgorund7_{0:06d}'.format(name_count)
    yolo_name_path = os.path.join(yolo_path,name+'.txt')
    img_name_path = os.path.join(image_path, name+'.jpg')
    rename(yolo_list[count], yolo_name_path)
    rename(img_list[count], img_name_path)
    count += 1
    name_count += 1