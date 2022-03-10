import os
import xml.etree.ElementTree
from bs4 import BeautifulSoup
import cv2
import random
import shutil
import time
import numpy as np
import pandas as pd
# from time import sleep
from pandas import DataFrame

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\common\Origin'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\common\\file_list.txt'
total_file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\common\\common_total.xlsx'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
xml_count = 0

man = 0
woman = 0
genderdk = 0
infant = 0
child = 0
teenager = 0
adult = 0
oldperson = 0
backpack = 0
totebag = 0
shoulderbag = 0
plasticbag = 0
bagdk = 0
bagnone = 0
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
man_list = []
woman_list = []
genderdk_list = []
infant_list = []
child_list = []
teenager_list = []
adult_list = []
oldperson_list = []
backpack_list = []
totebag_list = []
shoulderbag_list = []
plasticbag_list = []
bagdk_list = []
bagnone_list = []
red_list = []
yellow_list = []
green_list = []
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
            label = 'head'
            lines = str(box).splitlines()
            for x in lines[1:]:
                result = split_label(x)
                if result != 'false':
                    label_name = split_name(x)
                    if label_name == 'gender':
                        if result == 'male':
                            man += 1
                            man_list.append(file_name_list[xml_count])
                        elif result == 'female':
                            woman += 1
                            woman_list.append(file_name_list[xml_count])
                        else:
                            genderdk += 1
                            genderdk_list.append(file_name_list[xml_count])
                    elif label_name == 'age':
                        if result == '8~13':
                            child += 1
                            child_list.append(file_name_list[xml_count])
                        elif result == '14~19':
                            teenager += 1
                            teenager_list.append(file_name_list[xml_count])
                        elif result == '20~70':
                            adult += 1
                            adult_list.append(file_name_list[xml_count])
                        elif result == '70~':
                            oldperson += 1
                            oldperson_list.append(file_name_list[xml_count])
                        else:
                            infant += 1
                            infant_list.append(file_name_list[xml_count])
                    else:
                        if label_name == 'backpack':
                            backpack += 1
                            backpack_list.append(file_name_list[xml_count])
                        elif label_name == 'bagless':
                            bagnone += 1
                            bagnone_list.append(file_name_list[xml_count])
                        elif label_name == 'unknown_bag':
                            bagdk += 1
                            bagdk_list.append(file_name_list[xml_count])
                        elif label_name == 'plasticbag':
                            plasticbag += 1
                            plasticbag_list.append(file_name_list[xml_count])
                        elif label_name == 'shoulderbag':
                            shoulderbag += 1
                            shoulderbag_list.append(file_name_list[xml_count])
                        elif label_name == 'handbag':
                            totebag += 1
                            totebag_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_red':
                            red += 1
                            red_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_yellow':
                            yellow += 1
                            yellow_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_green':
                            green+=1
                            green_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_blue':
                            blue += 1
                            blue_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_brown':
                            brown += 1
                            brown_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_pink':
                            pink += 1
                            pink_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_grey':
                            gray += 1
                            gray_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_black':
                            black += 1
                            black_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_white':
                            white += 1
                            white_list.append(file_name_list[xml_count])
                        elif label_name == 'bag_color_unknown':
                            unknown += 1
                            unknown_list.append(file_name_list[xml_count])
    xml_count += 1

total_list = [man, woman, genderdk, infant, child, teenager, adult, oldperson, backpack, totebag, shoulderbag, plasticbag, bagdk, bagnone, red, yellow, green, blue, brown, pink, gray, black, white, unknown]

red_copy_list = red_list.copy()
yellow_copy_list = yellow_list.copy()
green_copy_list = green_list.copy()
blue_copy_list = blue_list.copy()
brown_copy_list = brown_list.copy()
pink_copy_list = pink_list.copy()
gray_copy_list = gray_list.copy()
black_copy_list = black_list.copy()
white_copy_list = white_list.copy()
unknown_copy_list = unknown_list.copy()
man_copy_list = man_list.copy()
woman_copy_list = woman_list.copy()
genderdk_copy_list = genderdk_list.copy()
infant_copy_list = infant_list.copy()
child_copy_list = child_list.copy()
teenager_copy_list = teenager_list.copy()
adult_copy_list = adult_list.copy()
oldperson_copy_list = oldperson_list.copy()
backpack_copy_list = backpack_list.copy()
totebag_copy_list = totebag_list.copy()
shoulderbag_copy_list = shoulderbag_list.copy()
plasticbag_copy_list = plasticbag_list.copy()
bagdk_copy_list = bagdk_list.copy()
bagnone_copy_list = bagnone_list.copy()

