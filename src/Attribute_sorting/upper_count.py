import os
import xml.etree.ElementTree
from bs4 import BeautifulSoup
import cv2
import random
import shutil
import time
import numpy as np
import pandas as pd
from pandas import DataFrame

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\origin'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\\file_list.txt'
total_file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\\upper_total.xlsx'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
shortshirt_list = []
longshirt_list = []
shirtdk_list = []
total_count_list = []
type_name_list = ['shortshirt', 'longshirt', 'shirtdk']
color_name_list = ['red', 'green', 'yellow', 'blue', 'brown', 'pink', 'gray', 'black', 'white','unknown']

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
xml_count = 0

red_list = []
green_list = []
yellow_list = []
blue_list = []
brown_list = []
pink_list = []
gray_list = []
black_list = []
white_list = []
unknown_list = []

target_file_list = os.listdir(target_path)
for x in target_file_list:
    if x.endswith('png'):
        crop_img_list.append(x)
    elif x.endswith('xml'):
        xml_list.append(x)
        temp = x.split('.')
        file_name_list.append(temp[0])

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


def comparison(value):
    sort_list = value.copy()
    empty_list = value.copy()
    sort_list.sort()
    return_count = 0
    count = 0
    count_list = []
    result = []
    num_len = len(value)
    if num_len <= 3:
        for x in value:
            if sort_list[0] == x:
                return count
            else:
                count += 1
    else:
        for x in sort_list:
            count = 0
            for y in empty_list:
                if y == x:
                    result.append(str(count))
                    return_count +=1
                    empty_list.pop(count)
                    break
                else:
                    count += 1
            if return_count == 3:
                break
    return result

file_attri = []
print("xml을 읽어 속성 값 count 시작")

for xml in xml_list:
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
        str_temp = '%s' % file_name_list[xml_count]
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
                            elif label_name == 'top_yellow':
                                top_yellow += 1
                            elif label_name == 'top_green':
                                top_green += 1
                            elif label_name == 'top_blue':
                                top_blue += 1
                            elif label_name == 'top_black':
                                top_black += 1
                            elif label_name == 'top_brown':
                                top_brown += 1
                            elif label_name == 'top_pink':
                                top_pink += 1
                            elif label_name == 'top_grey':
                                top_gray += 1
                            elif label_name == 'top_white':
                                top_white += 1
                            elif label_name == 'top_color_unknown':
                                top_color_unknown += 1

    xml_count += 1

total_list = [longshirt, shortshirt, shirtdk, top_brown, top_red, top_yellow, top_green, top_blue, top_pink, top_gray, top_black, top_white, top_color_unknown]
total_count_list= [longshirt, shortshirt, shirtdk, top_brown,top_red, top_yellow, top_green, top_blue,top_pink, top_gray,  top_black, top_white, top_color_unknown]
total_name_list = ['longshirt', 'shortshirt', 'shirtdk', 'top_brown', 'top_red', 'top_yellow', 'top_green', 'top_blue', 'top_pink', 'top_gray','top_black', 'top_white', 'top_color_unknown']
df = pd.DataFrame(
    {
        "COUNT" : total_list
    }, index = total_name_list
)
df.to_excel(total_file_path)
