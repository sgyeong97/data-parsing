import os
import xml.etree.ElementTree
from bs4 import BeautifulSoup
import random
import shutil
import time
import pandas as pd
from pandas import DataFrame

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Origin'
xml_list_path = os.path.join(target_path, 'Xmls')
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

xml_file_list = os.listdir(xml_list_path)
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

file_attri = []
print("xml을 읽어 속성 값 count 시작")

for xml in xml_list:
    if xml.endswith('xml'):
        xml_path = os.path.join(xml_list_path, xml)
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
                                shortshirt_list.append(file_name_list[xml_count])
                                temp_str += 'short_sleeve,'
                            elif result == 'long_sleeve':
                                longshirt += 1
                                longshirt_list.append(file_name_list[xml_count])
                                temp_str += 'long_sleeve,'
                            else:
                                shirtdk += 1
                                shirtdk_list.append(file_name_list[xml_count])
                                temp_str += 'shirtdk,'
                            attri = result
                        else:
                            if label_name == 'top_red':
                                top_red += 1
                                temp_str += 'top_red'
                                red_list.append(file_name_list[xml_count])
                            if label_name == 'top_yellow':
                                top_yellow += 1
                                yellow_list.append(file_name_list[xml_count])
                                temp_str += 'top_yellow'
                            if label_name == 'top_green':
                                top_green += 1
                                green_list.append(file_name_list[xml_count])
                                temp_str += 'top_green'
                            if label_name == 'top_blue':
                                top_blue += 1
                                blue_list.append(file_name_list[xml_count])
                                temp_str += 'top_blue'
                            if label_name == 'top_black':
                                top_black += 1
                                black_list.append(file_name_list[xml_count])
                                temp_str += 'top_black'
                            if label_name == 'top_brown':
                                top_brown += 1
                                brown_list.append(file_name_list[xml_count])
                                temp_str += 'top_brown'
                            if label_name == 'top_pink':
                                top_pink += 1
                                pink_list.append(file_name_list[xml_count])
                                temp_str += 'top_pink'
                            if label_name == 'top_grey':
                                top_gray += 1
                                gray_list.append(file_name_list[xml_count])
                                temp_str += 'top_gray'
                            if label_name == 'top_white':
                                top_white += 1
                                white_list.append(file_name_list[xml_count])
                                temp_str += 'top_white'
                            if label_name == 'top_color_unknown':
                                top_color_unknown += 1
                                unknown_list.append(file_name_list[xml_count])
                                temp_str += 'top_color_unknown'
                            attri = label_name
                    temp = temp_str
                    if not (str(attri) in str_temp):
                        str_temp += ',%s' % str(attri)
    file_attri.append(temp)
    attri_list.append(str_temp)
    xml_count += 1

total_list = [longshirt, shortshirt, shirtdk, top_brown, top_red, top_yellow, top_green, top_blue, top_pink, top_gray, top_black, top_white, top_color_unknown]
total_count_list= [longshirt, shortshirt, shirtdk, top_brown,top_red, top_yellow, top_green, top_blue,top_pink, top_gray,  top_black, top_white, top_color_unknown]
total_name_list = ['longshirt', 'shortshirt', 'shirtdk', 'top_brown', 'top_red', 'top_yellow', 'top_green', 'top_blue', 'top_pink', 'top_gray','top_black', 'top_white', 'top_color_unknown']


result_list = []
index_list = []
shirtdk_copy_list = shirtdk_list.copy()
longshirt_copy_list = longshirt_list.copy()
shortshirt_copy_list = shortshirt_list.copy()
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

longshirt_count = 0
shortshirt_count = 0
red_count = 0
yellow_count = 0
green_count = 0
blue_count = 0
brown_count = 0
pink_count = 0
gray_count = 0
black_count = 0
white_count = 0

print("테스트셋에 들어갈 파일 분류 시작")

