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

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\Origin'
xml_list_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\Origin\Xmls'
file_path ='D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head\\file_list.txt'
result_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\head'

crop_img_list = []
xml_list = []
file_name_list = []
attri_list = []

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

total_list = [cap,visor,nonvisor,helmat,hood,nohat,hatdk,hatred,hatyellow,hatgreen,hatblue,hatbrwon,hatpink,hatgray,hatblack,hatwhite,unknown,short,long,bald, hairdk]

cap_list = []
visor_list = []
nonvisor_list = []
helmat_list = []
hood_list = []
nohat_list = []
hatdk_list = []
hatred_list = []
hatyellow_list = []
hatgreen_list = []
hatblue_list = []
hatbrwon_list = []
hatpink_list = []
hatgray_list = []
hatblack_list = []
hatwhite_list = []
unknown_list = []
short_list = []
long_list = []
bald_list = []
hairdk_list = []

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
        if return_count == 6:
            break
    return result

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
                                cap_list.append(file_name_list[xml_count])
                            elif result == 'brimmed':
                                visor += 1
                                visor_list.append(file_name_list[xml_count])
                            elif result == 'brimless':
                                nonvisor += 1
                                nonvisor_list.append(file_name_list[xml_count])
                            elif result == 'helmat':
                                helmat += 1
                                helmat_list.append(file_name_list[xml_count])
                            elif result == 'hood':
                                hood += 1
                                hood_list.append(file_name_list[xml_count])
                            elif result == 'hatless':
                                nohat += 1
                                nohat_list.append(file_name_list[xml_count])
                            else:
                                hatdk += 1
                                hatdk_list.append(file_name_list[xml_count])
                        elif label_name == 'hair':
                            if result == 'long':
                                long += 1
                                long_list.append(file_name_list[xml_count])
                            elif result == 'short':
                                short += 1
                                short_list.append(file_name_list[xml_count])
                            elif result == 'bald':
                                bald += 1
                                bald_list.append(file_name_list[xml_count])
                            else:
                                hairdk += 1
                                hairdk_list.append(file_name_list[xml_count])
                        else:
                            if 'hat_red' in label_name:
                                hatred += 1
                                hatred_list.append(file_name_list[xml_count])
                            if 'hat_yellow' in label_name:
                                hatyellow += 1
                                hatyellow_list.append(file_name_list[xml_count])
                            if 'hat_green' in label_name:
                                hatgreen += 1
                                hatgreen_list.append(file_name_list[xml_count])
                            if 'hat_blue' in label_name:
                                hatblue += 1
                                hatblue_list.append(file_name_list[xml_count])
                            if 'hat_brown' in label_name:
                                hatbrwon += 1
                                hatbrwon_list.append(file_name_list[xml_count])
                            if 'hat_black' in label_name:
                                hatblack += 1
                                hatblack_list.append(file_name_list[xml_count])
                            if 'hat_grey' in label_name:
                                hatgray += 1
                                hatgray_list.append(file_name_list[xml_count])
                            if 'hat_white' in label_name:
                                hatwhite += 1
                                hatwhite_list.append(file_name_list[xml_count])
                            if 'hat_pink' in label_name:
                                hatpink += 1
                                hatpink_list.append(file_name_list[xml_count])
                            if 'hat_color_unknown' in label_name:
                                unknown += 1
                                unknown_list.append(file_name_list[xml_count])
        xml_count += 1
print("총량 파일 생성")
total_list = [cap,visor,nonvisor,helmat,hood,nohat,hatdk,hatred,hatyellow,hatgreen,hatblue,hatbrwon,hatpink,hatgray,hatblack,hatwhite,unknown,short,long,bald, hairdk]
total_name_list = ['cap', 'visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrwon','hatpink','hatgray','hatblack','hatwhite','unknown','short','long','bald', 'hairdk']

df = pd.DataFrame(
    {
        "COUNT" : total_list
    },index=total_name_list
)

txt_file = os.path.join(result_path, 'head_total.xlsx')
df.to_excel(txt_file)

print("분류 시작")

result_list = []
index_list = []

cap_copy_list = cap_list.copy()
visor_copy_list = visor_list.copy()
nonvisor_copy_list = nonvisor_list.copy()
helmat_copy_list = helmat_list.copy()
hood_copy_list = hood_list.copy()
nohat_copy_list = nohat_list.copy()
hatdk_copy_list = hatdk_list.copy()
red_copy_list = hatred_list.copy()
yellow_copy_list = hatyellow_list.copy()
green_copy_list = hatgreen_list.copy()
blue_copy_list = hatblue_list.copy()
brown_copy_list = hatbrwon_list.copy()
pink_copy_list = hatpink_list.copy()
gray_copy_list = hatgray_list.copy()
black_copy_list = hatblack_list.copy()
white_copy_list = hatwhite_list.copy()
unknown_copy_list = unknown_list.copy()
short_copy_list = short_list.copy()
long_copy_list = long_list.copy()
bald_copy_list = bald_list.copy()
hairdk_copy_list = hairdk_list.copy()

