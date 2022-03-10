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

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\lower\origin'
xml_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\lower\Origin\Xmls'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\lower\\file_list.txt'
total_file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\lower\\lower_total.xlsx'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
xml_count = 0

longpants = 0
shortpants = 0
longskirt = 0
shortskirt = 0
lowerdk = 0
longpants_list = []
shortpants_list = []
longskirt_list = []
shortskirt_list = []
lowerdk_list = []

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
l_red_list = []
l_green_list = []
l_yellow_list = []
l_blue_list = []
l_brown_list = []
l_pink_list = []
l_gray_list = []
l_black_list = []
l_white_list = []
l_unknown_list = []


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
s_red_list = []
s_green_list = []
s_yellow_list = []
s_blue_list = []
s_brown_list = []
s_pink_list = []
s_gray_list = []
s_black_list = []
s_white_list = []
s_unknown_list = []


target_file_list = os.listdir(target_path)
for x in target_file_list:
    if x.endswith('png'):
        crop_img_list.append(x)
xml_file_list = os.listdir(xml_path)
for x in xml_file_list:
    if x.endswith('xml'):
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
print("xml을 읽어 속성 값 확인 시작")

for xml in xml_list:
    if xml.endswith('xml'):
        xml_path = os.path.join(target_path, 'Xmls', xml)
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
            label = 'lower'
            lines = str(box).splitlines()
            for x in lines[1:]:
                result = split_label(x)
                if result != 'false':
                    label_name = split_name(x)
                    if label_name:
                        if label_name == 'shoes_color':
                            if 'shoes_red' in result:
                                s_red += 1
                                s_red_list.append(file_name_list[xml_count])
                            if 'shoes_yellow' in result:
                                s_yellow += 1
                                s_yellow_list.append(file_name_list[xml_count])
                            if 'shoes_green' in result:
                                s_green += 1
                                s_green_list.append(file_name_list[xml_count])
                            if 'shoes_blue' in result:
                                s_blue += 1
                                s_blue_list.append(file_name_list[xml_count])
                            if 'shoes_brown' in result:
                                s_brown += 1
                                s_brown_list.append(file_name_list[xml_count])
                            if 'shoes_pink' in result:
                                s_pink += 1
                                s_pink_list.append(file_name_list[xml_count])
                            if 'shoes_grey' in result:
                                s_gray += 1
                                s_gray_list.append(file_name_list[xml_count])
                            if 'shoes_black' in result:
                                s_black += 1
                                s_black_list.append(file_name_list[xml_count])
                            if 'shoes_white' in result:
                                s_white += 1
                                s_white_list.append(file_name_list[xml_count])
                            if 'shoes_unknown' in result:
                                s_unknown += 1
                                s_unknown_list.append(file_name_list[xml_count])
                        elif label_name == 'bottom':
                            if result == 'long_pants':
                                longpants += 1
                                longpants_list.append(file_name_list[xml_count])
                            elif result == 'short_pants':
                                shortpants += 1
                                shortpants_list.append(file_name_list[xml_count])
                            elif result == 'long_skirt':
                                longskirt += 1
                                longskirt_list.append(file_name_list[xml_count])
                            elif result == 'short_skirt':
                                shortskirt += 1
                                shortskirt_list.append(file_name_list[xml_count])
                            else:
                                lowerdk += 1
                                lowerdk_list.append(file_name_list[xml_count])
                        else:
                            if 'bottom_red' in label_name:
                                l_red += 1
                                l_red_list.append(file_name_list[xml_count])
                            if 'bottom_yellow' in label_name:
                                l_yellow += 1
                                l_yellow_list.append(file_name_list[xml_count])
                            if 'bottom_green' in label_name:
                                l_green += 1
                                l_green_list.append(file_name_list[xml_count])
                            if 'bottom_blue' in label_name:
                                l_blue += 1
                                l_blue_list.append(file_name_list[xml_count])
                            if 'bottom_brown' in label_name:
                                l_brown += 1
                                l_brown_list.append(file_name_list[xml_count])
                            if 'bottom_pink' in label_name:
                                l_pink += 1
                                l_pink_list.append(file_name_list[xml_count])
                            if 'bottom_grey' in label_name:
                                l_gray += 1
                                l_gray_list.append(file_name_list[xml_count])
                            if 'bottom_black' in label_name:
                                l_black += 1
                                l_black_list.append(file_name_list[xml_count])
                            if 'bottom_white' in label_name:
                                l_white += 1
                                l_white_list.append(file_name_list[xml_count])
                            if 'bottom_color_unknown' in label_name:
                                l_unknown += 1
                                l_unknown_list.append(file_name_list[xml_count])
    xml_count += 1