red_copy_list.sort()
yellow_copy_list.sort()
green_copy_list.sort()
blue_copy_list.sort()
brown_copy_list.sort()
pink_copy_list.sort()
gray_copy_list.sort()
black_copy_list.sort()
white_copy_list.sort()
unknown_copy_list.sort()
man_copy_list.sort()
woman_copy_list.sort()
genderdk_copy_list.sort()
oldperson_copy_list.sort()
infant_copy_list.sort()
child_copy_list.sort()
teenager_copy_list.sort()
adult_copy_list.sort()
backpack_copy_list.sort()
totebag_copy_list.sort()
shoulderbag_copy_list.sort()
plasticbag_copy_list.sort()
bagdk_copy_list.sort()
bagnone_copy_list.sort()

remove_target = []
run_bool = True
man_count = 0
woman_count = 0
child_count = 0
teenager_count = 0
adult_count = 0
backpack_count = 0
totebag_count = 0
shoulderbag_count =0
plasticbag_count = 0
bagnone_count = 0
black_count = 0

result_list = []
print("분류 시작")
while run_bool:
    origin_list = []
    sort_list = []

    if not ('infant' in remove_target):
        infant_len = len(infant_copy_list)
        origin_list.append(infant_len)
        sort_list.append(infant_len)
    if not('oldperson' in remove_target):
        oldperson_len = len(oldperson_copy_list)
        origin_list.append(oldperson_len)
        sort_list.append(oldperson_len)
    if not('unknown' in remove_target):
        unknown_len = len(unknown_copy_list)
        origin_list.append(unknown_len)
        sort_list.append(unknown_len)

    sort_list.sort()
    # print(sort_list)
    # sleep(2)
    if len(remove_target) == 3:
        run_bool = False
        print(remove_target)
        break
    if len(remove_target) < 3:
        if not('genderdk' in remove_target):
            if len(genderdk_copy_list) == 0:
                remove_target.append('genderdk')
            else:
                if len(genderdk_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(genderdk_copy_list) - 1)
                temp = genderdk_copy_list[random_num]
                empty = temp[-6:]
                name = 'atr_c_common_%s' % empty
                result_list.append(name)
                if temp in infant_copy_list:
                    infant_copy_list.remove(temp)
                if temp in child_copy_list:
                    child_copy_list.remove(temp)
                    child_count += 1
                if temp in teenager_copy_list:
                    teenager_copy_list.remove(temp)
                    teenager_count += 1
                if temp in adult_copy_list:
                    adult_copy_list.remove(temp)
                    adult_count += 1
                if temp in oldperson_copy_list:
                    oldperson_copy_list.remove(temp)
                if temp in backpack_copy_list:
                    backpack_copy_list.remove(temp)
                if temp in totebag_copy_list:
                    totebag_copy_list.remove(temp)
                if temp in shoulderbag_copy_list:
                    shoulderbag_copy_list.remove(temp)
                if temp in plasticbag_copy_list:
                    plasticbag_copy_list.remove(temp)
                if temp in bagdk_copy_list:
                    bagdk_copy_list.remove(temp)
                if temp in bagnone_copy_list:
                    bagnone_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not('infant' in remove_target):
            if len(infant_copy_list) == 0:
                remove_target.append('infant')
            else:
                if len(infant_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(infant_copy_list) - 1)
                temp = infant_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    infant_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        age = abs(child_count-teenager_count-adult_count)
        if age < 5:
            if len(child_copy_list) == 1:
                random_num = 0
            else:
                random_num = random.randint(0, len(child_copy_list) - 1)
            temp = child_copy_list[random_num]
            if man_count >= woman_count:
                if temp in man_copy_list:
                    in_run_bool = False
                elif temp in woman_copy_list:
                    in_run_bool = True
                    woman_count += 1
                    woman_copy_list.remove(temp)
                else:
                    in_run_bool = True
            elif man_count < woman_count:
                if temp in woman_copy_list:
                    in_run_bool = False
                elif temp in man_copy_list:
                    man_count += 1
                    man_copy_list.remove(temp)
                    in_run_bool = True
                else:
                    in_run_bool = True
            if in_run_bool:
                child_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_common_%s' % empty
                result_list.append(name)

                if temp in man_copy_list:
                    man_copy_list.remove(temp)
                if temp in woman_copy_list:
                    woman_copy_list.remove(temp)
                if temp in genderdk_copy_list:
                    genderdk_copy_list.remove(temp)
                if temp in backpack_copy_list:
                    backpack_copy_list.remove(temp)
                if temp in totebag_copy_list:
                    totebag_copy_list.remove(temp)
                if temp in shoulderbag_copy_list:
                    shoulderbag_copy_list.remove(temp)
                if temp in plasticbag_copy_list:
                    plasticbag_copy_list.remove(temp)
                if temp in bagdk_copy_list:
                    bagdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        age = abs(child_count - teenager_count)
        if age > 100 or age < 120:
            if len(teenager_copy_list) <= 2:
                pass
            else:
                random_num = random.randint(0, len(teenager_copy_list) - 1)
                temp = teenager_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    teenager_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        age = abs(child_count - adult_count)
        if age < 5:
            if len(adult_copy_list) == 1:
                random_num = 0
            else:
                random_num = random.randint(0, len(adult_copy_list) - 1)
                temp = adult_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    adult_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)

                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not('oldperson' in remove_target):
            if len(oldperson_copy_list) == 0:
                remove_target.append('oldperson')
            else:
                if len(oldperson_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(oldperson_copy_list) - 1)
                temp = oldperson_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    oldperson_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not('bagdk' in remove_target):
            if len(bagdk_copy_list) == 0:
                remove_target.append('bagdk')
            else:
                if len(bagdk_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(bagdk_copy_list) - 1)
                temp = bagdk_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    bagdk_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
        if not('yellow' in remove_target):
            if len(yellow_copy_list) == 0:
                remove_target.append('yellow')
            else:
                if len(yellow_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(yellow_copy_list) - 1)
                temp = yellow_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    yellow_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('red' in remove_target):
            if len(red_copy_list) == 0:
                remove_target.append('red')
            else:
                if len(red_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(red_copy_list) - 1)
                temp = red_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    red_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('green' in remove_target):
            if len(green_copy_list) == 0:
                remove_target.append('green')
            else:
                if len(green_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(green_copy_list) - 1)
                temp = green_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    green_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('blue' in remove_target):
            if len(blue_copy_list) == 0:
                remove_target.append('blue')
            else:
                if len(blue_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(blue_copy_list) - 1)
                temp = blue_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    blue_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('brown' in remove_target):
            if len(brown_copy_list) == 0:
                remove_target.append('brown')
            else:
                if len(brown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(brown_copy_list) - 1)
                temp = brown_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    brown_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('pink' in remove_target):
            if len(pink_copy_list) == 0:
                remove_target.append('pink')
            else:
                if len(pink_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(pink_copy_list) - 1)
                temp = pink_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    pink_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('gray' in remove_target):
            if len(gray_copy_list) == 0:
                pass
            else:
                if len(gray_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(gray_copy_list) - 1)
                temp = gray_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    gray_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('black' in remove_target):
            if len(black_copy_list) == 0:
                pass
            else:
                if len(black_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(black_copy_list) - 1)
                temp = black_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    black_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('white' in remove_target):
            if len(white_copy_list) == 0:
                pass
            else:
                if len(white_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(white_copy_list) - 1)
                temp = white_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    white_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)
        if not('unknown' in remove_target):
            if len(unknown_copy_list) == 0:
                remove_target.append('unknown')
            else:
                if len(unknown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(unknown_copy_list) - 1)
                temp = unknown_copy_list[random_num]
                if man_count >= woman_count:
                    if temp in man_copy_list:
                        in_run_bool = False
                    elif temp in woman_copy_list:
                        in_run_bool = True
                        woman_count += 1
                        woman_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif man_count < woman_count:
                    if temp in woman_copy_list:
                        in_run_bool = False
                    elif temp in man_copy_list:
                        man_count += 1
                        man_copy_list.remove(temp)
                        in_run_bool = True
                    else:
                        in_run_bool = True
                if in_run_bool:
                    unknown_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_common_%s' % empty
                    result_list.append(name)
                    if temp in man_copy_list:
                        man_copy_list.remove(temp)
                    if temp in woman_copy_list:
                        woman_copy_list.remove(temp)
                    if temp in genderdk_copy_list:
                        genderdk_copy_list.remove(temp)
                    if temp in infant_copy_list:
                        infant_copy_list.remove(temp)
                    if temp in child_copy_list:
                        child_copy_list.remove(temp)
                        child_count += 1
                    if temp in teenager_copy_list:
                        teenager_copy_list.remove(temp)
                        teenager_count += 1
                    if temp in adult_copy_list:
                        adult_copy_list.remove(temp)
                        adult_count += 1
                    if temp in oldperson_copy_list:
                        oldperson_copy_list.remove(temp)
                    if temp in backpack_copy_list:
                        backpack_copy_list.remove(temp)
                    if temp in totebag_copy_list:
                        totebag_copy_list.remove(temp)
                    if temp in shoulderbag_copy_list:
                        shoulderbag_copy_list.remove(temp)
                    if temp in plasticbag_copy_list:
                        plasticbag_copy_list.remove(temp)
                    if temp in bagdk_copy_list:
                        bagdk_copy_list.remove(temp)

print("분류 완료, 파일 생성")
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