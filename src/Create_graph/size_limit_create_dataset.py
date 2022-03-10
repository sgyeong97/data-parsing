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

target_path = 'D:\신지영_업무\Dataset_표준편차\DataSet\\UniTrain2'
file_copy_path = 'D:\신지영_업무\Dataset_표준편차\크기제한_DataSet\\UniTrain2'
xml_name_list = []
car_object_count = 0
person_object_count = 0
total_file_count = 0
file_count = 0
m_file_count = 0
a_file_count = 0

file_contents = [] #중앙값, 평균 만족
median_file_contents = [] #중앙값 만족
average_file_contents = [] #평균 만족

for x in os.listdir(target_path):
    if x.endswith('xml'):
        xml_name_list.append(x)

for file_name in xml_name_list:
    file_path = os.path.join(target_path, file_name)
    tree = parse(file_path)
    note = tree.getroot()
    file_person_count = 0
    img_width = 0
    img_height = 0
    file_bool = False
    for child in note.findall('object'):
        name = child.find('name').text
        if name in ['bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car', 'car']:
            name = 'car'
            car_object_count += 1
        elif name == 'person':
            person_object_count += 1
        img_size = child.find('size')
        # img_width = int(img_size.find('width').text)
        # img_height = int(img_size.find('height').text)
        img_width = 1920
        img_height = 1080

        bndbox = child.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)
        width =abs(xmax-xmin)
        height = abs(ymax-ymin)
        if name == 'car':
            if width >= 28 and height >= 23: # 중앙값보다 큰 경우
                if width >= 113.164 and height >= 86.729: #평균값 보다 큰 경우
                    file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
                else:
                    median_file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
            elif width >= 113.164 and height >= 86.729:
                average_file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
        elif name == 'person':
            if width >= 15 and height >= 41:
                if width >= 38.637 and height >= 88.462:
                    file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
                    file_person_count += 1
                else:
                    median_file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
                    file_person_count += 1
            elif width >= 38.637 and height >= 88.462:
                average_file_contents.append('%s,%f,%f,%f,%f\n' % (name,xmin,ymin,xmax,ymax))
                file_person_count += 1
    if file_person_count > 0:
        if len(file_contents):
            file_bool = True
            file_count += 1
            name = file_name.split('.')
            root = Element('annotation')
            SubElement(root, 'folder').text = ''
            SubElement(root, 'filename').text = name[0]+'.jpg'
            SubElement(root, 'path').text = ''
            source = SubElement(root, 'source')
            SubElement(source, 'database').text = 'Unknown'
            size = SubElement(root,'size')
            SubElement(size, 'width').text = str(img_width)
            SubElement(size, 'height').text = str(img_height)
            SubElement(size, 'depth').text = '3'
            SubElement(root,'segmented').text = '0'
            for line in file_contents:
                try:
                    obj = SubElement(root, 'object')
                    str_split = line.split(',')
                    SubElement(obj,'name').text = str_split[0]
                    SubElement(obj,'pose').text = 'Unspecified'
                    SubElement(obj,'truncated').text = '0'
                    SubElement(obj, 'difficult').text = '0'
                    bbox = SubElement(obj, 'bndbox')
                    SubElement(bbox, 'xmin').text = str_split[1]
                    SubElement(bbox, 'ymin').text = str_split[2]
                    SubElement(bbox, 'xmax').text = str_split[3]
                    SubElement(bbox, 'ymax').text = str_split[4]
                except:
                    pass #공백의 경우 pass
            tree = ElementTree(root)
            path = os.path.join(file_copy_path, '2_'+file_name)
            tree.write(path)

        if len(median_file_contents):
            file_bool = True
            m_file_count += 1
            name = file_name.split('.')
            m_root = Element('annotation')
            SubElement(m_root, 'folder').text = ''
            SubElement(m_root, 'filename').text = name[0] + '.jpg'
            SubElement(m_root, 'path').text = ''
            source = SubElement(m_root, 'source')
            SubElement(source, 'database').text = 'Unknown'
            size = SubElement(m_root, 'size')
            SubElement(size, 'width').text = str(img_width)
            SubElement(size, 'height').text = str(img_height)
            SubElement(size, 'depth').text = '3'
            SubElement(m_root, 'segmented').text = '0'
            for line in median_file_contents:
                try:
                    obj = SubElement(m_root, 'object')
                    str_split = line.split(',')
                    SubElement(obj, 'name').text = str_split[0]
                    SubElement(obj, 'pose').text = 'Unspecified'
                    SubElement(obj, 'truncated').text = '0'
                    SubElement(obj, 'difficult').text = '0'
                    bbox = SubElement(obj, 'bndbox')
                    SubElement(bbox, 'xmin').text = str_split[1]
                    SubElement(bbox, 'ymin').text = str_split[2]
                    SubElement(bbox, 'xmax').text = str_split[3]
                    SubElement(bbox, 'ymax').text = str_split[4]
                except:
                    pass  # 공백의 경우 pass
            tree = ElementTree(m_root)
            path = os.path.join(file_copy_path, '0_' + file_name)
            tree.write(path)

        if len(average_file_contents):
            file_bool = True
            a_file_count += 1
            name = file_name.split('.')
            a_root = Element('annotation')
            SubElement(a_root, 'folder').text = ''
            SubElement(a_root, 'filename').text = name[0] + '.jpg'
            SubElement(a_root, 'path').text = ''
            source = SubElement(a_root, 'source')
            SubElement(source, 'database').text = 'Unknown'
            size = SubElement(a_root, 'size')
            SubElement(size, 'width').text = str(img_width)
            SubElement(size, 'height').text = str(img_height)
            SubElement(size, 'depth').text = '3'
            SubElement(a_root, 'segmented').text = '0'
            for line in average_file_contents:
                try:
                    obj = SubElement(a_root, 'object')
                    str_split = line.split(',')
                    SubElement(obj, 'name').text = str_split[0]
                    SubElement(obj, 'pose').text = 'Unspecified'
                    SubElement(obj, 'truncated').text = '0'
                    SubElement(obj, 'difficult').text = '0'
                    bbox = SubElement(obj, 'bndbox')
                    SubElement(bbox, 'xmin').text = str_split[1]
                    SubElement(bbox, 'ymin').text = str_split[2]
                    SubElement(bbox, 'xmax').text = str_split[3]
                    SubElement(bbox, 'ymax').text = str_split[4]
                except:
                    pass  # 공백의 경우 pass
            tree = ElementTree(a_root)
            path = os.path.join(file_copy_path, '1_' + file_name)
            tree.write(path)

    if file_bool == True:
        total_file_count += 1

total_txt = ("File_Count = %d\n중앙,평균 만족 File_count = %d\n평균만족 File_count = %d\n중앙만족 File_count = %d" % (total_file_count, file_count, a_file_count, m_file_count))
path = os.path.join(file_copy_path, 'info.txt')
file = open(path, 'w')
file.write(total_txt)
file.close()