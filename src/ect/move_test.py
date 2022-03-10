import os
import xml.etree.ElementTree
import cv2
import shutil
import time

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper'
target_file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\\file_list.txt'
img_path = os.path.join(target_path, '분류용')
xml_path = os.path.join(target_path, '분류용', 'Xmls')
name_list = []
xml_list = []
file = open(target_file_path, 'r')
while True:
    line = file.readline()
    if not line: break
    temp = line.split('\n')
    path = temp[0]+'.png'
    path2 = temp[0]+'.xml'
    name_list.append(path)
    xml_list.append(path2)
file.close()
print("이동 시작")
# for file_name in name_list:
#     name_path = os.path.join(img_path, file_name)
#     move_name = os.path.join(target_path,'Test', file_name)
#     shutil.move(name_path, move_name)
for file_name in xml_list:
    name_path = os.path.join(xml_path, file_name)
    move_name = os.path.join(target_path,'Test','Xmls', file_name)
    shutil.move(name_path, move_name)

print("이동 끝")
print(time.time()-start)