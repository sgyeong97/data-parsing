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

root_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_DataSet'
target_path = 'D:\신지영_업무\Dataset_표준편차'
empty_path = os.listdir(root_path)
path_name_list = []
path_list = []
file_list = []
name_list = []

xml_list_count = 0
none_xml_count = 0
# index = empty_path.index('Result')
# empty_path.pop(index)
# empty_path.remove('Info')
# empty_path.sort()
# empty_path == ['UniTrain2']
# target_list = ['background1']
# for x in empty_path:
#     empty = str(x)
#     # 대상을 추려야 할 경우에 사용
#     # if empty in target_list:
#     #     path = os.path.join(root_path, empty)
#     #     path_list.append(path)
#     #     path_name_list.append(empty)
#
#     path = os.path.join(root_path, empty)
#     path_list.append(path)
#     path_name_list.append(empty)
path = 'D:\신지영_업무\Dataset_표준편차\DataSet\\UniTrain2'
for x in os.listdir(path):
    if x.endswith('.xml'):
        if x.startswith('0_'):
            empty = os.path.join(path, x)
            path_list.append(empty)

# answer = ['car', 'person']
answer = ['car','person']
attr = ['width', 'height', 'box']
count = 0
car_count = 0 #차 객체 count
person_count = 0 #사람 객체 count
print("시작")
dir_count = 1
c_std_w = 0
c_std_h = 0
c_std_b = 0
p_std_w = 0
p_std_h = 0
p_std_b = 0
#y축 값 기준 최대값 뽑는데 사용
c_w_m = 0
c_h_m = 0
c_b_m = 0
p_w_m = 0
p_h_m = 0
p_b_m = 0
#x축 값 기준 최대값 뽑는데 사용
c_w_x_max = 0
c_h_x_max = 0
c_b_x_max = 0
p_w_x_max = 0
p_h_x_max = 0
p_b_x_max = 0
#x축 값 기준 최대값 뽑는데 사용
c_w_x_min = 0
c_h_x_min = 0
c_b_x_min = 0
p_w_x_min = 0
p_h_x_min = 0
p_b_x_min = 0
c_height_list = []
c_width_list = []
c_box_len_list = []
p_height_list = []
p_width_list = []
p_box_len_list = []
dir_len = len(path_list)
# for y in path_list:
#     empty = y
#     xml_list = []
#     print("디렉터리 단위  작업 = %d/%s" % (dir_count,dir_len))
#     dir_count += 1

    # for z in path_list:
        # print(z)
        # input()
        # if z.endswith('xml'):
        #     if z.startswith('0_'): #0_ = 중앙,평균 만족값 통계
        #         xml_list.append(z)
        #         temp = z.split('.')
        #         name_list.append(temp[0])
for x in path_list:
    path = os.path.join(y,x)
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
                bndbox = child.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                width = abs(xmin - xmax)
                height = abs(ymin - ymax)
                box = abs(width * height)
                if name == 'car':
                    c_width_list.append(width)
                    c_height_list.append(height)
                    c_box_len_list.append(box)
                if name == 'person':
                    p_width_list.append(width)
                    p_height_list.append(height)
                    p_box_len_list.append(box)
        except:
            none_xml_count += 1
