import os
import xml.etree.ElementTree
import cv2
import shutil
import time
import numpy as np
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\head\Origin\Xmls'
target_file = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\head\\file_list.txt'
result_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\head'

start = time.time()

cap = 0
visor = 0
nonvisor = 0
helmat = 0
hood = 0
nohat = 0
hatdk = 0
hatred = 0
hatyellow = 0
hatgreen = 0
hatblue = 0
hatbrwon = 0
hatpink = 0
hatgray = 0
hatblack = 0
hatwhite = 0
unknown = 0
short = 0
long = 0
bald = 0
hairdk = 0
xml_count = 0

xml_list = []

def split_label(label):
    temp = str(label)
    temp0 = temp.split('<')
    temp1, result = temp0[1].split('>')
    return result


def split_name(name):
    temp = str(name)
    try:
        temp0 = temp.split("\"")
        result = temp0[1]
    except:
        return False
    return result

name_list = []
file = open(target_file, 'r')
while True:
    line = file.readline()
    if not line: break
    temp = line.split('\n')
    path = os.path.join(target_path, temp[0]+'.xml')
    name_list.append(path)
file.close()

for xml in name_list:
    if xml.endswith('xml'):
        xml_path = os.path.join(target_path, xml)
        file = open(xml_path, 'r', encoding='utf-8')
        lines = ''
        while True:
            line = file.readline()
            if not line: break
            lines += line
        file.close()
        bs = BeautifulSoup(lines, 'lxml')
        temp = []
        temp_str = ''
        for box in bs.find_all('box'):
            label = 'head'
            lines = str(box).splitlines()
            for x in lines[1:]:
                result = split_label(x)
                if result != 'false':
                    label_name = split_name(x)
                    if label_name:
                        if label_name == 'hat':
                            if result == 'cap':
                                cap += 1
                            elif result == 'brimmed':
                                visor += 1
                            elif result == 'brimless':
                                nonvisor += 1
                            elif result == 'helmat':
                                helmat += 1
                            elif result == 'hood':
                                hood += 1
                            elif result == 'hatless':
                                nohat += 1
                            else:
                                hatdk += 1
                        elif label_name == 'hair':
                            if result == 'long':
                                long += 1
                            elif result == 'short':
                                short += 1
                            elif result == 'bald':
                                bald += 1
                            else:
                                hairdk += 1
                        else:
                            if label_name == 'hat_red':
                                hatred += 1
                            elif label_name == 'hat_yellow':
                                hatyellow += 1
                            elif label_name == 'hat_green':
                                hatgreen += 1
                            elif label_name == 'hat_blue':
                                hatblue += 1
                            elif label_name == 'hat_brown':
                                hatbrwon += 1
                            elif label_name == 'hat_black':
                                hatblack += 1
                            elif label_name == 'hat_grey':
                                hatgray += 1
                            elif label_name == 'hat_white':
                                hatwhite += 1
                            elif label_name == 'hat_pink':
                                hatpink += 1
                            elif label_name == 'hat_color_unknown':
                                unknown += 1

total_list = [cap,visor,nonvisor,helmat,hood,nohat,hatdk,hatred,hatyellow,hatgreen,hatblue,hatbrwon,hatpink,hatgray,hatblack,hatwhite,unknown,short,long,bald, hairdk]
total_name_list = ['cap', 'visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrwon','hatpink','hatgray','hatblack','hatwhite','unknown','short','long','bald', 'hairdk']

df = pd.DataFrame(
    {
        "COUNT" : total_list
    },index=total_name_list
)

txt_file = os.path.join(result_path, 'head_result.xlsx')
df.to_excel(txt_file)

print(time.time() - start)
