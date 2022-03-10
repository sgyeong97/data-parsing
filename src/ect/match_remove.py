import os
import sys
from os import listdir
from os.path import isfile, join
#jpg와 xml파일명을 비교하여 xml파일이 없는 jpg파일을 제거하는 코드

rm_dir = r'D:\신지영_업무\dataset\0723_dataset(아산and성남)\아산토탈\end\Images'
txt_list = []
jpg_list = []
txt_name_list = []
jpg_name_list = []

temp = os.listdir(rm_dir)

for x in temp:
    try:
        file_name, file_type = x.split('.')

        if file_type == 'jpg':
            jpg_name_list.append(file_name)
        elif file_type == 'xml':
            txt_name_list.append(file_name)
    except:
        pass
for x in jpg_name_list:
    if x not in txt_name_list:
        try:
            os.remove(os.path.join(rm_dir, x+'.jpg'))
        except:
            pass