total_list = [longpants, shortpants, longskirt, shortskirt, lowerdk, l_red, l_yellow, l_green, l_blue, l_brown, l_pink, l_gray, l_black, l_white, l_unknown, s_red, s_yellow, s_green, s_blue, s_brown, s_pink, s_gray, s_black, s_white, s_unknown]
print("속성 확인 및 리스트 생성 완료")

s_red_copy_list = s_red_list.copy()
s_yellow_copy_list = s_yellow_list.copy()
s_green_copy_list = s_green_list.copy()
s_blue_copy_list = s_blue_list.copy()
s_brown_copy_list = s_brown_list.copy()
s_pink_copy_list = s_pink_list.copy()
s_gray_copy_list = s_gray_list.copy()
s_black_copy_list = s_black_list.copy()
s_white_copy_list = s_white_list.copy()
s_unknown_copy_list = s_unknown_list.copy()
l_red_copy_list = l_red_list.copy()
l_yellow_copy_list = l_yellow_list.copy()
l_green_copy_list = l_green_list.copy()
l_blue_copy_list = l_blue_list.copy()
l_brown_copy_list = l_brown_list.copy()
l_pink_copy_list = l_pink_list.copy()
l_gray_copy_list = l_gray_list.copy()
l_black_copy_list = l_black_list.copy()
l_white_copy_list = l_white_list.copy()
l_unknown_copy_list = l_unknown_list.copy()

longpants_copy_list = longpants_list.copy()
shortpants_copy_list = shortpants_list.copy()
longskirt_copy_list = longskirt_list.copy()
shortskirt_copy_list = shortskirt_list.copy()
lowerdk_copy_list = lowerdk_list.copy()

remove_target = []
run_bool = True
result_list = []

longpants_count = 0
shortpants_count = 0
longskirt_count = 0
shortskirt_count = 0
lowerdk_count = 0

l_red_count = 0
l_yellow_count = 0
l_green_count = 0
l_blue_count = 0
l_brown_count = 0
l_pink_count = 0
l_gray_count = 0
l_black_count = 0
l_white_count = 0
l_unknown_count = 0

s_red_count = 0
s_yellow_count = 0
s_green_count = 0
s_blue_count = 0
s_brown_count = 0
s_pink_count = 0
s_gray_count = 0
s_black_count = 0
s_white_count = 0
s_unknown_count = 0

in_run_bool = True
print("분류 시작")