cap_count = 0
visor_count = 0
hood_count = 0
nohat_count = 0
hatdk_count = 0
red_count = 0
blue_count = 0
gray_count = 0
black_count = 0
white_count = 0
short_count = 0
long_count = 0
bald_count = 0
hairdk_count = 0

remove_target = []
run_bool = True

short_count = 0
long_count = 0
hairdk_count = 0

while run_bool:
    in_run_bool = False

    if len(remove_target) == 12:
        run_bool = False
        print(remove_target)
        break
    print(red_count, blue_count, gray_count, black_count, white_count)
    if len(remove_target) < 12:
        if not('nonvisor' in remove_target):
            if len(nonvisor_copy_list) == 0:
                remove_target.append('nonvisor')
            else:
                if len(nonvisor_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(nonvisor_copy_list) - 1)
                temp = nonvisor_copy_list[random_num]
                nonvisor_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_copy_list.remove(temp)
                    blue_count += 1
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_copy_list.remove(temp)
                    gray_count += 1
                if temp in black_copy_list:
                    black_copy_list.remove(temp)
                    black_count += 1
                if temp in white_copy_list:
                    white_copy_list.remove(temp)
                    white_count += 1
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
        if not('helmat' in remove_target):
            if len(helmat_copy_list) == 0:
                remove_target.append('helmat')
            else:
                if len(helmat_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(helmat_copy_list) - 1)
                temp = helmat_copy_list[random_num]
                helmat_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_copy_list.remove(temp)
                    bald_count += 1
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
        if not ('red' in remove_target):
            if red_count >= 300:
                remove_target.append('red')
            else:
                if len(red_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(red_copy_list) - 1)
                red_count += 1
                temp = red_copy_list[random_num]
                red_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in cap_copy_list:
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in hood_copy_list:
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('yellow' in remove_target):
            if len(yellow_copy_list) == 0:
                remove_target.append('yellow')
            else:
                if len(yellow_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(yellow_copy_list) - 1)
                temp = yellow_copy_list[random_num]
                yellow_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in cap_copy_list:
                    in_run_bool = True
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in hood_copy_list:
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('green' in remove_target):
            if len(green_copy_list) == 0:
                remove_target.append('green')
            else:
                if len(green_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(green_copy_list) - 1)
                temp = green_copy_list[random_num]
                green_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in cap_copy_list:
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in hood_copy_list:
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    in_run_bool = True
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('blue' in remove_target):
            if blue_count >= 280:
                remove_target.append('blue')
            else:
                if len(blue_copy_list) <= 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(blue_copy_list) - 1)
                try:
                    temp = blue_copy_list[random_num]
                except:
                    print("오류발생")
                    print(len(blue_copy_list))
                    print(random_num)
                blue_copy_list.remove(temp)
                blue_count += 1
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('brown' in remove_target):
            if len(brown_copy_list) == 0:
                random_num = 0
                remove_target.append('brown')
            else:
                if len(brown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(brown_copy_list)-1)
                temp = brown_copy_list[random_num]
                brown_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in cap_copy_list:
                    in_run_bool = True
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    in_run_bool = True
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in hood_copy_list:
                    in_run_bool = True
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    in_run_bool = True
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    in_run_bool = True
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('pink' in remove_target):
            if len(pink_copy_list) == 0:
                remove_target.append('pink')
            else:
                if len(pink_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(pink_copy_list) - 1)
                temp = pink_copy_list[random_num]
                pink_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in cap_copy_list:
                    in_run_bool = True
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    in_run_bool = True
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in hood_copy_list:
                    in_run_bool = True
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    in_run_bool = True
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    in_run_bool = True
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('gray' in remove_target):
            if gray_count >= 170:
                remove_target.append('gray')
            else:
                if len(gray_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(gray_copy_list) - 1)
                temp = gray_copy_list[random_num]
                count_list = [cap_count, visor_count, hood_count, nohat_count, hatdk_count]
                count_list.sort()
                min_val = count_list[0]
                if cap_count == min_val:
                    if temp in cap_copy_list:
                        in_run_bool = True
                        cap_count += 1
                        cap_copy_list.remove(temp)
                if visor_count == min_val:
                    if temp in visor_copy_list:
                        in_run_bool = True
                        visor_count += 1
                        visor_copy_list.remove(temp)
                if hood_count == min_val:
                    if temp in hood_copy_list:
                        in_run_bool = True
                        hood_count += 1
                        hood_copy_list.remove(temp)
                if nohat_count == min_val:
                    if temp in nohat_copy_list:
                        in_run_bool = True
                        nohat_count += 1
                        nohat_copy_list.remove(temp)
                if hatdk_count == min_val:
                    if temp in hatdk_copy_list:
                        in_run_bool = True
                        hatdk_count += 1
                        hatdk_copy_list.remove(temp)
                if in_run_bool:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_head_%s' % empty
                    result_list.append(name)
                    if temp in nonvisor_copy_list:
                        nonvisor_copy_list.remove(temp)
                    if temp in helmat_copy_list:
                        helmat_copy_list.remove(temp)
                    if temp in short_copy_list:
                        short_copy_list.remove(temp)
                        short_count += 1
                    if temp in long_copy_list:
                        long_copy_list.remove(temp)
                        long_count += 1
                    if temp in bald_copy_list:
                        bald_count += 1
                        bald_copy_list.remove(temp)
                    if temp in hairdk_copy_list:
                        hairdk_copy_list.remove(temp)
                        hairdk_count += 1

                    if temp in red_copy_list:
                        red_count += 1
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_count += 1
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_count += 1
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_count += 1
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('black' in remove_target):
            if black_count >= 50:
                remove_target.append('black')
            else:
                if len(black_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(black_copy_list) - 1)
                temp = black_copy_list[random_num]
                black_count += 1
                black_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1

                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('white' in remove_target):
            if white_count >= 180:
                remove_target.append('white')
            else:
                if len(white_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(white_copy_list) - 1)
                temp = white_copy_list[random_num]
                white_count += 1
                white_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in unknown_copy_list:
                    unknown_copy_list.remove(temp)
        if not ('unknown' in remove_target):
            if len(unknown_copy_list) == 0:
                remove_target.append('unknown')
            else:
                if len(unknown_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(unknown_copy_list) - 1)
                temp = unknown_copy_list[random_num]
                unknown_copy_list.remove(temp)
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
                if temp in nonvisor_copy_list:
                    nonvisor_copy_list.remove(temp)
                if temp in helmat_copy_list:
                    helmat_copy_list.remove(temp)
                if temp in short_copy_list:
                    short_copy_list.remove(temp)
                    short_count += 1
                if temp in long_copy_list:
                    long_copy_list.remove(temp)
                    long_count += 1
                if temp in bald_copy_list:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                if temp in hairdk_copy_list:
                    hairdk_copy_list.remove(temp)
                    hairdk_count += 1
                if temp in cap_copy_list:
                    in_run_bool = True
                    cap_count += 1
                    cap_copy_list.remove(temp)
                if temp in visor_copy_list:
                    in_run_bool = True
                    visor_count += 1
                    visor_copy_list.remove(temp)
                if temp in hood_copy_list:
                    in_run_bool = True
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in nohat_copy_list:
                    in_run_bool = True
                    nohat_count += 1
                    nohat_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    in_run_bool = True
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if temp in red_copy_list:
                    red_count += 1
                    red_copy_list.remove(temp)
                if temp in yellow_copy_list:
                    yellow_copy_list.remove(temp)
                if temp in green_copy_list:
                    green_copy_list.remove(temp)
                if temp in blue_copy_list:
                    blue_count += 1
                    blue_copy_list.remove(temp)
                if temp in brown_copy_list:
                    brown_copy_list.remove(temp)
                if temp in pink_copy_list:
                    pink_copy_list.remove(temp)
                if temp in gray_copy_list:
                    gray_count += 1
                    gray_copy_list.remove(temp)
                if temp in black_copy_list:
                    black_count += 1
                    black_copy_list.remove(temp)
                if temp in white_copy_list:
                    white_count += 1
                    white_copy_list.remove(temp)
                    
