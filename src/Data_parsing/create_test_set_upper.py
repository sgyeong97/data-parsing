import os
import xml.etree.ElementTree
from bs4 import BeautifulSoup
import cv2
import random
import shutil
import time
import numpy as np

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\origin'
test_set_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Test_Set'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\\file_list.txt'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []
shortshirt_list = []
longshirt_list = []
shirtdk_list = []
type_name_list = ['shortshirt', 'longshirt', 'shirtdk']
color_name_list = ['red', 'green', 'yellow', 'blue', 'brown', 'pink', 'gray', 'black', 'white','unknown']

attri_target_count = 0
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
grey_list = []
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
                                shortshirt_list.append(file_name_list[xml_count])
                                temp_str += 'short_sleeve,'
                            elif result == 'long_sleeve':
                                longshirt += 1
                                longshirt_list.append(file_name_list[xml_count])
                                temp_str += 'long_sleeve,'
                            else:
                                shirtdk += 1
                                shortshirt_list.append(file_name_list[xml_count])
                                temp_str += 'shirtdk,'
                            attri = result
                        else:
                            if label_name == 'top_red':
                                top_red += 1
                                temp_str += 'top_red'
                                red_list.append(file_name_list[xml_count])
                            elif label_name == 'top_yellow':
                                top_yellow += 1
                                yellow_list.append(file_name_list[xml_count])
                                temp_str += 'top_yellow'
                            elif label_name == 'top_green':
                                top_green += 1
                                green_list.append(file_name_list[xml_count])
                                temp_str += 'top_green'
                            elif label_name == 'top_blue':
                                top_blue += 1
                                blue_list.append(file_name_list[xml_count])
                                temp_str += 'top_blue'
                            elif label_name == 'top_black':
                                top_black += 1
                                black_list.append(file_name_list[xml_count])
                                temp_str += 'top_black'
                            elif label_name == 'top_brown':
                                top_brown += 1
                                brown_list.append(file_name_list[xml_count])
                                temp_str += 'top_brown'
                            elif label_name == 'top_pink':
                                top_pink += 1
                                pink_list.append(file_name_list[xml_count])
                                temp_str += 'top_pink'
                            elif label_name == 'top_grey':
                                top_grey += 1
                                grey_list.append(file_name_list[xml_count])
                                temp_str += 'top_grey'
                            elif label_name == 'top_white':
                                top_white += 1
                                white_list.append(file_name_list[xml_count])
                                temp_str += 'top_white'
                            elif label_name == 'top_color_unknown':
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

total_list = [longshirt, shortshirt, shirtdk, top_red, top_brown,
              top_color_unknown, top_white, top_black, top_grey,
              top_blue, top_green, top_yellow, top_pink]
total_name_list = ['longshirt', 'shortshirt', 'shirtdk', 'top_red', 'top_brown',
              'top_color_unknown', 'top_white', 'top_black', 'top_grey',
              'top_blue', 'top_green', 'top_yellow', 'top_pink']
min_name = comparison(total_list)
temp = len(min_name)
maximum = total_list[int(temp)-1]
attri_min_name_list = []
attri_min_list = []
pop_file_name_list = []

for x in min_name:
    temp = int(x)
    attri_min_list.append(total_list.pop(temp))
    attri_min_name_list.append(total_name_list.pop(temp))
min_count = 0
result_list = []
unknown_copy_list = unknown_list.copy()
shirtdk_copy_list = shirtdk_list.copy()
brown_copy_list = brown_list.copy()
print("테스트셋에 들어갈 파일 분류 시작")

while True: #분류진행 코드
    if min_count == 0:
        if top_color_unknown >= 1:
            temp = len(unknown_copy_list)
            list_len = int(temp)
            if list_len > 1:
                random_num = random.randint(0, list_len-1)
                target_file = unknown_copy_list.pop(random_num)
                top_color_unknown -= 1
            else:
                target_file = unknown_copy_list[0]
            if not(target_file in result_list):
                result_list.append(target_file)
        else:
            print("첫 번째 최소값 분류 완료")
            min_count += 1
    elif min_count == 1: #shirtdk
        if shirtdk >= 1:
            temp = len(shirtdk_copy_list)
            list_len = int(temp)
            if list_len > 1:
                random_num = random.randint(0, list_len - 1)
                target_file = shirtdk_copy_list.pop(random_num)
                shirtdk -= 1
            else:
                target_file = shirtdk_copy_list[0]
            if not(target_file in result_list):
                result_list.append(target_file)
        else:
            print("두 번째 최소값 분류 완료")
            min_count += 1
    elif min_count == 2: #top_brown
        if top_brown >= 1:
            temp = len(brown_copy_list)
            list_len = int(temp)
            if list_len > 1:
                random_num = random.randint(0, list_len-1)
                target_file = brown_copy_list.pop(random_num)
                top_brown -= 1
            else:
                target_file = brown_copy_list[0]
            result_list.append(target_file)
            if not (target_file in result_list):
                result_list.append(target_file)
        else:
            print("세 번째 최소값 분류 완료")
            break
temp = ''
for x in result_list:
    temp += x+'\n'
file = open(file_path, 'w')
file.write(temp)
file.close()

print("EXIT")
print(time.time()-start)