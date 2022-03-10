import cv2

import os
import sys
from os import listdir
from os.path import isfile, join


root_dir = 'D:\신지영_업무\아산\sampling_완료_이미지'
root_dir_list = []
root_dir_list_name = []
count_jpg = 0
total_count = 0

temp= os.listdir(root_dir)
for x in temp:
    if x == '.idea' or x == 'get_length.py' or x == 'Info' or x == '분류' or x == 'split_info(30sec).txt':
        pass
    else:
        root_dir_list.append(os.path.join(root_dir, x))
        root_dir_list_name.append(x)

count = 0
for x in root_dir_list:
    count_video = 0
    count_0_9 = 0
    count_10_19 = 0
    temp = os.listdir(x)
    count_0_9_list = []
    for y in temp:
        try:
            filename, file_type = y.split('.')
            if file_type == 'jpg':
                count_jpg += 1
            elif file_type == 'avi' or file_type == 'mp4':
                count_video += 1
                total_count += 1
                file_path = os.path.join(x, y)

                cap = cv2.VideoCapture(file_path)

                length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                length_temp = int(length/fps)
                video_length = length_temp/60

                if video_length < 10:
                    count_0_9 += 1
                    count_0_9_list.append(filename)
                else:
                    count_10_19 += 1
        except:
            pass

    '''txt_path = root_dir+"\\Info\\"+root_dir_list_name[count]+'.txt'
    writefile = open(txt_path, 'w')
    writefile.write("""<TOTAL COUNT>
영상 총 갯수 = %d
10분 미만 영상 갯수 = %d
10분 미만 영상 리스트 = %s
10분 이상 20분 미만 영상 갯수 = %d
"""%(count_video, count_0_9, count_0_9_list, count_10_19))

    writefile.close()'''
    count += 1

print(total_count)
print(count_jpg)