shirtdk_copy_list.sort()
brown_copy_list.sort()
red_copy_list.sort()
yellow_copy_list.sort()
green_copy_list.sort()
blue_copy_list.sort()
pink_copy_list.sort()
gray_copy_list.sort()
black_copy_list.sort()
white_copy_list.sort()
unknown_copy_list.sort()

remove_target = []
run_bool = True

while run_bool:
    origin_list = []
    sort_list = []

    if 'brown' in remove_target:
        pass
    else:
        brown_len = len(brown_copy_list)
        origin_list.append(brown_len)
        sort_list.append(brown_len)
    if 'red' in remove_target:
        pass
    else:
        red_len = len(red_copy_list)
        origin_list.append(red_len)
        sort_list.append(red_len)
    if 'yellow' in remove_target:
        pass
    else:
        yellow_len = len(yellow_copy_list)
        origin_list.append(yellow_len)
        sort_list.append(yellow_len)
    if 'green' in remove_target:
        pass
    else:
        green_len = len(green_copy_list)
        origin_list.append(green_len)
        sort_list.append(green_len)
    if 'blue' in remove_target:
        pass
    else:
        blue_len = len(blue_copy_list)
        origin_list.append(blue_len)
        sort_list.append(blue_len)
    if 'pink' in remove_target:
        pass
    else:
        pink_len = len(pink_copy_list)
        origin_list.append(pink_len)
        sort_list.append(pink_len)
    if 'gray' in remove_target:
        pass
    else:
        gray_len = len(gray_copy_list)
        origin_list.append(gray_len)
        sort_list.append(gray_len)
    if 'black' in remove_target:
        pass
    else:
        black_len = len(black_copy_list)
        origin_list.append(black_len)
        sort_list.append(black_len)
    if 'white' in remove_target:
        pass
    else:
        white_len = len(white_copy_list)
        origin_list.append(white_len)
        sort_list.append(white_len)
    if 'unknown' in remove_target:
        pass
    else:
        unknown_len = len(unknown_copy_list)
        origin_list.append(unknown_len)
        sort_list.append(unknown_len)
    if 'shirtdk' in remove_target:
        pass
    else:
        shirtdk_len = len(shirtdk_copy_list)
        origin_list.append(shirtdk_len)
        sort_list.append(shirtdk_len)
    sort_list.sort()
    if len(remove_target) == 2:
        run_bool = False
        break

    #print(sort_list)
    # print(origin_list)
    #print(remove_target)
    #print(remove_count)
    # input()

    if len(remove_target) < 2:
        if not('shirtdk' in remove_target):
            if len(shirtdk_copy_list) == 0:
                remove_target.append('shirtdk')
            else:
                if len(shirtdk_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(shirtdk_copy_list) - 1)
                temp = shirtdk_copy_list[random_num]
                shirtdk_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_upper_%s' % empty
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                    brown_count += 1
                if temp in red_copy_list:
                    red_copy_list.remove(temp)
                    red_count += 1
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                    yellow_count += 1
                if temp in gray_copy_list:
                    gray_copy_list.remove(temp)
                    gray_count += 1
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                    green_count += 1
                if temp in blue_copy_list:
                    blue_copy_list.remove(temp)
                    blue_count += 1
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                    pink_count += 1
                if temp in black_copy_list:
                    black_copy_list.remove(temp)
                    black_count += 1
                if temp in white_copy_list:
                    white_copy_list.remove(temp)
                    white_count += 1
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
                result_list.append(name)
        if not ('brown' in remove_target):
            if len(brown_copy_list) == 0:
                remove_target.append('brown')
            else:
                if len(brown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(brown_copy_list)-1)
                temp = brown_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    brown_count += 1
                    brown_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    result_list.append(name)
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('red' in remove_target) :
            if len(red_copy_list) == 0:
                remove_target.append('red')
            else:
                if len(red_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(red_copy_list)-1)
                temp = red_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    red_count += 1
                    red_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    result_list.append(name)
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('yellow' in remove_target) :
            if len(yellow_copy_list)  == 0:
                remove_target.append('yellow')
            else:
                if len(yellow_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(yellow_copy_list)-1)
                temp = yellow_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    yellow_count += 1
                    yellow_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    result_list.append(name)
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('green' in remove_target):
            if len(green_copy_list) == 0:
                remove_target.append('green')
            else:
                if len(green_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(green_copy_list)-1)
                temp = green_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    green_count += 1
                    green_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    result_list.append(name)
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('blue' in remove_target):
            if len(blue_copy_list) == 0:
                remove_target.append('blue')
            else:
                if len(blue_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(blue_copy_list) - 1)
                temp = blue_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    result_list.append(name)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('pink' in remove_target):
            if len(pink_copy_list) == 0:
                remove_target.append('pink')
            else:
                if len(pink_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(pink_copy_list)-1)
                temp = pink_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    pink_count += 1
                    pink_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    result_list.append(name)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('gray' in remove_target):
            if len(gray_copy_list) == 0:
                remove_target.append('gray')
            else:
                if len(gray_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(gray_copy_list)-1)
                temp = gray_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    result_list.append(name)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('black' in remove_target):
            if len(black_copy_list) == 0:
                remove_target.append('black')
            else:
                if len(black_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(black_copy_list)-1)
                temp = black_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    black_count += 1
                    black_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    result_list.append(name)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('white' in remove_target):
            if len(white_copy_list) == 0:
                remove_target.append('white')
            else:
                if len(white_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(white_copy_list)-1)
                temp = white_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    white_count += 1
                    white_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    result_list.append(name)
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                        result_list.append(name)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not('unknown' in remove_target):
            if len(unknown_copy_list) == 0:
                remove_target.append('unknown')
            else:
                if len(shirtdk_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(unknown_copy_list)-1)
                temp = unknown_copy_list[random_num]
                if longshirt_count >= shortshirt_count:
                    if temp in longshirt_copy_list:
                        in_run_bool = False
                    elif temp in shortshirt_copy_list:
                        in_run_bool = True
                        shortshirt_count += 1
                        shortshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                elif longshirt_count < shortshirt_count:
                    if temp in shortshirt_copy_list:
                        in_run_bool = False
                    elif temp in longshirt_copy_list:
                        in_run_bool = True
                        longshirt_count += 1
                        longshirt_copy_list.remove(temp)
                    else:
                        in_run_bool = True
                if in_run_bool:
                    unknown_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_upper_%s' % empty
                    if temp in shirtdk_copy_list:
                        shirtdk_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                        brown_count += 1
                    if temp in red_copy_list:
                        red_copy_list.remove(temp)
                        red_count += 1
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                        yellow_count += 1
                    if temp in gray_copy_list:
                        gray_copy_list.remove(temp)
                        gray_count += 1
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                        green_count += 1
                    if temp in blue_copy_list:
                        blue_copy_list.remove(temp)
                        blue_count += 1
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                        pink_count += 1
                    if temp in black_copy_list:
                        black_copy_list.remove(temp)
                        black_count += 1
                    if temp in white_copy_list:
                        white_copy_list.remove(temp)
                        white_count += 1
                    result_list.append(name)
