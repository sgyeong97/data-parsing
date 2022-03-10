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

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\origin'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\\file_list.txt'
total_file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\\head_total.xlsx'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
xml_count = 0

cap = 0
visor = 0
nonvisor = 0
helmat = 0
hood = 0
nohat = 0
hatdk = 0
red = 0
yellow = 0
green = 0
blue = 0
brown = 0
pink = 0
gray = 0
black = 0
white = 0
unknown = 0
short = 0
long = 0
bald = 0
hairdk = 0

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
            label = 'head'
            lines = str(box).splitlines()
            for x in lines[1:]:
                result = split_label(x)
                if result != 'false':
                    label_name = split_name(x)
                    if label_name == 'hat':
                        if result == 'hatless':
                            nohat += 1
                        elif result == 'cap':
                            cap += 1
                        elif result == 'brimmed':
                            visor += 1
                        elif result == 'brimless':
                            nonvisor += 1
                        elif result == 'helmat':
                            helmat += 1
                        elif result == 'hood':
                            hood += 1
                        else:
                            hatdk += 1
                    elif label_name == 'hair':
                        if result == 'short':
                            short += 1
                        elif result == 'long':
                            long += 1
                        elif result == 'bald':
                            bald += 1
                        else:
                            hairdk += 1
                else:
                    if label_name == 'hat_red':
                        red += 1
                    elif label_name == 'hat_yellow':
                        yellow += 1
                    elif label_name == 'hat_green':
                        green += 1
                    elif label_name == 'hat_blue':
                        blue += 1
                    elif label_name == 'hat_brown':
                        brown += 1
                    elif label_name == 'hat_pink':
                        pink += 1
                    elif label_name == 'hat_grey':
                        gray += 1
                    elif label_name == 'hat_black':
                        black += 1
                    elif label_name == 'hat_white':
                        white += 1
                    else:
                        unknown += 1

total_list = [cap, visor, nonvisor, helmat, hood, nohat, hatdk, red, yellow, green, blue, brown, pink, gray, black, white, unknown, short, long, bald, hairdk]

df = pd.DataFrame(
    {
        "TOTAL_COUNT" : total_list
    }, index = ['cap', 'visor', 'nonvisor', 'helmat', 'hood', 'nohat', 'hatdk', 'hat_red', 'hat_yellow', 'hat_green', 'hat_blue', 'hat_brown', 'hat_pink', 'hat_gray', 'hat_black', 'hat_white', 'hat_unknown', 'short', 'long', 'bald', 'hairdk']
)

df.to_excel(total_file_path)
print(time.time()-start)