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

root_path = 'D:\신지영_업무\Dataset_표준편차\DataSet'
copy_root_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_2차'
info_path = 'D:\신지영_업무\Dataset_표준편차\크기분류_2차\Info'

dir_list = os.listdir(root_path)
dir_list.remove('Result')

def indent(elem, level = 0):
    i = '\n'+level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i+"    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

for dir_name in dir_list:
    try:
        empty = os.path.join(copy_root_path, dir_name)
        os.mkdir(empty)
    except:
        pass

    target_path = os.path.join(root_path, dir_name)
    file_copy_path = os.path.join(copy_root_path, dir_name)

    xml_name_list = []


    total_file_count = 0
    xml_file_count = 0
    file_count = 0
    m_file_count = 0
    a_file_count = 0
    car_count = 0
    person_count = 0
    car_object_count = 0
    person_object_count = 0

    for x in os.listdir(target_path):
        if x.endswith('xml'):
            xml_name_list.append(x)
            xml_file_count += 1

    for file_name in xml_name_list:
        file_path = os.path.join(target_path, file_name)
        file_contents = []  # 중앙값, 평균 만족
        median_file_contents = []  # 중앙값 만족
        average_file_contents = []  # 평균 만족
        try:
            tree = parse(file_path)
            note = tree.getroot()
            file_person_count = 0
            median_person_count = 0
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
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                width =abs(xmax-xmin)
                height = abs(ymax-ymin)
                if name == 'car':
                    if width >= 28 and height >= 23: # 중앙값보다 큰 경우
                        if width >= 113.164 and height >= 86.729: #평균값 만족 경우
                            file_contents.append('%s,%d,%d,%d,%d' % (name,xmin,ymin,xmax,ymax))
                            median_file_contents.append('%s,%d,%d,%d,%d' % (name, xmin, ymin, xmax, ymax))
                            car_count += 1
                        else: #중앙값만 만족하는 경우
                            median_file_contents.append('%s,%d,%d,%d,%d' % (name,xmin,ymin,xmax,ymax))
                            car_count += 1
                elif name == 'person':
                    if width >= 15 and height >= 41:
                        if width >= 38.637 and height >= 88.462:
                            file_contents.append('%s,%d,%d,%d,%d' % (name,xmin,ymin,xmax,ymax))
                            file_person_count += 1
                            median_file_contents.append('%s,%d,%d,%d,%d' % (name, xmin, ymin, xmax, ymax))
                            median_person_count += 1
                            person_count += 1
                        else:
                            median_file_contents.append('%s,%d,%d,%d,%d' % (name,xmin,ymin,xmax,ymax))
                            median_person_count += 1
                            person_count += 1
            if file_person_count > 0:
                if len(file_contents):
                    file_bool = True
                    file_count += 1
                    name = file_name.split('.')
                    root = Element('annotation')
                    SubElement(root, 'folder').text = ""
                    SubElement(root, 'filename').text = name[0]+'.jpg'
                    SubElement(root, 'path').text = ""
                    source = SubElement(root, 'source')
                    SubElement(source, 'database').text = 'Unknown'
                    size = SubElement(root,'size')
                    SubElement(size, 'width').text = str(img_width)
                    SubElement(size, 'height').text = str(img_height)
                    SubElement(size, 'depth').text = '3'
                    SubElement(root, 'segmented').text = '0'

                    for line in file_contents:
                        try:
                            obj = SubElement(root, 'object')
                            str_split = line.split(',')
                            str_split[4] = str_split[4].rstrip()
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
                            pass #공백의 경우 pass
                    indent(root)
                    tree = ElementTree(root)
                    path = os.path.join(file_copy_path, '0_'+file_name) #0 = 평균값 만족
                    tree.write(path)
            if median_person_count > 0:
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
                    indent(m_root)
                    tree = ElementTree(m_root)
                    path = os.path.join(file_copy_path, '1_' + file_name) # 중앙값 만족
                    tree.write(path)
        except:
            file_bool = False
            pass
        if file_bool == True:
            total_file_count += 1

    total_txt = ("원본 디렉터리 내부 xml 파일 수량 = %d\nFile_Count = %d\n중앙,평균 만족 File_count = %d\n중앙만족 File_count = %d\n분류 후 생성 파일 수량 = %d" % (xml_file_count,total_file_count, file_count, m_file_count, (file_count+m_file_count)))
    total_txt += ("\nCar객체 수 = %d\nCar객체 분류 수 = %d\nPerson객체 수 = %d\nPerson객체 분류 수 = %d" % (car_object_count, car_count, person_object_count, person_count))
    path = os.path.join(info_path, '%s.txt' % dir_name)
    file = open(path, 'w')
    file.write(total_txt)
    file.close()