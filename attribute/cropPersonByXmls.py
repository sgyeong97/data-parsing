# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 09:42:37 2020

@author: kth

어노테이션(xml for cvat) 1개의 파일을 읽고, 150개의 이미지 경로를 참조하여, 작업폴더에 사람이미지만 크롭해주는 프로그램. 

"""

import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np




#1개만 처리할때 쓰는 변수.
#xml = r"E:\0203__3200images_annotations_backup\xmls\0073_d_20191018_083700.xml"
#images = r"E:\0203__3200images_annotations_backup\images\0073_d_20191018_083700\JPEGImages"
#croped = r"C:\Users\kth\Desktop\croped"


xmlrootpath = r"D:\1026__hackathon_10000_final\hackathon_10000\200630_xmls_for_summer_annotation"
imagesrootpath = r"D:\1026__hackathon_10000_final\hackathon_10000\JPEGImages"
cropedrootpath = r"F:\0630__hackathonAnnotation\croped"


def naming(length, name):
    name = str(name)
    if int(length) == 5:
        if len(name) == 1:
            return "0000"+name
        elif len(name) == 2:
            return "000"+name
        elif len(name) == 3:
            return "00" + name
        elif len(name) == 4:
            return "0" + name
        else:
            return name
    else:
        if len(name) == 1:
            return "00000"+name
        elif len(name) == 2:
            return "0000"+name
        elif len(name) == 3:
            return "000" + name
        elif len(name) == 4:
            return "00" + name
        elif len(name) == 5:
            return "0" + name
        else:
            return name


def cropPersonByXml(xmlpath, imagespath, cropedpath):
    cropCount = 0
    if not os.path.isdir(cropedpath):
        print("디렉토리 생성")
        os.mkdir(cropedpath)
    
  
    
    xmllist = os.listdir(xmlpath)
    for xml in xmllist:
        tree = ET.parse(os.path.join(xmlpath,xml))
        note = tree.getroot()
        
        
        for obj in note.findall("object"):
            name = obj.find("name").text
            bndbox = obj.find('bndbox')
            xmin = int(float(bndbox.find('xmin').text))
            ymin = int(float(bndbox.find('ymin').text))
            xmax = int(float(bndbox.find('xmax').text))
            ymax = int(float(bndbox.find('ymax').text))
            
            
            xlen = abs(xmin-xmax)
            ylen = abs(ymin-ymax)
            
            
            if name == "person" and xlen > 25 and ylen > 25:
                img = cv2.imread(os.path.join(imagespath,xml[:-4]+".jpg"), cv2.IMREAD_COLOR)
                src = img.copy()
                croped = src[ymin:ymax, xmin:xmax]
                cropCount += 1
                cv2.imwrite(os.path.join(cropedpath,xml[:-4]+"_"+naming(6,cropCount))+".jpg", croped)

    return


cropPersonByXml(xmlrootpath, imagesrootpath, cropedrootpath)