while run_bool:

    in_run_bool = True

    sort_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count, lowerdk_count, l_red_count, l_yellow_count, l_green_count, l_blue_count, l_brown_count, l_pink_count, l_gray_count, l_black_count, l_white_count, l_unknown_count, s_red_count, s_yellow_count, s_green_count, s_blue_count, s_brown_count, s_pink_count, s_gray_count, s_black_count, s_white_count, s_unknown_count]
    print(sort_list)
    print(remove_target)
    if len(remove_target) == 21:
        run_bool = False
        break

    if run_bool:
        if not('lowerdk' in remove_target):
            if lowerdk_count >= 400:
                remove_target.append('lowerdk')
            else:
                if len(lowerdk_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(lowerdk_copy_list) - 1)

                temp = lowerdk_copy_list[random_num]
                lowerdk_count += 1
                lowerdk_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1

        if not('l_red' in remove_target):
            if l_red_count >= 400:
                remove_target.append('l_red')
            else:
                if len(l_red_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_red_copy_list) - 1)
                temp = l_red_copy_list[random_num]
                l_red_copy_list.remove(temp)
                l_red_count += 1
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)

                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not('l_yellow' in remove_target):
            if len(l_yellow_copy_list) == 0:
                remove_target.append('l_yellow')
            else:
                if len(l_yellow_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_yellow_copy_list) - 1)
                temp = l_yellow_copy_list[random_num]
                l_yellow_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                l_yellow_count += 1
                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not('l_green' in remove_target):
            if l_green_count >= 400:
                remove_target.append('l_green')
            else:
                if len(l_green_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_green_copy_list) - 1)
                temp = l_green_copy_list[random_num]
                l_green_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                l_green_count += 1
                if temp in l_red_copy_list:
                    l_red_count += 1
                    l_red_copy_list.remove(temp)
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)

        if not ('l_blue' in remove_target):
            if l_blue_count >= 400:
                remove_target.append('l_blue')
            else:
                if len(l_blue_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_blue_copy_list) - 1)
                temp = l_blue_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                if in_run_bool:
                    l_blue_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    l_blue_count += 1

                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)
        if not ('l_brown' in remove_target):
            if l_brown_count >= 400:
                remove_target.append('l_brown')
            else:
                if len(l_brown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_brown_copy_list) - 1)
                temp = l_brown_copy_list[random_num]

                l_brown_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                l_brown_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('l_pink' in remove_target):
            if len(l_pink_copy_list) == 0:
                remove_target.append('l_pink')
            else:
                if len(l_pink_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_pink_copy_list) - 1)
                temp = l_pink_copy_list[random_num]
                l_pink_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                l_pink_count += 1
                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)

                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('l_gray' in remove_target):
            if l_gray_count >= 400:
                remove_target.append('l_gray')
            else:
                if len(l_gray_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_gray_copy_list) - 1)
                temp = l_gray_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                if in_run_bool:
                    l_gray_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    l_gray_count += 1
                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)
        if not ('l_black' in remove_target):
            if l_black_count >= 400:
                remove_target.append('l_black')
            else:
                if len(l_black_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_black_copy_list) - 1)
                temp = l_black_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False

                if in_run_bool:
                    l_black_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    l_black_count += 1

                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)
        if not ('l_white' in remove_target):
            if l_white_count >= 400:
                remove_target.append('l_white')
            else:
                if len(l_white_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_white_copy_list) - 1)
                temp = l_white_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                if in_run_bool:
                    l_white_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    l_white_count += 1
                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)
        if not ('l_unknown' in remove_target):
            if l_unknown_count >= 400:
                remove_target.append('l_unknown')
            else:
                if len(l_unknown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(l_unknown_copy_list) - 1)
                temp = l_unknown_copy_list[random_num]
                l_unknown_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                l_unknown_count += 1
                result_list.append(temp)
                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)

        if not ('s_red' in remove_target):
            if s_red_count >= 400:
                remove_target.append('s_red')
            else:
                if len(s_red_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_red_copy_list) - 1)
                temp = s_red_copy_list[random_num]

                s_red_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_red_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_yellow' in remove_target):
            if len(s_yellow_copy_list) == 0:
                remove_target.append('s_yellow')
            else:
                if len(s_yellow_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_yellow_copy_list) - 1)
                temp = s_yellow_copy_list[random_num]

                s_yellow_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_yellow_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_green' in remove_target):
            if len(s_green_copy_list) == 0:
                remove_target.append('s_green')
            else:
                if len(s_green_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_green_copy_list) - 1)
                temp = s_green_copy_list[random_num]

                s_green_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_green_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_blue' in remove_target):
            if s_blue_count >= 400:
                remove_target.append('s_blue')
            else:
                if len(s_blue_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_blue_copy_list) - 1)
                temp = s_blue_copy_list[random_num]

                s_blue_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_blue_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_brown' in remove_target):
            if s_brown_count >= 400:
                remove_target.append('s_brown')
            else:
                if len(s_brown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_brown_copy_list) - 1)
                temp = s_brown_copy_list[random_num]

                s_brown_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_brown_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_count += 1
                    lowerdk_copy_list.remove(temp)
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_pink' in remove_target):
            if s_pink_count >= 400 :
                remove_target.append('s_pink')
            else:
                if len(s_pink_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_pink_copy_list) - 1)
                temp = s_pink_copy_list[random_num]

                s_pink_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_lower_%s' % empty
                result_list.append(name)
                s_pink_count += 1

                if temp in l_red_copy_list:
                    l_red_copy_list.remove(temp)
                    l_red_count += 1
                if temp in l_yellow_copy_list:
                    l_yellow_copy_list.remove(temp)
                    l_yellow_count += 1
                if temp in l_green_copy_list:
                    l_green_copy_list.remove(temp)
                    l_green_count += 1
                if temp in l_blue_copy_list:
                    l_blue_copy_list.remove(temp)
                    l_blue_count += 1
                if temp in l_brown_copy_list:
                    l_brown_copy_list.remove(temp)
                    l_brown_count += 1
                if temp in l_pink_copy_list:
                    l_pink_copy_list.remove(temp)
                    l_pink_count += 1
                if temp in l_gray_copy_list:
                    l_gray_copy_list.remove(temp)
                    l_gray_count += 1
                if temp in l_black_copy_list:
                    l_black_copy_list.remove(temp)
                    l_black_count += 1
                if temp in l_white_copy_list:
                    l_white_copy_list.remove(temp)
                    l_white_count += 1
                if temp in l_unknown_copy_list:
                    l_unknown_copy_list.remove(temp)
                    l_unknown_count += 1
                if temp in s_red_copy_list:
                    s_red_copy_list.remove(temp)
                    s_red_count += 1
                if temp in s_yellow_copy_list:
                    s_yellow_copy_list.remove(temp)
                    s_yellow_count += 1
                if temp in s_green_copy_list:
                    s_green_copy_list.remove(temp)
                    s_green_count += 1
                if temp in s_blue_copy_list:
                    s_blue_copy_list.remove(temp)
                    s_blue_count += 1
                if temp in s_brown_copy_list:
                    s_brown_copy_list.remove(temp)
                    s_brown_count += 1
                if temp in s_pink_copy_list:
                    s_pink_copy_list.remove(temp)
                    s_pink_count += 1
                if temp in s_gray_copy_list:
                    s_gray_copy_list.remove(temp)
                    s_gray_count += 1
                if temp in s_black_copy_list:
                    s_black_copy_list.remove(temp)
                    s_black_count += 1
                if temp in s_white_copy_list:
                    s_white_copy_list.remove(temp)
                    s_white_count += 1
                if temp in s_unknown_copy_list:
                    s_unknown_copy_list.remove(temp)
                    s_unknown_count += 1
                if temp in lowerdk_copy_list:
                    lowerdk_copy_list.remove(temp)
                    lowerdk_count += 1
                if temp in longpants_copy_list:
                    in_run_bool = True
                    longpants_count += 1
                    longpants_copy_list.remove(temp)
                if temp in shortpants_copy_list:
                    shortpants_count += 1
                    shortpants_copy_list.remove(temp)
                if temp in longskirt_copy_list:
                    longskirt_count += 1
                    longskirt_copy_list.remove(temp)
                if temp in shortskirt_copy_list:
                    shortskirt_count += 1
                    shortskirt_copy_list.remove(temp)
        if not ('s_gray' in remove_target):
            if s_gray_count >= 400:
                remove_target.append('s_gray')
            else:
                if len(s_gray_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_gray_copy_list) - 1)
                temp = s_gray_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                else:
                    in_run_bool = False

                if in_run_bool:
                    s_gray_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    s_gray_count += 1
                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)

        if not ('s_black' in remove_target):
            if s_black_count >= 400:
                remove_target.append('s_black')
            else:
                if len(s_black_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_black_copy_list) - 1)
                temp = s_black_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                else:
                    in_run_bool = False
                if in_run_bool:
                    s_black_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    s_black_count += 1
                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_copy_list.remove(temp)
                        lowerdk_count += 1
        if not ('s_white' in remove_target):
            if s_white_count >= 400:
                remove_target.append('s_white')
            else:
                if len(s_white_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_white_copy_list) - 1)
                temp = s_white_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                if shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                else:
                    in_run_bool = False
                if in_run_bool:
                    s_white_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    s_white_count += 1
                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_unknown_copy_list:
                        s_unknown_copy_list.remove(temp)
                        s_unknown_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)

        if not ('s_unknown' in remove_target):
            if s_unknown_count >= 400:
                remove_target.append('s_unknown')
            else:
                if len(s_unknown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(s_unknown_copy_list) - 1)
                temp = s_unknown_copy_list[random_num]
                count_list = [longpants_count, shortpants_count, longskirt_count, shortskirt_count]
                count_list.sort()
                min_val = count_list[0]
                if longpants_count == min_val:
                    if temp in longpants_copy_list:
                        in_run_bool = True
                        longpants_count += 1
                        longpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortpants_count == min_val:
                    if temp in shortpants_copy_list:
                        in_run_bool = True
                        shortpants_count += 1
                        shortpants_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif longskirt_count == min_val:
                    if temp in longskirt_copy_list:
                        in_run_bool = True
                        longskirt_count += 1
                        longskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                elif shortskirt_count == min_val:
                    if temp in shortskirt_copy_list:
                        in_run_bool = True
                        shortskirt_count += 1
                        shortskirt_copy_list.remove(temp)
                    else:
                        in_run_bool = False
                else:
                    in_run_bool = False
                if in_run_bool:
                    s_unknown_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_lower_%s' % empty
                    result_list.append(name)
                    s_unknown_count += 1

                    if temp in l_red_copy_list:
                        l_red_copy_list.remove(temp)
                        l_red_count += 1
                    if temp in l_yellow_copy_list:
                        l_yellow_copy_list.remove(temp)
                        l_yellow_count += 1
                    if temp in l_green_copy_list:
                        l_green_copy_list.remove(temp)
                        l_green_count += 1
                    if temp in l_blue_copy_list:
                        l_blue_copy_list.remove(temp)
                        l_blue_count += 1
                    if temp in l_brown_copy_list:
                        l_brown_copy_list.remove(temp)
                        l_brown_count += 1
                    if temp in l_pink_copy_list:
                        l_pink_copy_list.remove(temp)
                        l_pink_count += 1
                    if temp in l_gray_copy_list:
                        l_gray_copy_list.remove(temp)
                        l_gray_count += 1
                    if temp in l_black_copy_list:
                        l_black_copy_list.remove(temp)
                        l_black_count += 1
                    if temp in l_white_copy_list:
                        l_white_copy_list.remove(temp)
                        l_white_count += 1
                    if temp in l_unknown_copy_list:
                        l_unknown_copy_list.remove(temp)
                        l_unknown_count += 1
                    if temp in s_red_copy_list:
                        s_red_copy_list.remove(temp)
                        s_red_count += 1
                    if temp in s_yellow_copy_list:
                        s_yellow_copy_list.remove(temp)
                        s_yellow_count += 1
                    if temp in s_green_copy_list:
                        s_green_copy_list.remove(temp)
                        s_green_count += 1
                    if temp in s_blue_copy_list:
                        s_blue_copy_list.remove(temp)
                        s_blue_count += 1
                    if temp in s_brown_copy_list:
                        s_brown_copy_list.remove(temp)
                        s_brown_count += 1
                    if temp in s_pink_copy_list:
                        s_pink_copy_list.remove(temp)
                        s_pink_count += 1
                    if temp in s_gray_copy_list:
                        s_gray_copy_list.remove(temp)
                        s_gray_count += 1
                    if temp in s_black_copy_list:
                        s_black_copy_list.remove(temp)
                        s_black_count += 1
                    if temp in s_white_copy_list:
                        s_white_copy_list.remove(temp)
                        s_white_count += 1
                    if temp in lowerdk_copy_list:
                        lowerdk_count += 1
                        lowerdk_copy_list.remove(temp)

temp_list = result_list.copy()
temp_list.sort()
my_set = set(temp_list)
index_list = list(my_set)

empty = ''
for x in index_list:
    empty += x+'\n'
file = open(file_path, 'w')
file.write(empty)
file.close()

print("EXIT")
print(time.time()-start)