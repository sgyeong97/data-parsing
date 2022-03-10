#!/usr/bin/python
# -*- coding: UTF-8

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import DataFrame
from xml.etree.ElementTree import ElementTree, Element, SubElement
from xml.etree.ElementTree import parse
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

root_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_2차'
target_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_2차\Info\Result'
move_xmls_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_중앙_yolo화\\xmls'
empty_path = os.listdir(root_path)
path_name_list = []
path_list = []
file_list = []
name_list = []

xml_list_count = 0
none_xml_count = 0
empty_path.remove('Info')
empty_path.sort()
# target_list = ['background1']
for x in empty_path:
    empty = str(x)
    # 대상을 추려야 할 경우에 사용
    # if empty in target_list:
    #     path = os.path.join(root_path, empty)
    #     path_list.append(path)
    #     path_name_list.append(empty)

    path = os.path.join(root_path, empty)
    path_list.append(path)
    path_name_list.append(empty)

# answer = ['car', 'person']
answer = ['car','person']
attr = ['width', 'height', 'box']
count = 0
print("시작")
dir_count = 0
total_txt = ''
c_height_list = []
c_width_list = []
c_box_len_list = []
p_height_list = []
p_width_list = []
p_box_len_list = []
dir_len = len(path_list)
for y in path_list:
    empty = y
    xml_list = []
    print("디렉터리 단위  작업 = %d/%s" % (dir_count+1,dir_len))
    car_count = 0 #차 객체 count
    person_count = 0 #사람 객체 count
    for z in os.listdir(empty):
        # print(z)
        # input()
        if z.endswith('xml'):
            if z.startswith('1_'): #1_ = 중앙 만족값 통계 / 0_ = 평균값 만족
                xml_list.append(z)
                temp = z.split('.')
                name_list.append(temp[0])
    for x in xml_list:
        path = os.path.join(y,x)
        copy_path = os.path.join(move_xmls_path, x)
        shutil.copy(path, copy_path)
        if path.endswith('xml'):
            # print(path)
            try:
                tree = parse(path)
                note = tree.getroot()
                for child in note.findall('object'):
                    name = child.find('name').text
                    if name in ['bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car', 'car']:
                        name = 'car'
                        car_count += 1
                    elif name == 'person':
                        person_count += 1
            except:
                none_xml_count += 1
    # total_txt = 'Car Count = %d\nPerson Count = %d'%(car_count, person_count)
    # path = os.path.join('D:\신지영_업무\Dataset_표준편차\크기분류_2차\Info\Result', '평균값_%s.txt'%(empty_path[dir_count]))
    # dir_count += 1
    # file = open(path, 'w')
    # file.write(total_txt)
    # file.close()
