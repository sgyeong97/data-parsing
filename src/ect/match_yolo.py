import os
import sys
import shutil
from os import listdir
from os.path import isfile, join
#xml이 없는 yolo 파일을 이미지 파일명과 비교하여 없는 파일을 생성하는 코드

target_path = 'D:\신지영_업무\dataset\\0723_dataset(아산and성남)\아산토탈\end'
image_path = 'D:\신지영_업무\dataset\\0723_dataset(아산and성남)\아산토탈\end'
xml_path = 'D:\신지영_업무\dataset\\0723_dataset(아산and성남)\아산토탈\end\Xmls'

img_list = []
xml_list = []
target_list = []

img_list = os.listdir(image_path)
empty = os.listdir(xml_path)

for x in empty:
    temp = x.split('.')
    xml_list.append(temp[0])

for img in img_list:
    empty = img.split('.')
    if empty[0] in xml_list:
        pass
    else:
        target_list.append(empty[0])

for x in target_list:
    path = os.path.join(target_path, x+'.txt')
    print(path)
    file = open(path, 'w')
    file.close()