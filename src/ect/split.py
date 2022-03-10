import os
import sys
from os.path import join
from xml.etree.ElementTree import ElementTree, SubElement, Element

target_dir = 'D:\신지영_업무\dataset\Download_LP_Images\yolo_csv형식있음'
txt_file_path = 'D:\신지영_업무\dataset\Download_LP_Images\yolo_csv형식있음\indian_license_plates.txt'
contants_list = []

f = open(txt_file_path, 'r')

count = 0
while True:
    line = f.readline()
    if not line: break
    temp = line.split(',')
    if count == 0:
        pass
    else:
        contants_list.append(temp)
    count += 1
f.close()
'''for x in contants_list:
    file_name, image_width, image_height, top_x, top_y, bottom_x, bottom_y = x

    root = Element('annotaion')
    SubElement(root, 'folder').text = ""
    SubElement(root, 'filenmae').text = file_name

    sourceTag = SubElement(root, 'source')
    SubElement(sourceTag, 'database').text = 'UnKnown'
    sizeTag = SubElement(root, 'size')
    SubElement(sizeTag, 'width').text = image_width
    SubElement(sizeTag, 'height').text = image_height
    SubElement(sizeTag, 'depth').text = '3'

    SubElement(root, 'segmented').text = '0'

    objTag = SubElement(root, 'object')
    SubElement(objTag, 'name').text = 'license plate'
    SubElement(objTag, 'pose').text = 'Unspecified'
    SubElement(objTag, 'truncated').text = '0'
    SubElement(objTag, 'difficult').text = '0'

    bndboxTag = SubElement(objTag, 'bndbox')
    SubElement(bndboxTag, 'xmin').text = top_x
    SubElement(bndboxTag, 'ymin').text = top_y
    SubElement(bndboxTag, 'xmax').text = bottom_x
    SubElement(bndboxTag, 'ymax').text = bottom_y

    temp_path = os.path.join(target_dir, file_name+'.xml')
    tree = ElementTree(root)
    tree.write(temp_path)
    '''
for x in contants_list:
    file_name, image_width, image_height, top_x, top_y, bottom_x, bottom_y = x
    f = open(os.path.join(target_dir, file_name+'.txt'), 'w')
    f.write('0 %s %s %s %s' % (top_x, top_y, bottom_x, bottom_y))