remove_target = []
run_bool = True
in_run_bool = True
print("머리모양 분류 시작")
input()

while run_bool:
    if len(remove_target) == 4:
        run_bool = False
        print(remove_target)
        break

    print(bald_count, long_count, hatdk_count, hood_count)
    if len(remove_target) < 4:
        if not ('bald' in remove_target):
            if bald_count >= 300:
                remove_target.append('bald')
            else:
                if len(bald_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(bald_copy_list) - 1)
                temp = bald_copy_list[random_num]
                count_list = [cap_count, visor_count, hood_count, nohat_count, hatdk_count]
                count_list.sort()
                min_val = count_list[0]
                if cap_count == min_val:
                    if temp in cap_copy_list:
                        in_run_bool = True
                        cap_count += 1
                        cap_copy_list.remove(temp)
                elif visor_count == min_val:
                    if temp in visor_copy_list:
                        in_run_bool = True
                        visor_count += 1
                        visor_copy_list.remove(temp)
                elif hood_count == min_val:
                    if temp in hood_copy_list:
                        in_run_bool = True
                        hood_count += 1
                        hood_copy_list.remove(temp)
                elif nohat_count == min_val:
                    if temp in nohat_copy_list:
                        in_run_bool = True
                        nohat_count += 1
                        nohat_copy_list.remove(temp)
                elif hatdk_count == min_val:
                    if temp in hatdk_copy_list:
                        in_run_bool = True
                        hatdk_count += 1
                        hatdk_copy_list.remove(temp)
                if in_run_bool:
                    bald_count += 1
                    bald_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_head_%s' % empty
                    result_list.append(name)
                    if temp in cap_copy_list:
                        cap_copy_list.remove(temp)
                        cap_count += 1
                    if temp in visor_copy_list:
                        visor_copy_list.remove(temp)
                        visor_count += 1
                    if temp in nonvisor_copy_list:
                        nonvisor_copy_list.remove(temp)
                    if temp in helmat_copy_list:
                        helmat_copy_list.remove(temp)
                    if temp in hood_copy_list:
                        hood_copy_list.remove(temp)
                        hood_count += 1
                    if temp in nohat_copy_list:
                        nohat_copy_list.remove(temp)
                        nohat_count += 1
                    if temp in hatdk_copy_list:
                        hatdk_copy_list.remove(temp)
                        hatdk_count += 1
                    if temp in hairdk_copy_list:
                        hairdk_copy_list.remove(temp)
                        hairdk_count += 1
                    if temp in red_copy_list:
                        red_count += 1
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_count += 1
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_count += 1
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_count += 1
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_count += 1
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not ('long' in remove_target):
            if long_count >= 300:
                remove_target.append('long')
            else:
                if len(long_copy_list) == 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(long_copy_list) - 1)
                temp = long_copy_list[random_num]
                if temp in hood_copy_list:
                    in_run_bool = True
                    hood_count += 1
                    hood_copy_list.remove(temp)
                if temp in hatdk_copy_list:
                    in_run_bool = True
                    hatdk_count += 1
                    hatdk_copy_list.remove(temp)
                if in_run_bool:
                    long_count += 1
                    long_copy_list.remove(temp)
                    empty = temp[-6:]
                    name = 'atr_c_head_%s' % empty
                    result_list.append(name)
                    if temp in cap_copy_list:
                        cap_copy_list.remove(temp)
                        cap_count += 1
                    if temp in visor_copy_list:
                        visor_copy_list.remove(temp)
                        visor_count += 1
                    if temp in nonvisor_copy_list:
                        nonvisor_copy_list.remove(temp)
                    if temp in helmat_copy_list:
                        helmat_copy_list.remove(temp)
                    if temp in hood_copy_list:
                        hood_copy_list.remove(temp)
                        hood_count += 1
                    if temp in nohat_copy_list:
                        nohat_copy_list.remove(temp)
                        nohat_count += 1
                    if temp in hatdk_copy_list:
                        hatdk_copy_list.remove(temp)
                        hatdk_count += 1
                    if temp in hairdk_copy_list:
                        hairdk_copy_list.remove(temp)
                        hairdk_count += 1
                    if temp in red_copy_list:
                        red_count += 1
                        red_copy_list.remove(temp)
                    if temp in yellow_copy_list:
                        yellow_copy_list.remove(temp)
                    if temp in green_copy_list:
                        green_copy_list.remove(temp)
                    if temp in blue_copy_list:
                        blue_count += 1
                        blue_copy_list.remove(temp)
                    if temp in brown_copy_list:
                        brown_copy_list.remove(temp)
                    if temp in pink_copy_list:
                        pink_copy_list.remove(temp)
                    if temp in gray_copy_list:
                        gray_count += 1
                        gray_copy_list.remove(temp)
                    if temp in black_copy_list:
                        black_count += 1
                        black_copy_list.remove(temp)
                    if temp in white_copy_list:
                        white_count += 1
                        white_copy_list.remove(temp)
                    if temp in unknown_copy_list:
                        unknown_copy_list.remove(temp)
        if not('hood' in remove_target):
            if hood_count >= 300:
                remove_target.append('hood')
            else:
                if len(hood_copy_list) <= 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(hood_copy_list) - 1)
                try:
                    temp = hood_copy_list[random_num]
                except:
                    print(len(hood_copy_list))
                    print(hood_count)

                hood_copy_list.remove(temp)
                hood_count += 1
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)
        if not('hatdk' in remove_target):
            if hatdk_count >= 300:
                remove_target.append('hatdk')
            else:
                if len(hatdk_copy_list) <= 1:
                    random_num = 0
                else:
                    random_num = random.randint(0, len(hatdk_copy_list) - 1)
                temp = hatdk_copy_list[random_num]
                hatdk_copy_list.remove(temp)
                hatdk_count += 1
                empty = temp[-6:]
                name = 'atr_c_head_%s' % empty
                result_list.append(name)

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