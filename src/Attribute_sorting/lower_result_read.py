import os
import xml.etree.ElementTree
import cv2
import shutil
import time
import numpy as np
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\lower\Origin/Xmls'
target_file = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\lower\\file_list.txt'
result_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\lower'

start = time.time()

longpants = 0
shortpants = 0
longskirt = 0
shortskirt = 0
lowerdk = 0
s_red = 0
s_yellow = 0
s_green = 0
s_blue = 0
s_brown = 0
s_pink = 0
s_gray = 0
s_black = 0
s_white = 0
s_unknown = 0
l_red = 0
l_yellow = 0
l_green = 0
l_blue = 0
l_brown = 0
l_pink = 0
l_gray = 0
l_black = 0
l_white = 0
l_unknown = 0
crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
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
                        if label_name == 'shoes_color':
                            if result == 'shoes_red':
                                s_red += 1
                            if result == 'shoes_yellow':
                                s_yellow += 1
                            if result == 'shoes_green':
                                s_green += 1
                            if result == 'shoes_blue':
                                s_blue += 1
                            if result == 'shoes_brown':
                                s_brown += 1
                            if result == 'shoes_pink':
                                s_pink += 1
                            if result == 'shoes_grey':
                                s_gray += 1
                            if result == 'shoes_black':
                                s_black += 1
                            if result == 'shoes_white':
                                s_white += 1
                            if result == 'shoes_unknown':
                                s_unknown += 1
                        elif label_name == 'bottom':
                            if result == 'long_pants':
                                longpants += 1
                            if result == 'short_pants':
                                shortpants += 1
                            if result == 'long_skirt':
                                longskirt += 1
                            if result == 'short_skirt':
                                shortskirt += 1
                            if result == 'unknown' :
                                lowerdk += 1
                        else:
                            if label_name == 'bottom_red':
                                l_red += 1
                            if label_name == 'bottom_yellow':
                                l_yellow += 1
                            if label_name == 'bottom_green':
                                l_green += 1
                            if label_name == 'bottom_blue':
                                l_blue += 1
                            if label_name == 'bottom_brown':
                                l_brown += 1
                            if label_name == 'bottom_pink':
                                l_pink += 1
                            if label_name == 'bottom_grey':
                                l_gray += 1
                            if label_name == 'bottom_black':
                                l_black += 1
                            if label_name == 'bottom_white':
                                l_white += 1
                            if label_name == 'bottom_color_unknown':
                                l_unknown += 1
    xml_count += 1

total_list = [longpants, shortpants, longskirt, shortskirt, lowerdk, l_red, l_yellow, l_green,
              l_blue, l_brown, l_pink, l_gray, l_black, l_white, l_unknown, s_red, s_yellow,
              s_green, s_blue, s_brown, s_pink, s_gray, s_black, s_white, s_unknown]
total_name_list = ['longpants', 'shortpants', 'longskirt', 'shortskirt', 'lowerdk', 'l_red', 'l_yellow', 'l_green',
              'l_blue', 'l_brown', 'l_pink', 'l_gray', 'l_black', 'l_white', 'l_unknown', 's_red', 's_yellow',
              's_green', 's_blue', 's_brown', 's_pink', 's_gray', 's_black', 's_white', 's_unknown']

df = pd.DataFrame(
    {
        "COUNT" : total_list
    },index=total_name_list
)

txt_file = os.path.join(result_path, 'lower_result.xlsx')
df.to_excel(txt_file)