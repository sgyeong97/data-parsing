import os
import xml.etree.ElementTree
import cv2
import shutil
import time
import numpy as np
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Origin'
target_file = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\\file_list.txt'
result_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper'
xml_list_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Origin\Xmls'
start = time.time()

shortshirt = 0
longshirt = 0
shirtdk = 0
top_red = 0
top_green = 0
top_yellow = 0
top_blue = 0
top_brown = 0
top_pink = 0
top_gray = 0
top_black = 0
top_white = 0
top_color_unknown = 0
total_count = 0

type_name_list = ['longshirt', 'shortshirt', 'shirtdk']
color_name_list = ['top_brown', 'top_red', 'top_yellow', 'top_green', 'top_blue', 'top_pink','top_gray', 'top_black', 'top_white', 'top_color_unknown']
total_count_list = []


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


file = open(target_file, 'r')
name_list = []
while True:
    line = file.readline()
    if not line: break
    if line.startswith('#'):
        for x in line.split(','):
            if x == '#':
                pass
            else:
                total_count_list.append(x)
    else:
        temp = line.split('\n')
        name_list.append(temp[0])
file.close()

for name in name_list:
    xml_path = os.path.join(xml_list_path, name + '.xml')
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
        label = 'upper'
        lines = str(box).splitlines()
        for x in lines[1:]:
            result = split_label(x)
            if result != 'false':
                label_name = split_name(x)
                if label_name:
                    if label_name == 'top':
                        if result == 'short_sleeve':
                            shortshirt += 1
                        elif result == 'long_sleeve':
                            longshirt += 1
                        else:
                            shirtdk += 1
                    else:
                        if label_name == 'top_red':
                            top_red += 1
                        if label_name == 'top_yellow':
                            top_yellow += 1
                        if label_name == 'top_green':
                            top_green += 1
                        if label_name == 'top_blue':
                            top_blue += 1
                        if label_name == 'top_black':
                            top_black += 1
                        if label_name == 'top_brown':
                            top_brown += 1
                        if label_name == 'top_pink':
                            top_pink += 1
                        if label_name == 'top_grey':
                            top_gray += 1
                        if label_name == 'top_white':
                            top_white += 1
                        if label_name == 'top_color_unknown':
                            top_color_unknown += 1

df = pd.DataFrame(
    {
        "RESULT_COUNT": [longshirt, shortshirt, shirtdk, top_brown, top_red, top_yellow, top_green, top_blue,top_pink, top_gray, top_black, top_white, top_color_unknown]

    }, index=[type_name_list + color_name_list])

txt_file = os.path.join(result_path, 'upper_result.xlsx')
df.to_excel(txt_file)

print(time.time() - start)
