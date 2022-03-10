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




#1개만 처리s_annotation할때 쓰는 변수.
#cvatxml = r"E:\0203__3200images_annotations_backup\cvatxmls\0073_d_20191018_083700.xml"
#images = r"E:\0203__3200images_backup\images\0073_d_20191018_083700\JPEGImages"
#croped = r"C:\Users\kth\Desktop\croped"


cvatxmlrootpath = r"F:\0622__summerAnnotation\UniTrain16\cvatxmls"
#cvatxmlrootpath = r"E:\0203__3200images_annotations_backup\test"
imagesrootpath = r"F:\0605__summerVideos\total_sampled"
cropedrootpath = r"F:\0622__summerAnnotation\UniTrain16\croped"


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
        
    
    

def cropPersonByXmlForCvat(cvatxmlpath, imagespath, cropedpath):
    cropCount = 0
    if not os.path.isfile(cvatxmlpath):
        print("xml없음.")
        return
    if not os.path.isdir(cropedpath):
        print("디렉토리 생성")
        os.mkdir(cropedpath)
    tree = ET.parse(cvatxmlpath)
    note = tree.getroot()
    for image in note.findall("image"):
        name = image.get("name")
        for box in image.findall("box"):
            label = box.get("label")
            attribute = box.find("attribute").text
            xtl = int(float(box.get("xtl")))  ##일단 10base로 만드려고 float캐스팅 한번 넣어준거.
            ytl = int(float(box.get("ytl")))
            xbr = int(float(box.get("xbr")))
            ybr = int(float(box.get("ybr")))
            
            xlen = abs(xtl-xbr)
            ylen = abs(ytl-ybr)
            
#            if label == "person" and attribute == "pure":
            if label == "person" and attribute == "pure" and  xlen > 25 and ylen > 25 : 
                img = cv2.imread(os.path.join(imagespath,name), cv2.IMREAD_COLOR)
                print(os.path.join(imagespath,name))
                src = img.copy()
                croped = src[ytl:ybr, xtl:xbr]
                cropCount += 1
                if not os.path.isdir(os.path.join(cropedpath,name[:-9])):
                    os.mkdir(os.path.join(cropedpath,name[:-9]))
                cv2.imwrite(os.path.join(cropedpath,name[:-9],name[:-9]+"_"+naming(6,cropCount))+".jpg", croped)
    print(name[:-9] + " : "+str(cropCount) + " crop")
    return

def cropPersonByXmlsDirectory(cvatxmlrootpath, imagesrootpath, cropedrootpath):
    cvatxmlpathlist = []
    for (path, dir, files) in os.walk(cvatxmlrootpath):
        for filename in files:
            if filename.endswith(".xml"):
                cvatxmlpathlist.append(os.path.join(path,filename))
    cvatxmlpathlist.sort()
    for file in cvatxmlpathlist:
        #cropPersonByXmlForCvat(file, os.path.join(imagesrootpath, file.split("\\")[-1].strip()[:-4], "JPEGImages"), cropedrootpath )
        cropPersonByXmlForCvat(file, os.path.join(imagesrootpath, file.split("\\")[-1].strip()[:-4]), cropedrootpath )
cropPersonByXmlsDirectory(cvatxmlrootpath, imagesrootpath, cropedrootpath)