temp_list = result_list.copy()
temp_list.sort()
my_set = set(temp_list)
index_list = list(my_set)

empty = ''

run_bool = True
in_run_bool = True

print("부족한 부분 채우는중 (최소 1000)")

remove_target = []
while run_bool:
    if red_count < 1000:
        random_num = random.randint(0, len(red_copy_list) - 1)
        temp = red_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and red_count < 1000:
            red_count += 1
            red_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            result_list.append(name)
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if yellow_count < 1000:
        random_num = random.randint(0, len(yellow_copy_list) - 1)
        temp = yellow_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and yellow_count < 1000:
            yellow_count += 1
            yellow_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            result_list.append(name)
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if green_count < 1000:
        random_num = random.randint(0, len(green_copy_list) - 2)
        temp = green_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and green_count < 1000:
            green_count += 1
            green_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            result_list.append(name)
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if blue_count < 1000:
        random_num = random.randint(0, len(blue_copy_list) - 2)
        temp = blue_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and blue_count < 1000:
            blue_count += 1
            blue_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            result_list.append(name)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if brown_count < 1000 :
        random_num = random.randint(0, len(brown_copy_list) - 1)
        temp = brown_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and brown_count < 1000:
            brown_count += 1
            brown_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            result_list.append(name)
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1

    if pink_count < 1000:
        random_num = random.randint(0, len(pink_copy_list) - 2)
        temp = pink_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and pink_count < 1000:
            pink_count += 1
            pink_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            result_list.append(name)
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)

            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if gray_count < 1000:
        random_num = random.randint(0, len(gray_copy_list) - 2)
        temp = gray_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and gray_count < 1000:
            gray_count += 1
            gray_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            result_list.append(name)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1
    if black_count < 1000:
        random_num = random.randint(0, len(black_copy_list) - 2)
        temp = black_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and black_count < 1000:
            black_count += 1
            black_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            result_list.append(name)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in white_copy_list:
                white_copy_list.remove(temp)
                white_count += 1

    if white_count < 1000:
        random_num = random.randint(0, len(white_copy_list) - 2)
        temp = white_copy_list[random_num]
        if longshirt_count >= shortshirt_count:
            if temp in longshirt_copy_list:
                in_run_bool = False
            elif temp in shortshirt_copy_list:
                in_run_bool = True
                shortshirt_count += 1
                shortshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        elif longshirt_count < shortshirt_count:
            if temp in shortshirt_copy_list:
                in_run_bool = False
            elif temp in longshirt_copy_list:
                in_run_bool = True
                longshirt_count += 1
                longshirt_copy_list.remove(temp)
            else:
                in_run_bool = True
        if temp in red_copy_list:
            if red_count >= 1000:
                in_run_bool = False
        if temp in yellow_copy_list:
            if yellow_count >= 1000:
                in_run_bool = False
        if temp in green_copy_list:
            if green_count >= 1000:
                in_run_bool = False
        if temp in blue_copy_list:
            if blue_count >= 1000:
                in_run_bool = False
        if temp in brown_copy_list:
            if brown_count >= 1000:
                in_run_bool = False
        if temp in pink_copy_list:
            if pink_count >= 1000:
                in_run_bool = False
        if temp in gray_copy_list:
            if gray_count >= 1000:
                in_run_bool = False
        if temp in black_copy_list:
            if black_count >= 1000:
                in_run_bool = False
        if temp in white_copy_list:
            if white_count >= 1000:
                in_run_bool = False
        if in_run_bool and white_count < 1000:
            white_count += 1
            white_copy_list.remove(temp)
            empty = temp[-6:]
            name = 'atr_c_upper_%s' % empty
            result_list.append(name)
            if temp in shirtdk_copy_list:
                shirtdk_copy_list.remove(temp)
            if temp in brown_copy_list:
                brown_copy_list.remove(temp)
                brown_count += 1
            if temp in red_copy_list:
                red_copy_list.remove(temp)
                red_count += 1
            if temp in yellow_copy_list:
                yellow_copy_list.remove(temp)
                yellow_count += 1
            if temp in gray_copy_list:
                gray_copy_list.remove(temp)
                gray_count += 1
            if temp in green_copy_list:
                green_copy_list.remove(temp)
                green_count += 1
            if temp in blue_copy_list:
                blue_copy_list.remove(temp)
                blue_count += 1
            if temp in pink_copy_list:
                pink_copy_list.remove(temp)
                pink_count += 1
            if temp in black_copy_list:
                black_copy_list.remove(temp)
                black_count += 1

    print(red_count, yellow_count, green_count, blue_count, brown_count, pink_count, gray_count, black_count, white_count)
    if red_count >= 1000 and yellow_count >= 1000 and green_count >= 1000 and blue_count >= 1000 and brown_count >= 1000 and pink_count >= 1000 and gray_count >= 1000 and black_count >= 1000 and white_count >= 1000:
        run_bool = False

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