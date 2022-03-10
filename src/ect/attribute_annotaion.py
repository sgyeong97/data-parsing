import os
import xml.etree.ElementTree
import cv2
import shutil
import time
import xml.etree.ElementTree
from bs4 import BeautifulSoup

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\common\Test_Set'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\common\\common_attribute_annotaion.txt'

xml_list = []
file_name_list = []
target_file_list = os.listdir(target_path)
for x in target_file_list:
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

xml_count = 0

str_result = ''
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
                        elif result == 'female':
                            woman += 1
                        else:
                            genderdk += 1
                    elif label_name == 'age':
                        if result == '8~13':
                            child += 1
                        elif result == '14~19':
                            teenager += 1
                        elif result == '20~70':
                            adult += 1
                        elif result == '70~':
                            oldperson += 1
                        else:
                            infant += 1
                    else:
                        if label_name == 'backpack':
                            backpack += 1
                        elif label_name == 'bagless':
                            bagnone += 1
                        elif label_name == 'unknown_bag':
                            bagdk += 1
                        elif label_name == 'plasticbag':
                            plasticbag += 1
                        elif label_name == 'shoulderbag':
                            shoulderbag += 1
                        elif label_name == 'handbag':
                            totebag += 1
                        elif label_name == 'bag_red':
                            red += 1
                        elif label_name == 'bag_yellow':
                            yellow += 1
                        elif label_name == 'bag_green':
                            green += 1
                        elif label_name == 'bag_blue':
                            blue += 1
                        elif label_name == 'bag_brown':
                            brown += 1
                        elif label_name == 'bag_pink':
                            pink += 1
                        elif label_name == 'bag_grey':
                            gray += 1
                        elif label_name == 'bag_black':
                            black += 1
                        elif label_name == 'bag_white':
                            white += 1
                        elif label_name == 'bag_color_unknown':
                            unknown += 1


        ALL_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(man, woman, genderdk, infant, child, teenager, adult, oldperson, backpack, totebag, shoulderbag, plasticbag, bagdk, bagnone, red, yellow, green, blue, brown, pink, gray, black, white, unknown)
        str_result += ALL_classes + '\n'

file = open(file_path, 'a')
for x in str_result:
    file.write(x)

file.close()