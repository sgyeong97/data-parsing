import os
import xml.etree.ElementTree
import cv2
import shutil
import time
import xml.etree.ElementTree
from bs4 import BeautifulSoup

start = time.time()

target_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Test\Xmls'
file_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images\\upper\Testz\\annotaions'

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
        file_name = file_name_list[xml_count]+'.txt'

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
                                long_sleeve, short_sleeve, unknown_sleeve = 0,1,0
                            elif result == 'long_sleeve':
                                long_sleeve, short_sleeve, unknown_sleeve = 1, 0, 0
                            else:
                                long_sleeve, short_sleeve, unknown_sleeve = 0,0,1
                            attri = result
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
        UPPER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(long_sleeve, short_sleeve, unknown_sleeve, top_red, top_yellow, top_green, top_blue, top_brown, top_pink, top_gray, top_black, top_white, top_color_unknown)

        file_name_path = os.path.join(file_path, file_name)
        file = open(file_name_path, 'w')
        file.write(UPPER_classes)
        file.close()

        xml_count += 1