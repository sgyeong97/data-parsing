import os
import shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
from pandas import DataFrame
from xml.etree.ElementTree import ElementTree, Element, SubElement
from xml.etree.ElementTree import parse
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

root_path = 'D:\신지영_업무\Dataset_표준편차\DataSet'
empty_path = os.listdir(root_path)
path_name_list = []
path_list = []
file_list = []
name_list = []

xml_list_count = 0
index = empty_path.index('Result')
empty_path.pop(index)
empty_path.sort()

for x in empty_path:
    empty = str(x)
    path = os.path.join(root_path, empty)
    path_list.append(path)
    path_name_list.append(empty)
answer = ['car', 'person']
attr = ['width', 'height', 'box']
count = 0
for label_type in answer:
    height_list = []
    width_list = []
    box_len_list = []
    xml_count = 0
    none_xml_count = 0

    for y in path_list:
        empty = y
        xml_list = []
        for z in os.listdir(empty):
            # print(z)
            # input()
            if z.endswith('xml'):
                xml_count += 1
                xml_list.append(z)
                temp = z.split('.')
                name_list.append(temp[0])
        for x in xml_list:
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
                        elif name == 'person':
                            pass
                        else:
                            pass
                        if label_type == name:
                            bndbox = child.find('bndbox')
                            xmin = int(float(bndbox.find('xmin').text))
                            ymin = int(float(bndbox.find('ymin').text))
                            xmax = int(float(bndbox.find('xmax').text))
                            ymax = int(float(bndbox.find('ymax').text))
                            width = abs(xmin-xmax)
                            height = abs(ymin-ymax)
                            box = abs(width*height)
                            # print(width)
                            # print(height)
                            # print(box)
                            # input()
                            width_list.append(width)
                            height_list.append(height)
                            box_len_list.append(box)
                except:
                    none_xml_count += 1
    print(xml_count)
    print(none_xml_count)
    width_list.sort()
    height_list.sort()
    box_len_list.sort()
    file_count = 0
    for attr_type in attr:
        w_label = []
        w_count = []
        h_label = []
        h_count = []
        b_label = []
        b_count = []
        if attr_type == 'width':
            std = np.std(width_list)
            mean = np.mean(width_list)
            data = width_list
            x = np.linspace(min(data), max(data), 100)
            plt.hist(data, bins='auto')
            plt.grid()
            plt.plot(x, norm.pdf(x, mean, std))
            plt.title("%s %s" % (label_type, attr_type))
            file_path = os.path.join('D:\신지영_업무\Dataset_표준편차\DataSet\Result', 'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)
            exit()
        elif attr_type == 'height':
            std = np.std(height_list)
            mean = np.mean(height_list)
            data = height_list
            x = np.linspace(min(data), max(data), 100)
            plt.hist(data, bins='auto')
            plt.grid()
            plt.plot(x, norm.pdf(x, mean, std))
            plt.title("%s %s" % (label_type, attr_type))
            file_path = os.path.join('D:\신지영_업무\Dataset_표준편차\DataSet\Result',
                                     'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)
        elif attr_type == 'box':
            std = np.std(box_len_list)
            mean = np.mean(box_len_list)
            data = box_len_list
            x = np.linspace(min(data), max(data), 100)
            plt.hist(data, bins='auto')
            plt.grid()
            plt.plot(x, norm.pdf(x, mean, std))
            plt.title("%s %s" % (label_type, attr_type))
            file_path = os.path.join('D:\신지영_업무\Dataset_표준편차\DataSet\Result',
                                     'Dataset_%s_%s.jpg' % (label_type, attr_type))
            plt.savefig(file_path)