print("리스트 생성 완료")
c_width_list.sort()
c_height_list.sort()
c_box_len_list.sort()
p_width_list.sort()
p_height_list.sort()
p_box_len_list.sort()
p_w_max_list = []
p_h_max_list = []
p_b_max_list = []
print("그래프 생성")
file_count = 0
for label_type in answer:
    for attr_type in attr:
        w_label = []
        w_count = []
        h_label = []
        h_count = []
        b_label = []
        b_count = []
        if attr_type == 'width':
            if label_type == 'car':
                for x in c_width_list:
                    if not(x in w_label):
                        w_label.append(x)
                for x in range(0, len(w_label)):
                    w_count.append(0)
                for x in c_width_list:
                    if x in w_label:
                        index = w_label.index(x)
                        w_count[index] += 1
            if label_type == 'person':
                for x in p_width_list:
                    if not(x in w_label):
                        w_label.append(x)
                for x in range(0, len(w_label)):
                    w_count.append(0)
                for x in p_width_list:
                    if x in w_label:
                        index = w_label.index(x)
                        w_count[index] += 1
            file_count += 1
            # x = w_label / y = w_count
            plt.figure(figsize=(10, 10))
            plt.xlabel('Width len')
            plt.ylabel('Count')
            plt.plot(w_label, w_count, c='r',  alpha=0.5)
            plt.grid()
            if label_type == 'car':
                plt.plot(w_label, w_count, c='r', alpha=0.5)
                plt.title('%s %s' % (label_type, attr_type))
                c_std_w = np.std(c_width_list)
                c_w_m = np.mean(c_width_list)
                min_index = w_count.index(min(w_count))
                c_w_min_count = w_count[min_index]
                c_w_min_label = w_label[min_index]
                max_index = w_count.index(max(w_count))
                c_w_max_count = w_count[max_index]
                c_w_max_label = w_label[max_index]
                c_w_x_max = max(w_label)
                c_w_x_min = min(w_label)
                df = pd.DataFrame(
                    {
                        "Count" : w_count
                    }, index = w_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            if label_type == 'person':
                plt.title('%s %s' % (label_type, attr_type))
                p_std_w = np.std(p_width_list)
                p_w_m = np.mean(p_width_list)
                min_index = w_count.index(min(w_count))
                p_w_min_count = w_count[min_index]
                p_w_min_label = w_label[min_index]
                max_index = w_count.index(max(w_count))
                p_w_max_count = w_count[max_index]
                p_w_max_label = w_label[max_index]
                p_w_x_max = (max(w_label))
                p_w_x_min = min(w_label)
                count = 0
                for x in w_count:
                    if p_w_max_count == x:
                        p_w_max_list.append(w_label[count])
                    count += 1
                df = pd.DataFrame(
                    {
                        "Count" : w_count
                    }, index = w_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            file_path = os.path.join(target_path,'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)

        if attr_type == 'height':
            if label_type == 'car':
                for x in c_height_list:
                    if not (x in h_label):
                        h_label.append(x)
                for x in range(0, len(h_label)):
                    h_count.append(0)
                for x in c_height_list:
                    if x in h_label:
                        index = h_label.index(x)
                        h_count[index] += 1
            if label_type == 'person':
                for x in p_height_list:
                    if not (x in h_label):
                        h_label.append(x)
                for x in range(0, len(h_label)):
                    h_count.append(0)
                for x in p_height_list:
                    if x in h_label:
                        index = h_label.index(x)
                        h_count[index] += 1
            file_count += 1
            plt.figure(figsize=(10, 10))
            plt.xlabel('Height len')
            plt.ylabel('Count')
            plt.plot(h_label, h_count, c='b',  alpha=0.5)
            plt.grid()
            if label_type == 'car':
                plt.title('%s %s' % (label_type, attr_type))
                c_std_h = np.std(c_height_list)
                c_h_m = np.mean(c_height_list)
                min_index = h_count.index(min(h_count))
                c_h_min_count = h_count[min_index]
                c_h_min_label = h_label[min_index]
                max_index = h_count.index(max(h_count))
                c_h_max_count = h_count[max_index]
                c_h_max_label = h_label[max_index]
                c_h_x_max = max(h_label)
                c_h_x_min = min(h_label)
                df = pd.DataFrame(
                    {
                        "Count" : h_count
                    }, index = h_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            else:
                plt.title('%s %s' % (label_type, attr_type))
                p_std_h = np.std(p_height_list)
                p_h_m = np.mean(p_height_list)
                min_index = h_count.index(min(h_count))
                p_h_min_count = h_count[min_index]
                p_h_min_label = h_label[min_index]
                max_index = h_count.index(max(h_count))
                p_h_max_count = h_count[max_index]
                p_h_max_label = h_label[max_index]
                p_h_x_max = max(h_label)
                p_h_x_min = min(h_label)
                count = 0
                for x in h_count:
                    if p_h_max_count == x:
                        p_h_max_list.append(h_label[count])
                    count += 1
                df = pd.DataFrame(
                    {
                        "Count" : h_count
                    }, index = h_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            file_path = os.path.join(target_path,'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)
        if attr_type == 'box':
            if label_type == 'car':
                for x in c_box_len_list:
                    if not (x in b_label):
                        b_label.append(x)
                for x in range(0, len(b_label)):
                    b_count.append(0)
                for x in c_box_len_list:
                    if x in b_label:
                        index = b_label.index(x)
                        b_count[index] += 1
            if label_type == 'person':
                for x in p_box_len_list:
                    if not (x in b_label):
                        b_label.append(x)
                for x in range(0, len(b_label)):
                    b_count.append(0)
                for x in p_box_len_list:
                    if x in b_label:
                        index = b_label.index(x)
                        b_count[index] += 1
            count = 0
            # for x in b_count:
            #     if x <= 2:
            #         b_count.pop(count)
            #         b_label.pop(count)
            #     count += 1
            file_count += 1
            plt.figure(figsize=(20, 10))
            plt.xlabel('Box len')
            plt.ylabel('Count')
            plt.plot(b_label, b_count, c='g',  alpha=0.5)
            if label_type == 'car':
                plt.title('%s %s' % (label_type, attr_type))
                c_std_b = np.std(c_box_len_list)
                c_b_m = np.mean(c_box_len_list)
                min_index = b_count.index(min(b_count))
                c_b_min_count = b_count[min_index]
                c_b_min_label = b_label[min_index]
                max_index = b_count.index(max(b_count))
                c_b_max_count = b_count[max_index]
                c_b_max_label = b_label[max_index]
                c_b_x_max = max(b_label)
                c_b_x_min = min(b_label)
                df = pd.DataFrame(
                    {
                        "Count" : b_count
                    }, index = b_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            else:
                plt.title('%s %s' % (label_type, attr_type))
                p_std_b = np.std(p_box_len_list)
                p_b_m = np.mean(p_box_len_list)
                min_index = b_count.index(min(b_count))
                p_b_min_count = b_count[min_index]
                p_b_min_label = b_label[min_index]
                max_index = b_count.index(max(b_count))
                p_b_max_count = b_count[max_index]
                p_b_max_label = b_label[max_index]
                p_b_x_max = max(b_label)
                p_b_x_min = min(b_label)
                count = 0
                for x in b_count:
                    if p_b_max_count == x:
                        p_b_max_list.append(b_label[count])
                    count += 1
                df = pd.DataFrame(
                    {
                        "Count" : b_count
                    }, index = b_label
                )
                xlsx_file = os.path.join(target_path, 'Dataset_%s_%s.xlsx' % (label_type, attr_type))
                df.to_excel(xlsx_file)
            file_path = os.path.join(target_path, 'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)
        print("그래프 생성 완료")
file = open(os.path.join(target_path, 'info.txt'), 'w')
file.write('Car정보\nWidth 표준편차/%s/평균/%s\n(y축 기준)최소값/(%d,%d)/최고값/(%d,%d)\n(x축 기준) 최소값/%d/최고값/%d\n\nHeight 표준편차/%s/평균/%s\n(y축 기준)최소값/(%d,%d)/최고값/(%d,%d)\n(x축 기준)최소값/%d/최고값/%d\n\nBox 표준편차/%s/평균/%s\n(y축 기준) 최소값/(%d,%d) / 최고값/(%d,%d)\n(y축 기준) 최소값/%d/최고값/%d\n' %(c_std_w, c_w_m, c_w_min_count, c_w_min_label, c_w_max_count, c_w_max_label,c_w_x_min,c_w_x_max, c_std_h, c_h_m, c_h_min_count, c_h_min_label, c_h_max_count, c_h_max_label,c_h_x_min, c_h_x_max, c_std_b, c_b_m, c_b_min_count, c_b_min_label, c_b_max_count, c_b_max_label, c_b_x_min, c_b_x_max) + '\nPerson 정보\nWidth 표준편차/%s/평균/%s\n(y축 기준)최소값/(%d,%d)/최고값/(%d,%d)\n(x축 기준) 최소값/%d/ 최고값/%d\n\nHeight 표준편차/%s / 평균/%s\n(y축 기준)최소값/(%d,%d) / 최고값/(%d,%d)\n(x축 기준)최소값/%d / 최고값/%d\n\nBox 표준편/%s / 평균/%s\n(y축 기준) 최소값/(%d,%d) / 최고값/(%d,%d)\n(x축 기준) 최소값/%d / 최고값/%d\n' %(p_std_w, p_w_m, p_w_min_count, p_w_min_label, p_w_max_count, p_w_max_label,p_w_x_min,p_w_x_max, p_std_h, p_h_m, p_h_min_count, p_h_min_label, p_h_max_count, p_h_max_label,p_h_x_min, p_h_x_max, p_std_b, p_b_m, p_b_min_count, p_b_min_label, p_b_max_count, p_b_max_label, p_b_x_min, p_b_x_max))
file.close()

# print(p_w_max_list)
# print(p_h_max_list)
# print(p_b_max_list)
