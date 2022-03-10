import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
from PIL import Image
from bs4 import BeautifulSoup
import cv2
import shutil
import numpy as np

crop_image_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_crop_images'
image_root_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_images'
cvat_xmls_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\_attribute_cvatxmls(7월2일추가작업분포함)'

image_path_list = os.listdir(image_root_path)
cvat_xmls_list = os.listdir(cvat_xmls_path)
img_name_list = []
upper_count = 0
lower_count = 0
head_count = 0
common_count = 0
crop_name = 'atr_c_'
for xmls_name_list in cvat_xmls_list:
    temp = xmls_name_list.split('.')
    name = temp[0]
    if name in image_path_list:
        img_path = os.path.join(image_root_path, name)
        xml_path = os.path.join(cvat_xmls_path, name+'.xml')
        file = open(xml_path, 'r', encoding='utf-8')
        lines = ''
        while True:
            line = file.readline()
            if not line: break
            lines += line
        file.close()
        bs = BeautifulSoup(lines, 'lxml')
        for img in bs.find_all('image'):
            img_name = img.get('name')
            img_name_list.append(img_name)
            for box in img.find_all("box"):
                label = (box.get('label'))
                temp = box.get('xbr')
                xbr = float(temp)
                temp = box.get('ybr')
                ybr = float(temp)
                temp = box.get('xtl')
                xtl = float(temp)
                temp = box.get('ytl')
                ytl = float(temp)
                """if label == 'upper':
                    crop_image_upper_path = os.path.join(crop_image_path, 'upper\Origin')
                    file_name = crop_name+'upper_{0:06d}'.format(upper_count)
                    crop_path = os.path.join(crop_image_upper_path, file_name+'.png')
                    split_xml_path = os.path.join(crop_image_upper_path, file_name+'.xml')
                    with open(split_xml_path, 'w') as txt:
                        txt.write(str(box))
                        txt.close()
                    upper_count += 1
                    image_path = os.path.join(img_path, img_name)
                    img = Image.open(image_path, 'r')
                    dim = (xtl, ytl, xbr, ybr)
                    crop_img = img.crop(dim)
                    crop_img.save(crop_path)
                elif label == 'lower':
                    crop_image_lower_path = os.path.join(crop_image_path, 'lower\Origin')
                    file_name = crop_name+'lower_{0:06d}'.format(lower_count)
                    crop_path = os.path.join(crop_image_lower_path, file_name+'.png')
                    split_xml_path = os.path.join(crop_image_lower_path, file_name+'.xml')
                    with open(split_xml_path, 'w') as txt:
                        txt.write(str(box))
                        txt.close()
                    lower_count += 1
                    image_path = os.path.join(img_path, img_name)
                    img = Image.open(image_path, 'r')
                    dim = (xtl, ytl, xbr, ybr)
                    crop_img = img.crop(dim)
                    crop_img.save(crop_path)
                elif label == 'head':
                    crop_image_head_path = os.path.join(crop_image_path, 'head\Origin')
                    file_name = crop_name+'head_{0:06d}'.format(head_count)
                    crop_path = os.path.join(crop_image_head_path, file_name + '.png')
                    split_xml_path = os.path.join(crop_image_head_path, file_name+'.xml')
                    with open(split_xml_path, 'w') as txt:
                        txt.write(str(box))
                        txt.close()
                    head_count += 1
                    image_path = os.path.join(img_path, img_name)
                    img = Image.open(image_path, 'r')
                    dim = (xtl, ytl, xbr, ybr)
                    crop_img = img.crop(dim)
                    crop_img.save(crop_path)"""
                if label == 'all':
                    crop_image_common_path = os.path.join(crop_image_path, 'common\Train')
                    file_name = crop_name+'common_{0:06d}'.format(common_count)
                    crop_path = os.path.join(crop_image_common_path, file_name+'.png')
                    split_xml_path = os.path.join(crop_image_common_path, file_name+'.xml')
                    with open(split_xml_path, 'w') as txt:
                        txt.write(str(box))
                        txt.close()
                    common_count += 1
                    image_path = os.path.join(img_path, img_name)
                    img = Image.open(image_path, 'r')
                    dom = (xtl, ytl, xbr, ybr)
                    crop_img = img.crop(dom)
                    crop_img.save(crop_path)
