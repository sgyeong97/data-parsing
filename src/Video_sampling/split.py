import os
import sys
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import listdir
from os.path import isfile, join

root_dir = r"D:\신지영_업무\아산"
result_dir = r"D:\신지영_업무\아산\Videos"
split_video_dir = r"D:\신지영_업무\아산\분류"
info_txt = "D:\신지영_업무\아산\split_info.txt"
dir_name_list = []
dir_list = []
split_list = []
temp_list = []
fail_video_list = []

total_person = 0
total_rain = 0
total_car = 0
total_none = 0
total_background = 0
total_count = 0
create_video_count = 0
fail_video_count = 0

f = open(info_txt, 'r', encoding='utf-8')
lines = ''
while True:
    line = f.readline()
    if not line : break
    lines += line
f.close()

temp_list = lines.split(')')

for x in temp_list:
    try:
        temp, temp2 = x.split(']')
        temp3, temp4 = temp.split('[')
        dir_name_list.append(temp4)
        dir_list.append(os.path.join(split_video_dir,temp4))
        temp5 = str(temp2).splitlines()
        split_list.append(temp5[1:])
    except:
        pass

#file_path = ('D:\신지영_업무\아산\분류\가내1리-마을입구_고정1\\2019_C_가내1리-마을입구_고정1_KT^20200610-083000-20200610-084000.avi')
#result_path = 'D:\신지영_업무\아산\\test.avi'
#ffmpeg_extract_subclip(file_path, 00, 60, targetname=result_path)
limit = len(dir_name_list)
for x in range(0, len(dir_name_list)):
    count = 0
    print("%d/%d"%(total_count, limit))
    total_count += 1
    for y in split_list[x]:
        if y.startswith('"') and y.endswith('"'):
            file_name = y[1:-1]
            if file_name.endswith('.avi'):
                file_path = os.path.join(dir_list[x], file_name)
            else:
                try:
                    file_path = os.path.join(dir_list[x],file_name+'.avi')
                except:
                    pass
                    #input()
        else:
            if y.startswith('#'):
                start_time = end_time = 0
                trush, cont_type = y.split('#')
                total_none += 1
            elif y == 'none':
                start_time = 0
                end_time = 0
                count_type = 'none'
                total_none += 1
            else:
                try:
                    start_time, end_time, cont_type= y.split(',')
                    if cont_type == 'person':
                        total_person += 1
                    elif cont_type == 'rain':
                        total_rain += 1
                    elif cont_type == 'background':
                        total_background += 1
                    elif cont_type == 'car':
                        total_car += 1
                    s_temp = start_time.split(':')
                    e_temp = end_time.split(':')
                    if len(s_temp) == 3:
                        s_temp1 = int(s_temp[1])*60
                        s_temp2 = int(s_temp[2])
                        e_temp1 = int(e_temp[1])*60
                        e_temp2 = int(e_temp[2])
                    else:
                        s_temp1 = int(s_temp[0])*60
                        s_temp2 = int(s_temp[1])
                        e_temp1 = int(e_temp[0])*60
                        e_temp2 = int(e_temp[1])
                    start_time = int(s_temp1+s_temp2)
                    end_time = int(e_temp1+e_temp2)
                except:
                    fail_video_count += 1
                    fail_video_list.append('문자열 split 문제'+file_path)
                    break
                    pass
            result_path = os.path.join(result_dir, dir_name_list[x]+'_%d(%s).avi'%(count, cont_type))
            try:
                ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=result_path)
                create_video_count += 1
            except:
                fail_video_list.append(file_path)
                fail_video_count += 1
                break
                #print(file_path)
                #input()
            count += 1
txt_path = os.path.join(root_dir, "class_count_info.txt")
fail_list_txt = os.path.join(root_dir, "fail_split_video_info.txt")
writefile = open(txt_path, 'w')
writefile.write("<TOTAL COUNT>\nPerson = %d\nCar = %d\nRain = %d\nBackground = %d\nNone = %d\n생성된 영상 수 = %d" %
                (total_person, total_car, total_rain, total_background, total_none, create_video_count))
writefile.close()
writefile = open(fail_list_txt, 'w')
writefile.write("<Fail Video lists>\n")
for x in fail_video_list:
    writefile.write(x+'\n')
writefile.write('실패 영상 수 = %d'%fail_video_count)
writefile.close()