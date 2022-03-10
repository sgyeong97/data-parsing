# -*- coding: utf-8 -*-
"""
v1.0
pureExtractorV1.3을 바탕으로 만듬.
일단 임시코드이며, 머리만 체크함. 추후 확장 예정임.

v1.1 0511
모든 어트리뷰트로 확장함.
숄더백, 백팩 수정해야함.(cvat 라벨에서 수정하고 코드에서도 수정할것_수정완료)

v2 0525
모든 어트리뷰트 카운트 기능 추가.

v2.1 0525 만드는중
모든 어트리뷰트 카운트 기능을 이용하여 train/test 분리 기능 만들기.

v1.1 0629 (모르고 1.1코드에 만들었고, 여기로 다시 옮김.)
가방이 두개 있는 경우 버림.

v3.0 0703 
조건에 맞게 train/test 로 재생성.
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2
import random
import shutil
import numpy
import time

MAX = 100
CLASS = "head"
## common or head or lower or upper
ONLY_VIEW_DOCUMENTS = True


cvatxmlRootpath = r"D:\신지영_업무\0709__어트리뷰트인수인계\test\attributeTest"
##newImageRootpath = r"E:\0428__Attribute\0626__uniAttribute3\0708__Test_Train_min\head기준"





newImageRootpath = os.path.join(cvatxmlRootpath, "..", CLASS+"_Dataset")
os.makedirs(newImageRootpath,exist_ok=True)

## 이미지 원본 있는 패스.
imageRootpath = r"F:\Annotation_tasks"






def readBoodreturnInt(Bool):
    if Bool == "false":
        return 0
    else:
        return 1
    
    
def getImagePath(file):
    file= file.strip()
    for (path, dir, files) in os.walk(imageRootpath):
        for filename in files:
            filename = filename.strip()
            if filename == file:
                return os.path.abspath(os.path.join(path, filename))


def naming(name):
    name = str(name)
    if len(name) == 1:
        return "000000"+name
    elif len(name) == 2:
        return "00000"+name
    elif len(name) == 3:
        return "0000" + name
    elif len(name) == 4:
        return "000" + name
    elif len(name) == 5:
        return "00" + name
    elif len(name) == 6:
        return "0" + name
    else:
        return name
    

    
image_list = []
    
all_bbox_list = []
head_bbox_list = []
upper_bbox_list = []
lower_bbox_list = []

all_anno_list = []
head_anno_list = []
upper_anno_list = []
lower_anno_list = []


cwd = os.getcwd()



def readCvatxml():
    head_hair_short = 0
    head_hair_long = 0
    head_hair_bald = 0
    head_hair_unknown = 0
    
    head_hat_red = 0
    head_hat_yellow = 0
    head_hat_green = 0
    head_hat_blue = 0
    head_hat_brown = 0
    head_hat_pink = 0
    head_hat_grey = 0
    head_hat_black = 0
    head_hat_white = 0
    head_hat_color_unknown = 0
    
    head_hat_hatless = 0
    head_hat_cap = 0
    head_hat_brimmed = 0
    head_hat_brimless = 0
    head_hat_helmat= 0
    head_hat_hood = 0
    head_hat_unknown = 0
    
    
    all_gender_male = 0
    all_gender_female = 0
    all_gender_unknown = 0
    
    all_age_infant = 0
    all_age_child = 0
    all_age_teenager = 0
    all_age_adult = 0
    all_age_oldperson = 0
    
    all_bag_red = 0
    all_bag_yellow = 0
    all_bag_green = 0
    all_bag_blue = 0
    all_bag_brown = 0
    all_bag_pink = 0
    all_bag_grey = 0
    all_bag_black = 0
    all_bag_white = 0
    all_bag_color_unknown = 0
    
    all_unknown_bag = 0
    all_plasticbag = 0
    all_shoulderbag = 0
    all_handbag = 0
    all_backpack = 0
    all_bagless = 0
    
    upper_top_long_sleeve = 0
    upper_top_short_sleeve = 0
    upper_top_unknown_sleeve = 0
    
    upper_top_red = 0
    upper_top_yellow = 0
    upper_top_green = 0
    upper_top_blue = 0
    upper_top_brown = 0
    upper_top_pink = 0
    upper_top_grey = 0
    upper_top_black = 0
    upper_top_white = 0
    upper_top_color_unknown = 0
    
    
    lower_bottom_long_pants = 0
    lower_bottom_short_pants = 0
    lower_bottom_long_skirt = 0
    lower_bottom_short_skirt = 0
    lower_bottom_unknown_bottom = 0
    
    lower_shoes_red = 0
    lower_shoes_yellow = 0
    lower_shoes_green = 0
    lower_shoes_blue = 0
    lower_shoes_brown = 0
    lower_shoes_pink = 0
    lower_shoes_grey = 0
    lower_shoes_black = 0
    lower_shoes_white = 0
    lower_shoes_color_unknown = 0
    
    
    lower_bottom_red = 0
    lower_bottom_yellow = 0
    lower_bottom_green = 0
    lower_bottom_blue = 0
    lower_bottom_brown = 0
    lower_bottom_pink = 0
    lower_bottom_grey = 0
    lower_bottom_black = 0
    lower_bottom_white = 0
    lower_bottom_color_unknown = 0
    
    
    startFrameNumber = 0
    totalClassDict = makeClassDict()
    
    
    cvatxmllist = os.listdir(cvatxmlRootpath)


    
    for index, cvatxml in enumerate(cvatxmllist):
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            
            
            
            for image in note.findall("image"):
                imageName= image.get("name")
                
                ## 기본적으로 한개도 안쳐져있는 경우 cvatxmls에 기록이 안됨.
                
                
                ### 가방이 두개 있는 경우 버림.
                MOREBAG = False
                bagdk = 0
                backpack = 0
                totebag = 0
                shoulderbag = 0
                plasticbag = 0
                for box in image.findall("box"):
                    label = box.get("label")
                    if label == "all":
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "unknown_bag":
                                unknown_bag = attribute.text
                                unknown_bag = readBoodreturnInt(unknown_bag)
                                bagdk = unknown_bag
                            elif attribute.get("name") == "plasticbag":
                                plasticbag = attribute.text
                                plasticbag = readBoodreturnInt(plasticbag)
                            elif attribute.get("name") == "shoulderbag":
                                shoulderbag = attribute.text
                                shoulderbag = readBoodreturnInt(shoulderbag)
                            elif attribute.get("name") == "handbag":
                                handbag = attribute.text
                                handbag = readBoodreturnInt(handbag)
                                totebag = handbag
                            elif attribute.get("name") == "backpack":
                                backpack = attribute.text
                                backpack = readBoodreturnInt(backpack)
                            if plasticbag + shoulderbag + totebag + backpack + bagdk >= 2 :
                                MOREBAG = True
                if MOREBAG == True:
                    continue
                #---------------------
                
                
                
                ### 라벨 개수 4개 아니면 버림.
                if not (len(image.findall("box")) == 4):
                    continue
                #--------------------
            
            
                ### 4개여도 같은 박스중첩이 있을 경우 버림. 
                labelList = []
                for box in image.findall("box"):
                    labelList.append(box.get("label"))
                if not (len(set(labelList)) == 4):
                    continue
                #-------------------
                
                image_list.append(getImagePath(imageName))
    
                for box in image.findall("box"):
                    label = box.get("label")
                    if label == "head":
                        if not ONLY_VIEW_DOCUMENTS:
                            xtl = int(float(box.get("xtl")))
                            ytl = int(float(box.get("ytl")))
                            xbr = int(float(box.get("xbr")))
                            ybr = int(float(box.get("ybr")))
                            bbox = (xtl, ytl, xbr, ybr)
                            head_bbox_list.append(bbox)
                        
                        for attribute in box.findall("attribute"):
                                
                            if attribute.get("name") == "hair":
                                hair = attribute.text
                                if hair == "short":
                                    short, long, bald, hairdk = 1,0,0,0
                                    head_hair_short += 1
                                    
                                elif hair == "long":
                                    short, long, bald, hairdk = 0,1,0,0
                                    head_hair_long  += 1
                                    
                                elif hair == "bald":
                                    short, long, bald, hairdk = 0,0,1,0
                                    head_hair_bald += 1
                                    
                                elif hair == "unknown":
                                    short, long, bald, hairdk = 0,0,0,1
                                    head_hair_unknown += 1
                               
                                
                                
                                
                            elif attribute.get("name") == "hat_red":
                                hat_red = attribute.text
                                hat_red = readBoodreturnInt(hat_red)
                                head_hat_red += hat_red
                                
                                
                            elif attribute.get("name") == "hat_yellow":
                                hat_yellow = attribute.text
                                hat_yellow = readBoodreturnInt(hat_yellow)
                                head_hat_yellow += hat_yellow
                                
                            elif attribute.get("name") == "hat_green":
                                hat_green = attribute.text
                                hat_green = readBoodreturnInt(hat_green)
                                head_hat_green += hat_green
                                
                                
                            elif attribute.get("name") == "hat_blue":
                                hat_blue = attribute.text
                                hat_blue = readBoodreturnInt(hat_blue)
                                head_hat_blue += hat_blue
                                
                                
                                
                            elif attribute.get("name") == "hat_brown":
                                hat_brown = attribute.text
                                hat_brown = readBoodreturnInt(hat_brown)
                                head_hat_brown += hat_brown
                                
                                
                            elif attribute.get("name") == "hat_pink":
                                hat_pink = attribute.text
                                hat_pink = readBoodreturnInt(hat_pink)
                                head_hat_pink += hat_pink
                                
                                
                            elif attribute.get("name") == "hat_grey":
                                hat_grey = attribute.text
                                hat_grey = readBoodreturnInt(hat_grey)
                                head_hat_grey += hat_grey
                                
                                
                            elif attribute.get("name") == "hat_black":
                                hat_black = attribute.text
                                hat_black = readBoodreturnInt(hat_black)
                                head_hat_black += hat_black
                                
                                
                            elif attribute.get("name") == "hat_white":
                                hat_white = attribute.text
                                hat_white = readBoodreturnInt(hat_white)
                                head_hat_white += hat_white
                                
                                
                            elif attribute.get("name") == "hat_color_unknown":
                                hat_color_unknown = attribute.text
                                hat_color_unknown = readBoodreturnInt(hat_color_unknown)
                                head_hat_color_unknown += hat_color_unknown
    
                                    
                            
                            elif attribute.get("name") == "hat":
                                hat = attribute.text
                                if hat == "hatless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,1,0
                                    head_hat_hatless += 1
                                    
                                    
                                    #어노테이터 실수 제거 코드.
                                    hat_red, hat_yellow, hat_green, hat_blue, hat_brown, hat_pink, hat_grey, hat_black, hat_white, hat_color_unknown = 0,0,0,0,0, 0,0,0,0,0
                                    
                                    
                                elif hat == "cap":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 1,0,0,0,0,0,0
                                    head_hat_cap += 1
                                    
                                    
                                elif hat == "brimmed":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,1,0,0,0,0,0
                                    head_hat_brimmed += 1
                                    
                                    
                                elif hat == "brimless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,1,0,0,0,0
                                    head_hat_brimless += 1
                                    
                                elif hat == "helmat":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,1,0,0,0
                                    head_hat_helmat += 1
                                    
                                elif hat == "hood":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,1,0,0
                                    head_hat_hood += 1
                                    
                                elif hat == "unknown":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,0,1
                                    head_hat_unknown += 1
                            
                        
                        
                        HEAD_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(cap, visor, novisor, helmat, hood, nohat, hatdk,hat_red,hat_yellow,hat_green,hat_blue,hat_brown,hat_pink,hat_grey,hat_black,hat_white,hat_color_unknown, short, long, bald, hairdk)
                        #classesHEad =                                                 ['cap','visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrown','hatpink','hatgray','hatblack','hatwhite','hatcolordk','shot','long','bald','hairdk']
                        head_anno_list.append(HEAD_classes) 
                        addBinary("head",HEAD_classes,totalClassDict)
                    
                    elif label == "all":
                        if not ONLY_VIEW_DOCUMENTS:
                            xtl = int(float(box.get("xtl")))
                            ytl = int(float(box.get("ytl")))
                            xbr = int(float(box.get("xbr")))
                            ybr = int(float(box.get("ybr")))
                            bbox = (xtl, ytl, xbr, ybr)
                            all_bbox_list.append(bbox)
                        
                        
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "gender":
                                gender = attribute.text
                                if gender == "male":
                                    man, woman, unknown_gender = 1,0,0
                                    all_gender_male += 1
                                    
                                elif gender == "female":
                                    man, woman, unknown_gender = 0,1,0
                                    all_gender_female += 1
                                    
                                else: ##unknown gender
                                    man, woman, unknown_gender = 0,0,1
                                    all_gender_unknown += 1
                                    
                               
                                
                            elif attribute.get("name") == "age":
                                age = attribute.text
                                if age == "20~70":
                                    infant,child,teenager,adult,oldperson = 0,0,0,1,0
                                    all_age_adult += 1
                                    
                                    
                                    
                                elif age == "0~7":
                                    infant,child,teenager,adult,oldperson = 1,0,0,0,0
                                    all_age_infant += 1
                                    
                                elif age == "8~13":
                                    infant,child,teenager,adult,oldperson = 0,1,0,0,0
                                    all_age_child += 1
                                    
                                elif age == "14~19":
                                    infant,child,teenager,adult,oldperson = 0,0,1,0,0
                                    all_age_teenager += 1
                                    
                                else: ## 70~
                                    infant,child,teenager,adult,oldperson = 0,0,0,0,1
                                    all_age_oldperson += 1
                                    
                               
                                
                            elif attribute.get("name") == "bag_color_unknown":
                                bag_color_unknown = attribute.text
                                bag_color_unknown = readBoodreturnInt(bag_color_unknown)
                                all_bag_color_unknown += bag_color_unknown
                                
                                    
                            elif attribute.get("name") == "bag_white":
                                bag_white = attribute.text
                                bag_white = readBoodreturnInt(bag_white)
                                all_bag_white += bag_white
                                
                            
                            elif attribute.get("name") == "bag_black":
                                bag_black = attribute.text
                                bag_black = readBoodreturnInt(bag_black)
                                all_bag_black += bag_black
                                
                                
                            elif attribute.get("name") == "bag_grey":
                                bag_grey = attribute.text
                                bag_grey = readBoodreturnInt(bag_grey)
                                all_bag_grey += bag_grey
                                
                                
                            elif attribute.get("name") == "bag_pink":
                                bag_pink = attribute.text
                                bag_pink = readBoodreturnInt(bag_pink)
                                all_bag_pink += bag_pink
                                
                                
                            elif attribute.get("name") == "bag_brown":
                                bag_brown = attribute.text
                                bag_brown = readBoodreturnInt(bag_brown)
                                all_bag_brown += bag_brown
                                
                                
                            elif attribute.get("name") == "bag_blue":
                                bag_blue = attribute.text
                                bag_blue = readBoodreturnInt(bag_blue)
                                all_bag_blue += bag_blue
                                
                                
                            elif attribute.get("name") == "bag_green":
                                bag_green = attribute.text
                                bag_green = readBoodreturnInt(bag_green)
                                all_bag_green += bag_green
                                
                                
                            elif attribute.get("name") == "bag_yellow":
                                bag_yellow = attribute.text
                                bag_yellow = readBoodreturnInt(bag_yellow)
                                all_bag_yellow += bag_yellow
                                
                                
                            elif attribute.get("name") == "bag_red":
                                bag_red = attribute.text
                                bag_red = readBoodreturnInt(bag_red)
                                all_bag_red += bag_red
                                
                                
                            elif attribute.get("name") == "unknown_bag":
                                unknown_bag = attribute.text
                                unknown_bag = readBoodreturnInt(unknown_bag)
                                bagdk = unknown_bag
                                all_unknown_bag += unknown_bag
                                
                                
                            elif attribute.get("name") == "plasticbag":
                                plasticbag = attribute.text
                                plasticbag = readBoodreturnInt(plasticbag)
                                all_plasticbag += plasticbag
                                
                                
                            elif attribute.get("name") == "shoulderbag":
                                shoulderbag = attribute.text
                                shoulderbag = readBoodreturnInt(shoulderbag)
                                all_shoulderbag += shoulderbag
                                
                            
                            elif attribute.get("name") == "handbag":
                                handbag = attribute.text
                                handbag = readBoodreturnInt(handbag)
                                totebag = handbag
                                all_handbag += handbag
                                
                                
                            elif attribute.get("name") == "backpack":
                                backpack = attribute.text
                                backpack = readBoodreturnInt(backpack)
                                all_backpack += backpack
                                
                                
                            elif attribute.get("name") == "bagless":
                                bagless = attribute.text
                                bagless = readBoodreturnInt(bagless)
                                bagnone = bagless
                                all_bagless += bagless
                            
        
                   
                        ALL_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(man,woman,unknown_gender,infant,child,teenager,adult,oldperson,backpack,totebag,shoulderbag,plasticbag,bagdk,bagnone, bag_red, bag_yellow, bag_green, bag_blue, bag_brown, bag_pink, bag_grey, bag_black, bag_white, bag_color_unknown)
                        #classesCOMmon = ['man','woman','genderdk','infant','child','teenager','adult','oldperson','backpack','totebag','shoulderbag','plasticbag','bagdk','bagnone','begred','begyellow','beggreen','begblue','begbrown','begpink','beggray','begblack','begwhite','begcolordk'] 
                        all_anno_list.append(ALL_classes)
                        addBinary("common",ALL_classes,totalClassDict)
                    
                    elif label == "upper":
                        if not ONLY_VIEW_DOCUMENTS:
                            xtl = int(float(box.get("xtl")))
                            ytl = int(float(box.get("ytl")))
                            xbr = int(float(box.get("xbr")))
                            ybr = int(float(box.get("ybr")))
                            
                            bbox = (xtl, ytl, xbr, ybr)
                            upper_bbox_list.append(bbox)
                        
                        
                        
                        
                        for attribute in box.findall("attribute"):
                            
                            
                            if attribute.get("name") == "top_white":
                                top_white = attribute.text
                                top_white = readBoodreturnInt(top_white)
                                upper_top_white += top_white
                                
                                
                            elif attribute.get("name") == "top_color_unknown":
                                top_color_unknown = attribute.text
                                top_color_unknown = readBoodreturnInt(top_color_unknown)
                                upper_top_color_unknown += top_color_unknown
                                
                            
                            elif attribute.get("name") == "top_black":
                                top_black = attribute.text
                                top_black = readBoodreturnInt(top_black)
                                upper_top_black += top_black
                                
                            
                            elif attribute.get("name") == "top_grey":
                                top_grey = attribute.text
                                top_grey = readBoodreturnInt(top_grey)
                                upper_top_grey += top_grey
                                
                            
                            elif attribute.get("name") == "top_pink":
                                top_pink = attribute.text
                                top_pink = readBoodreturnInt(top_pink)
                                upper_top_pink += top_pink
                            
                            elif attribute.get("name") == "top_brown":
                                top_brown = attribute.text
                                top_brown = readBoodreturnInt(top_brown)
                                upper_top_brown += top_brown
                            
                            elif attribute.get("name") == "top_blue":
                                top_blue = attribute.text
                                top_blue = readBoodreturnInt(top_blue)
                                upper_top_blue += top_blue
                                
                            
                            elif attribute.get("name") == "top_green":
                                top_green = attribute.text
                                top_green = readBoodreturnInt(top_green)
                                upper_top_green += top_green
                                
                            
                            elif attribute.get("name") == "top_yellow":
                                top_yellow = attribute.text
                                top_yellow = readBoodreturnInt(top_yellow)
                                upper_top_yellow += top_yellow
                                
                            
                            elif attribute.get("name") == "top_red":
                                top_red = attribute.text
                                top_red = readBoodreturnInt(top_red)
                                upper_top_red += top_red
                                
                            
                            elif attribute.get("name") == "top":
                                top = attribute.text
                                if top == "long_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 1,0,0
                                    upper_top_long_sleeve += 1
                                    
                                elif top == "short_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,1,0
                                    upper_top_short_sleeve += 1
                                    
                                else: ##unknown sleeve
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,0,1
                                    upper_top_unknown_sleeve += 1
                                    
                                    
                                longshirt = long_sleeve
                                shortshirt = short_sleeve
                                
                                
                        
                        UPPER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(longshirt,shortshirt, unknown_sleeve, top_red,top_yellow,top_green,top_blue,top_brown,top_pink,top_grey,top_black,top_white,top_color_unknown)
                        upper_anno_list.append(UPPER_classes)
                        addBinary("upper",UPPER_classes,totalClassDict)
                        
                    elif label == "lower":
                        if not ONLY_VIEW_DOCUMENTS:
                            xtl = int(float(box.get("xtl")))
                            ytl = int(float(box.get("ytl")))
                            xbr = int(float(box.get("xbr")))
                            ybr = int(float(box.get("ybr")))
                            bbox = (xtl, ytl, xbr, ybr)
                            lower_bbox_list.append(bbox)
                        
                        for attribute in box.findall("attribute"):
                            
                            if attribute.get("name") == "bottom_color_unknown":
                                bottom_color_unknown = attribute.text
                                bottom_color_unknown = readBoodreturnInt(bottom_color_unknown)
                                lower_bottom_color_unknown += bottom_color_unknown
                                
                                
                            elif attribute.get("name") == "bottom_white":
                                bottom_white = attribute.text
                                bottom_white = readBoodreturnInt(bottom_white)
                                lower_bottom_white += bottom_white
                                
                            
                            elif attribute.get("name") == "bottom_black":
                                bottom_black = attribute.text
                                bottom_black = readBoodreturnInt(bottom_black)
                                lower_bottom_black += bottom_black
                                
                            
                            elif attribute.get("name") == "bottom_grey":
                                bottom_grey = attribute.text
                                bottom_grey = readBoodreturnInt(bottom_grey)
                                lower_bottom_grey += bottom_grey
                                
                            
                            elif attribute.get("name") == "bottom_pink":
                                bottom_pink = attribute.text
                                bottom_pink = readBoodreturnInt(bottom_pink)
                                lower_bottom_pink += bottom_pink
                            
                            elif attribute.get("name") == "bottom_brown":
                                bottom_brown = attribute.text
                                bottom_brown = readBoodreturnInt(bottom_brown)
                                lower_bottom_brown += bottom_brown
                                
                            
                            elif attribute.get("name") == "bottom_blue":
                                bottom_blue = attribute.text
                                bottom_blue = readBoodreturnInt(bottom_blue)
                                lower_bottom_blue += bottom_blue
                                
                            
                            elif attribute.get("name") == "bottom_green":
                                bottom_green = attribute.text
                                bottom_green = readBoodreturnInt(bottom_green)
                                lower_bottom_green += bottom_green
                                
                            
                            elif attribute.get("name") == "bottom_yellow":
                                bottom_yellow = attribute.text
                                bottom_yellow = readBoodreturnInt(bottom_yellow)
                                lower_bottom_yellow += bottom_yellow
                                
                            
                            elif attribute.get("name") == "bottom_red":
                                bottom_red = attribute.text
                                bottom_red = readBoodreturnInt(bottom_red)
                                lower_bottom_red += bottom_red
                                
                            
                            elif attribute.get("name") == "bottom":
                                bottom = attribute.text
                                if bottom == "long_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 1,0,0,0,0
                                    lower_bottom_long_pants += 1
                                    
                                elif bottom == "short_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,1,0,0,0
                                    lower_bottom_short_pants += 1
                                    
                                elif bottom == "long_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,1,0,0
                                    lower_bottom_long_skirt += 1
                                    
                                elif bottom == "short_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,1,0
                                    lower_bottom_short_skirt += 1
                                    
                                else: # unknown bottom
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,0,1
                                    lower_bottom_unknown_bottom += 1
                                    
                            elif attribute.get("name") == "shoes_color":
                                shoes_color = attribute.text
                                if shoes_color == "shoes_red":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 1,0,0,0,0,0,0,0,0,0
                                    lower_shoes_red += 1
                                    
                                elif shoes_color == "shoes_yellow":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,1,0,0,0,0,0,0,0,0
                                    lower_shoes_yellow += 1
                                    
                                elif shoes_color == "shoes_green":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,1,0,0,0,0,0,0,0
                                    lower_shoes_green += 1
                                    
                                elif shoes_color == "shoes_blue":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,1,0,0,0,0,0,0
                                    lower_shoes_blue += 1
                                
                                elif shoes_color == "shoes_brown":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,1,0,0,0,0,0
                                    lower_shoes_brown += 1
                                
                                elif shoes_color == "shoes_pink":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,1,0,0,0,0
                                    lower_shoes_pink += 1
                                
                                elif shoes_color == "shoes_grey":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,1,0,0,0
                                    lower_shoes_grey += 1
                                
                                elif shoes_color == "shoes_black":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,1,0,0
                                    lower_shoes_black += 1
                                
                                elif shoes_color == "shoes_white":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,1,0
                                    lower_shoes_white += 1
                                
                                else: #shoes_color_unknown
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,0,1
                                    lower_shoes_color_unknown += 1

                        
                        LOWER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(long_pants, short_pants, long_skirt, short_skirt, unknown_bottom, bottom_red, bottom_yellow, bottom_green, bottom_blue, bottom_brown, bottom_pink, bottom_grey, bottom_black, bottom_white, bottom_color_unknown,shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown)
                        lower_anno_list.append(LOWER_classes)
                        addBinary("lower",LOWER_classes,totalClassDict)
                    else:
                        continue
                        #이상한 라벨 들어온경우인데 절대 없다고 봐도됨.
                startFrameNumber += 1
                
            print('{}%완료\r'.format(int(index/len(cvatxmllist)*100)), end='')
            #print("{}% 완료")
                
    f = open(os.path.join(newImageRootpath,"..","total_statistics.txt"), "w")
    f.write("Total Image 장수: {}\n".format(startFrameNumber))
    f.write("head_hair_short: {}\n".format(head_hair_short))
    f.write("head_hair_long: {}\n".format(head_hair_long))
    f.write("head_hair_bald: {}\n".format(head_hair_bald))
    f.write("head_hair_unknown: {}\n".format(head_hair_unknown))
    f.write("head_hat_red: {}\n".format(head_hat_red))
    f.write("head_hat_yellow: {}\n".format(head_hat_yellow))
    f.write("head_hat_green: {}\n".format(head_hat_green))
    f.write("head_hat_blue: {}\n".format(head_hat_blue))
    f.write("head_hat_brown: {}\n".format(head_hat_brown))
    f.write("head_hat_pink: {}\n".format(head_hat_pink))
    f.write("head_hat_grey: {}\n".format(head_hat_grey))
    f.write("head_hat_black: {}\n".format(head_hat_black))
    f.write("head_hat_white: {}\n".format(head_hat_white))
    f.write("head_hat_color_unknown: {}\n".format(head_hat_color_unknown))
    f.write("head_hat_hatless: {}\n".format(head_hat_hatless))
    f.write("head_hat_cap: {}\n".format(head_hat_cap))
    f.write("head_hat_brimmed: {}\n".format(head_hat_brimmed))
    f.write("head_hat_brimless: {}\n".format(head_hat_brimless))
    f.write("head_hat_helmat: {}\n".format(head_hat_helmat))
    f.write("head_hat_hood: {}\n".format(head_hat_hood))
    f.write("head_hat_unknown: {}\n".format(head_hat_unknown))
    f.write("all_gender_male: {}\n".format(all_gender_male))
    f.write("all_gender_female: {}\n".format(all_gender_female))
    f.write("all_gender_unknown: {}\n".format(all_gender_unknown))
    f.write("all_age_infant: {}\n".format(all_age_infant))
    f.write("all_age_child: {}\n".format(all_age_child))
    f.write("all_age_teenager: {}\n".format(all_age_teenager))
    f.write("all_age_adult: {}\n".format(all_age_adult))
    f.write("all_age_oldperson: {}\n".format(all_age_oldperson))
    f.write("all_bag_red: {}\n".format(all_bag_red))
    f.write("all_bag_yellow: {}\n".format(all_bag_yellow))
    f.write("all_bag_green: {}\n".format(all_bag_green))
    f.write("all_bag_blue: {}\n".format(all_bag_blue))
    f.write("all_bag_brown: {}\n".format(all_bag_brown))
    f.write("all_bag_pink: {}\n".format(all_bag_pink))
    f.write("all_bag_grey: {}\n".format(all_bag_grey))
    f.write("all_bag_black: {}\n".format(all_bag_black))
    f.write("all_bag_white: {}\n".format(all_bag_white))
    f.write("all_bag_color_unknown: {}\n".format(all_bag_color_unknown))
    f.write("all_unknown_bag: {}\n".format(all_unknown_bag))
    f.write("all_plasticbag: {}\n".format(all_plasticbag))
    f.write("all_shoulderbag: {}\n".format(all_shoulderbag))
    f.write("all_handbag: {}\n".format(all_handbag))
    f.write("all_backpack: {}\n".format(all_backpack))
    f.write("all_bagless: {}\n".format(all_bagless))
    f.write("upper_top_long_sleeve: {}\n".format(upper_top_long_sleeve))
    f.write("upper_top_short_sleeve: {}\n".format(upper_top_short_sleeve))
    f.write("upper_top_unknown_sleeve: {}\n".format(upper_top_unknown_sleeve))
    f.write("upper_top_red: {}\n".format(upper_top_red))
    f.write("upper_top_yellow: {}\n".format(upper_top_yellow))
    f.write("upper_top_green: {}\n".format(upper_top_green))
    f.write("upper_top_blue: {}\n".format(upper_top_blue))
    f.write("upper_top_brown: {}\n".format(upper_top_brown))
    f.write("upper_top_pink: {}\n".format(upper_top_pink))
    f.write("upper_top_grey: {}\n".format(upper_top_grey))
    f.write("upper_top_black: {}\n".format(upper_top_black))
    f.write("upper_top_white: {}\n".format(upper_top_white))
    f.write("upper_top_color_unknown: {}\n".format(upper_top_color_unknown))
    f.write("lower_bottom_long_pants: {}\n".format(lower_bottom_long_pants))
    f.write("lower_bottom_short_pants: {}\n".format(lower_bottom_short_pants))
    f.write("lower_bottom_long_skirt: {}\n".format(lower_bottom_long_skirt))
    f.write("lower_bottom_short_skirt: {}\n".format(lower_bottom_short_skirt))
    f.write("lower_bottom_unknown_bottom: {}\n".format(lower_bottom_unknown_bottom))
    f.write("lower_shoes_red: {}\n".format(lower_shoes_red))
    f.write("lower_shoes_yellow: {}\n".format(lower_shoes_yellow))
    f.write("lower_shoes_green: {}\n".format(lower_shoes_green))
    f.write("lower_shoes_blue: {}\n".format(lower_shoes_blue))
    f.write("lower_shoes_brown: {}\n".format(lower_shoes_brown))
    f.write("lower_shoes_pink: {}\n".format(lower_shoes_pink))
    f.write("lower_shoes_grey: {}\n".format(lower_shoes_grey))
    f.write("lower_shoes_black: {}\n".format(lower_shoes_black))
    f.write("lower_shoes_white: {}\n".format(lower_shoes_white))
    f.write("lower_shoes_color_unknown: {}\n".format(lower_shoes_color_unknown))
    f.write("lower_bottom_red: {}\n".format(lower_bottom_red))
    f.write("lower_bottom_yellow: {}\n".format(lower_bottom_yellow))
    f.write("lower_bottom_green: {}\n".format(lower_bottom_green))
    f.write("lower_bottom_blue: {}\n".format(lower_bottom_blue))
    f.write("lower_bottom_brown: {}\n".format(lower_bottom_brown))
    f.write("lower_bottom_pink: {}\n".format(lower_bottom_pink))
    f.write("lower_bottom_grey: {}\n".format(lower_bottom_grey))
    f.write("lower_bottom_black: {}\n".format(lower_bottom_black))
    f.write("lower_bottom_white: {}\n".format(lower_bottom_white))
    f.write("lower_bottom_color_unknown: {}\n".format(lower_bottom_color_unknown))
    f.close()

#    print("Total Image 장수: {}".format(startFrameNumber))
#    print("head_hair_short: {}".format(head_hair_short))
#    print("head_hair_long: {}".format(head_hair_long))
#    print("head_hair_bald: {}".format(head_hair_bald))
#    print("head_hair_unknown: {}".format(head_hair_unknown))
#    print("head_hat_red: {}".format(head_hat_red))
#    print("head_hat_yellow: {}".format(head_hat_yellow))
#    print("head_hat_green: {}".format(head_hat_green))
#    print("head_hat_blue: {}".format(head_hat_blue))
#    print("head_hat_brown: {}".format(head_hat_brown))
#    print("head_hat_pink: {}".format(head_hat_pink))
#    print("head_hat_grey: {}".format(head_hat_grey))
#    print("head_hat_black: {}".format(head_hat_black))
#    print("head_hat_white: {}".format(head_hat_white))
#    print("head_hat_color_unknown: {}".format(head_hat_color_unknown))
#    print("head_hat_hatless: {}".format(head_hat_hatless))
#    print("head_hat_cap: {}".format(head_hat_cap))
#    print("head_hat_brimmed: {}".format(head_hat_brimmed))
#    print("head_hat_brimless: {}".format(head_hat_brimless))
#    print("head_hat_helmat: {}".format(head_hat_helmat))
#    print("head_hat_hood: {}".format(head_hat_hood))
#    print("head_hat_unknown: {}".format(head_hat_unknown))
#    print("all_gender_male: {}".format(all_gender_male))
#    print("all_gender_female: {}".format(all_gender_female))
#    print("all_gender_unknown: {}".format(all_gender_unknown))
#    print("all_age_infant: {}".format(all_age_infant))
#    print("all_age_child: {}".format(all_age_child))
#    print("all_age_teenager: {}".format(all_age_teenager))
#    print("all_age_adult: {}".format(all_age_adult))
#    print("all_age_oldperson: {}".format(all_age_oldperson))
#    print("all_bag_red: {}".format(all_bag_red))
#    print("all_bag_yellow: {}".format(all_bag_yellow))
#    print("all_bag_green: {}".format(all_bag_green))
#    print("all_bag_blue: {}".format(all_bag_blue))
#    print("all_bag_brown: {}".format(all_bag_brown))
#    print("all_bag_pink: {}".format(all_bag_pink))
#    print("all_bag_grey: {}".format(all_bag_grey))
#    print("all_bag_black: {}".format(all_bag_black))
#    print("all_bag_white: {}".format(all_bag_white))
#    print("all_bag_color_unknown: {}".format(all_bag_color_unknown))
#    print("all_unknown_bag: {}".format(all_unknown_bag))
#    print("all_plasticbag: {}".format(all_plasticbag))
#    print("all_shoulderbag: {}".format(all_shoulderbag))
#    print("all_handbag: {}".format(all_handbag))
#    print("all_backpack: {}".format(all_backpack))
#    print("all_bagless: {}".format(all_bagless))
#    print("upper_top_long_sleeve: {}".format(upper_top_long_sleeve))
#    print("upper_top_short_sleeve: {}".format(upper_top_short_sleeve))
#    print("upper_top_unknown_sleeve: {}".format(upper_top_unknown_sleeve))
#    print("upper_top_red: {}".format(upper_top_red))
#    print("upper_top_yellow: {}".format(upper_top_yellow))
#    print("upper_top_green: {}".format(upper_top_green))
#    print("upper_top_blue: {}".format(upper_top_blue))
#    print("upper_top_brown: {}".format(upper_top_brown))
#    print("upper_top_pink: {}".format(upper_top_pink))
#    print("upper_top_grey: {}".format(upper_top_grey))
#    print("upper_top_black: {}".format(upper_top_black))
#    print("upper_top_white: {}".format(upper_top_white))
#    print("upper_top_color_unknown: {}".format(upper_top_color_unknown))
#    print("lower_bottom_long_pants: {}".format(lower_bottom_long_pants))
#    print("lower_bottom_short_pants: {}".format(lower_bottom_short_pants))
#    print("lower_bottom_long_skirt: {}".format(lower_bottom_long_skirt))
#    print("lower_bottom_short_skirt: {}".format(lower_bottom_short_skirt))
#    print("lower_bottom_unknown_bottom: {}".format(lower_bottom_unknown_bottom))
#    print("lower_shoes_red: {}".format(lower_shoes_red))
#    print("lower_shoes_yellow: {}".format(lower_shoes_yellow))
#    print("lower_shoes_green: {}".format(lower_shoes_green))
#    print("lower_shoes_blue: {}".format(lower_shoes_blue))
#    print("lower_shoes_brown: {}".format(lower_shoes_brown))
#    print("lower_shoes_pink: {}".format(lower_shoes_pink))
#    print("lower_shoes_grey: {}".format(lower_shoes_grey))
#    print("lower_shoes_black: {}".format(lower_shoes_black))
#    print("lower_shoes_white: {}".format(lower_shoes_white))
#    print("lower_shoes_color_unknown: {}".format(lower_shoes_color_unknown))
#    print("lower_bottom_red: {}".format(lower_bottom_red))
#    print("lower_bottom_yellow: {}".format(lower_bottom_yellow))
#    print("lower_bottom_green: {}".format(lower_bottom_green))
#    print("lower_bottom_blue: {}".format(lower_bottom_blue))
#    print("lower_bottom_brown: {}".format(lower_bottom_brown))
#    print("lower_bottom_pink: {}".format(lower_bottom_pink))
#    print("lower_bottom_grey: {}".format(lower_bottom_grey))
#    print("lower_bottom_black: {}".format(lower_bottom_black))
#    print("lower_bottom_white: {}".format(lower_bottom_white))
#    print("lower_bottom_color_unknown: {}".format(lower_bottom_color_unknown))
    return startFrameNumber, totalClassDict
    

    
def getMin(classname, classdict):
    classTupleList = classdict.items()
    returnClassDict = {}
    returnAttribute = "getMin_Error!"
    for line in classTupleList:   # line[0] 이 key, line[1]이 value
        if line[0].strip().split("_")[0][:3] == classname[:3]:
            returnClassDict[line[0].strip()] = line[1]
    aaa = sorted(returnClassDict.items(), key=lambda x: x[1])
    for i in range(len(aaa)):
        if aaa[i][1] != 0:
            returnAttribute = aaa[i][0]
            break
        
    print(returnAttribute)
    return returnAttribute
    
    
def attributeCheck(min_attribute, annoBinary):
    if min_attribute == "head_hat_cap" and int(annoBinary[0]) == 1:
        return True
    elif min_attribute == "head_hat_brimmed" and int(annoBinary[1]) == 1:
        return True
    elif min_attribute == "head_hat_brimless" and int(annoBinary[2]) == 1:
        return True
    elif min_attribute == "head_hat_helmat" and int(annoBinary[3]) == 1:
    	return True
    elif min_attribute == "head_hat_hood" and int(annoBinary[4]) == 1:
    	return True
    elif min_attribute == "head_hat_hatless" and int(annoBinary[5]) == 1:
    	return True
    elif min_attribute == "head_hat_unknown" and int(annoBinary[6]) == 1:
    	return True
    elif min_attribute == "head_hat_red" and int(annoBinary[7]) == 1:
    	return True
    elif min_attribute == "head_hat_yellow" and int(annoBinary[8]) == 1:
    	return True
    elif min_attribute == "head_hat_green" and int(annoBinary[9]) == 1:
    	return True
    elif min_attribute == "head_hat_blue" and int(annoBinary[10]) == 1:
    	return True
    elif min_attribute == "head_hat_brown" and int(annoBinary[11]) == 1:
    	return True
    elif min_attribute == "head_hat_pink" and int(annoBinary[12]) == 1:
    	return True
    elif min_attribute == "head_hat_grey" and int(annoBinary[13]) == 1:
    	return True
    elif min_attribute == "head_hat_black" and int(annoBinary[14]) == 1:
    	return True
    elif min_attribute == "head_hat_white" and int(annoBinary[15]) == 1:
    	return True
    elif min_attribute == "head_hat_color_unknown" and int(annoBinary[16]) == 1:
    	return True
    elif min_attribute == "head_hair_short" and int(annoBinary[17]) == 1:
    	return True
    elif min_attribute == "head_hair_long" and int(annoBinary[18]) == 1:
    	return True
    elif min_attribute == "head_hair_bald" and int(annoBinary[19]) == 1:
    	return True
    elif min_attribute == "head_hair_unknown" and int(annoBinary[20]) == 1:
    	return True
    elif min_attribute == "upper_top_long_sleeve" and int(annoBinary[0]) == 1:
    	return True
    elif min_attribute == "upper_top_short_sleeve" and int(annoBinary[1]) == 1:
    	return True
    elif min_attribute == "upper_top_unknown_sleeve" and int(annoBinary[2]) == 1:
    	return True
    elif min_attribute == "upper_top_red" and int(annoBinary[3]) == 1:
    	return True
    elif min_attribute == "upper_top_yellow" and int(annoBinary[4]) == 1:
    	return True
    elif min_attribute == "upper_top_green" and int(annoBinary[5]) == 1:
    	return True
    elif min_attribute == "upper_top_blue" and int(annoBinary[6]) == 1:
    	return True
    elif min_attribute == "upper_top_brown" and int(annoBinary[7]) == 1:
    	return True
    elif min_attribute == "upper_top_pink" and int(annoBinary[8]) == 1:
    	return True
    elif min_attribute == "upper_top_grey" and int(annoBinary[9]) == 1:
    	return True
    elif min_attribute == "upper_top_black" and int(annoBinary[10]) == 1:
    	return True
    elif min_attribute == "upper_top_white" and int(annoBinary[11]) == 1:
    	return True
    elif min_attribute == "upper_top_color_unknown" and int(annoBinary[12]) == 1:
    	return True
    elif min_attribute == "lower_bottom_long_pants" and int(annoBinary[0]) == 1:
    	return True
    elif min_attribute == "lower_bottom_short_pants" and int(annoBinary[1]) == 1:
    	return True
    elif min_attribute == "lower_bottom_long_skirt" and int(annoBinary[2]) == 1:
    	return True
    elif min_attribute == "lower_bottom_short_skirt" and int(annoBinary[3]) == 1:
    	return True
    elif min_attribute == "lower_bottom_unknown_bottom" and int(annoBinary[4]) == 1:
    	return True
    elif min_attribute == "lower_bottom_red" and int(annoBinary[5]) == 1:
    	return True
    elif min_attribute == "lower_bottom_yellow" and int(annoBinary[6]) == 1:
    	return True
    elif min_attribute == "lower_bottom_green" and int(annoBinary[7]) == 1:
    	return True
    elif min_attribute == "lower_bottom_blue" and int(annoBinary[8]) == 1:
    	return True
    elif min_attribute == "lower_bottom_brown" and int(annoBinary[9]) == 1:
    	return True
    elif min_attribute == "lower_bottom_pink" and int(annoBinary[10]) == 1:
    	return True
    elif min_attribute == "lower_bottom_grey" and int(annoBinary[11]) == 1:
    	return True
    elif min_attribute == "lower_bottom_black" and int(annoBinary[12]) == 1:
    	return True
    elif min_attribute == "lower_bottom_white" and int(annoBinary[13]) == 1:
    	return True
    elif min_attribute == "lower_bottom_color_unknown" and int(annoBinary[14]) == 1:
    	return True
    elif min_attribute == "lower_shoes_red" and int(annoBinary[15]) == 1:
    	return True
    elif min_attribute == "lower_shoes_yellow" and int(annoBinary[16]) == 1:
    	return True
    elif min_attribute == "lower_shoes_green" and int(annoBinary[17]) == 1:
    	return True
    elif min_attribute == "lower_shoes_blue" and int(annoBinary[18]) == 1:
    	return True
    elif min_attribute == "lower_shoes_brown" and int(annoBinary[19]) == 1:
    	return True
    elif min_attribute == "lower_shoes_pink" and int(annoBinary[20]) == 1:
    	return True
    elif min_attribute == "lower_shoes_grey" and int(annoBinary[21]) == 1:
    	return True
    elif min_attribute == "lower_shoes_black" and int(annoBinary[22]) == 1:
    	return True
    elif min_attribute == "lower_shoes_white" and int(annoBinary[23]) == 1:
    	return True
    elif min_attribute == "lower_shoes_color_unknown" and int(annoBinary[24]) == 1:
    	return True
    elif min_attribute == "all_gender_male" and int(annoBinary[0]) == 1:
    	return True
    elif min_attribute == "all_gender_female" and int(annoBinary[1]) == 1:
    	return True
    elif min_attribute == "all_gender_unknown" and int(annoBinary[2]) == 1:
    	return True
    elif min_attribute == "all_age_infant" and int(annoBinary[3]) == 1:
    	return True
    elif min_attribute == "all_age_child" and int(annoBinary[4]) == 1:
    	return True
    elif min_attribute == "all_age_teenager" and int(annoBinary[5]) == 1:
    	return True
    elif min_attribute == "all_age_adult" and int(annoBinary[6]) == 1:
    	return True
    elif min_attribute == "all_age_oldperson" and int(annoBinary[7]) == 1:
    	return True
    elif min_attribute == "all_backpack" and int(annoBinary[8]) == 1:
    	return True
    elif min_attribute == "all_handbag" and int(annoBinary[9]) == 1:
    	return True
    elif min_attribute == "all_shoulderbag" and int(annoBinary[10]) == 1:
    	return True
    elif min_attribute == "all_plasticbag" and int(annoBinary[11]) == 1:
    	return True
    elif min_attribute == "all_unknown_bag" and int(annoBinary[12]) == 1:
    	return True
    elif min_attribute == "all_bagless" and int(annoBinary[13]) == 1:
    	return True
    elif min_attribute == "all_bag_red" and int(annoBinary[14]) == 1:
    	return True
    elif min_attribute == "all_bag_yellow" and int(annoBinary[15]) == 1:
    	return True
    elif min_attribute == "all_bag_green" and int(annoBinary[16]) == 1:
    	return True
    elif min_attribute == "all_bag_blue" and int(annoBinary[17]) == 1:
    	return True
    elif min_attribute == "all_bag_brown" and int(annoBinary[18]) == 1:
    	return True
    elif min_attribute == "all_bag_pink" and int(annoBinary[19]) == 1:
    	return True
    elif min_attribute == "all_bag_grey" and int(annoBinary[20]) == 1:
    	return True
    elif min_attribute == "all_bag_black" and int(annoBinary[21]) == 1:
    	return True
    elif min_attribute == "all_bag_white" and int(annoBinary[22]) == 1:
    	return True
    elif min_attribute == "all_bag_color_unknown" and int(annoBinary[23]) == 1:
    	return True
    else:
        return False
    

def subBinary(classname, annoBinary, classDict):
    if classname == "head":
        classDict["head_hat_cap"] -=  int(annoBinary[0])
        classDict["head_hat_brimmed"] -=  int(annoBinary[1])
        classDict["head_hat_brimless"] -=  int(annoBinary[2])
        classDict["head_hat_helmat"] -=  int(annoBinary[3])
        classDict["head_hat_hood"] -=  int(annoBinary[4])
        classDict["head_hat_hatless"] -=  int(annoBinary[5])
        classDict["head_hat_unknown"] -=  int(annoBinary[6])
        classDict["head_hat_red"] -=  int(annoBinary[7])
        classDict["head_hat_yellow"] -=  int(annoBinary[8])
        classDict["head_hat_green"] -=  int(annoBinary[9])
        classDict["head_hat_blue"] -=  int(annoBinary[10])
        classDict["head_hat_brown"] -=  int(annoBinary[11])
        classDict["head_hat_pink"] -=  int(annoBinary[12])
        classDict["head_hat_grey"] -=  int(annoBinary[13])
        classDict["head_hat_black"] -=  int(annoBinary[14])
        classDict["head_hat_white"] -=  int(annoBinary[15])
        classDict["head_hat_color_unknown"] -=  int(annoBinary[16])
        classDict["head_hair_short"] -=  int(annoBinary[17])
        classDict["head_hair_long"] -=  int(annoBinary[18])
        classDict["head_hair_bald"] -=  int(annoBinary[19])
        classDict["head_hair_unknown"] -=  int(annoBinary[20])
    elif classname == "upper":
        classDict["upper_top_long_sleeve"] -=  int(annoBinary[0])
        classDict["upper_top_short_sleeve"] -=  int(annoBinary[1])
        classDict["upper_top_unknown_sleeve"] -=  int(annoBinary[2])
        classDict["upper_top_red"] -=  int(annoBinary[3])
        classDict["upper_top_yellow"] -=  int(annoBinary[4])
        classDict["upper_top_green"] -=  int(annoBinary[5])
        classDict["upper_top_blue"] -=  int(annoBinary[6])
        classDict["upper_top_brown"] -=  int(annoBinary[7])
        classDict["upper_top_pink"] -=  int(annoBinary[8])
        classDict["upper_top_grey"] -=  int(annoBinary[9])
        classDict["upper_top_black"] -=  int(annoBinary[10])
        classDict["upper_top_white"] -=  int(annoBinary[11])
        classDict["upper_top_color_unknown"] -=  int(annoBinary[12])
    elif classname == "lower":
        classDict["lower_bottom_long_pants"] -=  int(annoBinary[0])
        classDict["lower_bottom_short_pants"] -=  int(annoBinary[1])
        classDict["lower_bottom_long_skirt"] -=  int(annoBinary[2])
        classDict["lower_bottom_short_skirt"] -=  int(annoBinary[3])
        classDict["lower_bottom_unknown_bottom"] -=  int(annoBinary[4])
        classDict["lower_bottom_red"] -=  int(annoBinary[5])
        classDict["lower_bottom_yellow"] -=  int(annoBinary[6])
        classDict["lower_bottom_green"] -=  int(annoBinary[7])
        classDict["lower_bottom_blue"] -=  int(annoBinary[8])
        classDict["lower_bottom_brown"] -=  int(annoBinary[9])
        classDict["lower_bottom_pink"] -=  int(annoBinary[10])
        classDict["lower_bottom_grey"] -=  int(annoBinary[11])
        classDict["lower_bottom_black"] -=  int(annoBinary[12])
        classDict["lower_bottom_white"] -=  int(annoBinary[13])
        classDict["lower_bottom_color_unknown"] -=  int(annoBinary[14])
        classDict["lower_shoes_red"] -=  int(annoBinary[15])
        classDict["lower_shoes_yellow"] -=  int(annoBinary[16])
        classDict["lower_shoes_green"] -=  int(annoBinary[17])
        classDict["lower_shoes_blue"] -=  int(annoBinary[18])
        classDict["lower_shoes_brown"] -=  int(annoBinary[19])
        classDict["lower_shoes_pink"] -=  int(annoBinary[20])
        classDict["lower_shoes_grey"] -=  int(annoBinary[21])
        classDict["lower_shoes_black"] -=  int(annoBinary[22])
        classDict["lower_shoes_white"] -=  int(annoBinary[23])
        classDict["lower_shoes_color_unknown"] -=  int(annoBinary[24])
    else:
        classDict["all_gender_male"] -=  int(annoBinary[0])
        classDict["all_gender_female"] -=  int(annoBinary[1])
        classDict["all_gender_unknown"] -=  int(annoBinary[2])
        classDict["all_age_infant"] -=  int(annoBinary[3])
        classDict["all_age_child"] -=  int(annoBinary[4])
        classDict["all_age_teenager"] -=  int(annoBinary[5])
        classDict["all_age_adult"] -=  int(annoBinary[6])
        classDict["all_age_oldperson"] -=  int(annoBinary[7])
        classDict["all_backpack"] -=  int(annoBinary[8])
        classDict["all_handbag"] -=  int(annoBinary[9])
        classDict["all_shoulderbag"] -=  int(annoBinary[10])
        classDict["all_plasticbag"] -=  int(annoBinary[11])
        classDict["all_unknown_bag"] -=  int(annoBinary[12])
        classDict["all_bagless"] -=  int(annoBinary[13])
        classDict["all_bag_red"] -=  int(annoBinary[14])
        classDict["all_bag_yellow"] -=  int(annoBinary[15])
        classDict["all_bag_green"] -=  int(annoBinary[16])
        classDict["all_bag_blue"] -=  int(annoBinary[17])
        classDict["all_bag_brown"] -=  int(annoBinary[18])
        classDict["all_bag_pink"] -=  int(annoBinary[19])
        classDict["all_bag_grey"] -=  int(annoBinary[20])
        classDict["all_bag_black"] -=  int(annoBinary[21])
        classDict["all_bag_white"] -=  int(annoBinary[22]) 
        classDict["all_bag_color_unknown"] -=  int(annoBinary[23])
        

def makeClassDict():
    classDict = {}
    classDict["head_hat_cap"] = 0
    classDict["head_hat_brimmed"] = 0
    classDict["head_hat_brimless"] = 0
    classDict["head_hat_helmat"] = 0
    classDict["head_hat_hood"] = 0
    classDict["head_hat_hatless"] = 0
    classDict["head_hat_unknown"] = 0
    classDict["head_hat_red"] = 0
    classDict["head_hat_yellow"] = 0
    classDict["head_hat_green"] = 0
    classDict["head_hat_blue"] = 0
    classDict["head_hat_brown"] = 0
    classDict["head_hat_pink"] = 0
    classDict["head_hat_grey"] = 0
    classDict["head_hat_black"] = 0
    classDict["head_hat_white"] = 0
    classDict["head_hat_color_unknown"] = 0
    classDict["head_hair_short"] = 0
    classDict["head_hair_long"] = 0
    classDict["head_hair_bald"] = 0
    classDict["head_hair_unknown"] = 0
    classDict["upper_top_long_sleeve"] = 0
    classDict["upper_top_short_sleeve"] = 0
    classDict["upper_top_unknown_sleeve"] = 0
    classDict["upper_top_red"] = 0
    classDict["upper_top_yellow"] = 0
    classDict["upper_top_green"] = 0
    classDict["upper_top_blue"] = 0
    classDict["upper_top_brown"] = 0
    classDict["upper_top_pink"] = 0
    classDict["upper_top_grey"] = 0
    classDict["upper_top_black"] = 0
    classDict["upper_top_white"] = 0
    classDict["upper_top_color_unknown"] = 0
    classDict["lower_bottom_long_pants"] = 0
    classDict["lower_bottom_short_pants"] = 0
    classDict["lower_bottom_long_skirt"] = 0
    classDict["lower_bottom_short_skirt"] = 0
    classDict["lower_bottom_unknown_bottom"] = 0
    classDict["lower_bottom_red"] = 0
    classDict["lower_bottom_yellow"] = 0
    classDict["lower_bottom_green"] = 0
    classDict["lower_bottom_blue"] = 0
    classDict["lower_bottom_brown"] = 0
    classDict["lower_bottom_pink"] = 0
    classDict["lower_bottom_grey"] = 0
    classDict["lower_bottom_black"] = 0
    classDict["lower_bottom_white"] = 0
    classDict["lower_bottom_color_unknown"] = 0
    classDict["lower_shoes_red"] = 0
    classDict["lower_shoes_yellow"] = 0
    classDict["lower_shoes_green"] = 0
    classDict["lower_shoes_blue"] = 0
    classDict["lower_shoes_brown"] = 0
    classDict["lower_shoes_pink"] = 0
    classDict["lower_shoes_grey"] = 0
    classDict["lower_shoes_black"] = 0
    classDict["lower_shoes_white"] = 0
    classDict["lower_shoes_color_unknown"] = 0
    classDict["all_gender_male"] = 0
    classDict["all_gender_female"] = 0
    classDict["all_gender_unknown"] = 0
    classDict["all_age_infant"] = 0
    classDict["all_age_child"] = 0
    classDict["all_age_teenager"] = 0
    classDict["all_age_adult"] = 0
    classDict["all_age_oldperson"] = 0
    classDict["all_backpack"] = 0
    classDict["all_handbag"] = 0
    classDict["all_shoulderbag"] = 0
    classDict["all_plasticbag"] = 0
    classDict["all_unknown_bag"] = 0
    classDict["all_bagless"] = 0
    classDict["all_bag_red"] = 0
    classDict["all_bag_yellow"] = 0
    classDict["all_bag_green"] = 0
    classDict["all_bag_blue"] = 0
    classDict["all_bag_brown"] = 0
    classDict["all_bag_pink"] = 0
    classDict["all_bag_grey"] = 0
    classDict["all_bag_black"] = 0
    classDict["all_bag_white"] = 0
    classDict["all_bag_color_unknown"] = 0
    return classDict
    
def addBinary(classname, annoBinary, classDict): 
    if classname == "head":
        classDict["head_hat_cap"] +=  int(annoBinary[0])
        classDict["head_hat_brimmed"] +=  int(annoBinary[1])
        classDict["head_hat_brimless"] +=  int(annoBinary[2])
        classDict["head_hat_helmat"] +=  int(annoBinary[3])
        classDict["head_hat_hood"] +=  int(annoBinary[4])
        classDict["head_hat_hatless"] +=  int(annoBinary[5])
        classDict["head_hat_unknown"] +=  int(annoBinary[6])
        classDict["head_hat_red"] +=  int(annoBinary[7])
        classDict["head_hat_yellow"] +=  int(annoBinary[8])
        classDict["head_hat_green"] +=  int(annoBinary[9])
        classDict["head_hat_blue"] +=  int(annoBinary[10])
        classDict["head_hat_brown"] +=  int(annoBinary[11])
        classDict["head_hat_pink"] +=  int(annoBinary[12])
        classDict["head_hat_grey"] +=  int(annoBinary[13])
        classDict["head_hat_black"] +=  int(annoBinary[14])
        classDict["head_hat_white"] +=  int(annoBinary[15])
        classDict["head_hat_color_unknown"] +=  int(annoBinary[16])
        classDict["head_hair_short"] +=  int(annoBinary[17])
        classDict["head_hair_long"] +=  int(annoBinary[18])
        classDict["head_hair_bald"] +=  int(annoBinary[19])
        classDict["head_hair_unknown"] +=  int(annoBinary[20])
    elif classname == "upper":
        classDict["upper_top_long_sleeve"] +=  int(annoBinary[0])
        classDict["upper_top_short_sleeve"] +=  int(annoBinary[1])
        classDict["upper_top_unknown_sleeve"] +=  int(annoBinary[2])
        classDict["upper_top_red"] +=  int(annoBinary[3])
        classDict["upper_top_yellow"] +=  int(annoBinary[4])
        classDict["upper_top_green"] +=  int(annoBinary[5])
        classDict["upper_top_blue"] +=  int(annoBinary[6])
        classDict["upper_top_brown"] +=  int(annoBinary[7])
        classDict["upper_top_pink"] +=  int(annoBinary[8])
        classDict["upper_top_grey"] +=  int(annoBinary[9])
        classDict["upper_top_black"] +=  int(annoBinary[10])
        classDict["upper_top_white"] +=  int(annoBinary[11])
        classDict["upper_top_color_unknown"] +=  int(annoBinary[12])
    elif classname == "lower":
        classDict["lower_bottom_long_pants"] +=  int(annoBinary[0])
        classDict["lower_bottom_short_pants"] +=  int(annoBinary[1])
        classDict["lower_bottom_long_skirt"] +=  int(annoBinary[2])
        classDict["lower_bottom_short_skirt"] +=  int(annoBinary[3])
        classDict["lower_bottom_unknown_bottom"] +=  int(annoBinary[4])
        classDict["lower_bottom_red"] +=  int(annoBinary[5])
        classDict["lower_bottom_yellow"] +=  int(annoBinary[6])
        classDict["lower_bottom_green"] +=  int(annoBinary[7])
        classDict["lower_bottom_blue"] +=  int(annoBinary[8])
        classDict["lower_bottom_brown"] +=  int(annoBinary[9])
        classDict["lower_bottom_pink"] +=  int(annoBinary[10])
        classDict["lower_bottom_grey"] +=  int(annoBinary[11])
        classDict["lower_bottom_black"] +=  int(annoBinary[12])
        classDict["lower_bottom_white"] +=  int(annoBinary[13])
        classDict["lower_bottom_color_unknown"] +=  int(annoBinary[14])
        classDict["lower_shoes_red"] +=  int(annoBinary[15])
        classDict["lower_shoes_yellow"] +=  int(annoBinary[16])
        classDict["lower_shoes_green"] +=  int(annoBinary[17])
        classDict["lower_shoes_blue"] +=  int(annoBinary[18])
        classDict["lower_shoes_brown"] +=  int(annoBinary[19])
        classDict["lower_shoes_pink"] +=  int(annoBinary[20])
        classDict["lower_shoes_grey"] +=  int(annoBinary[21])
        classDict["lower_shoes_black"] +=  int(annoBinary[22])
        classDict["lower_shoes_white"] +=  int(annoBinary[23])
        classDict["lower_shoes_color_unknown"] +=  int(annoBinary[24])
    else:
        classDict["all_gender_male"] +=  int(annoBinary[0])
        classDict["all_gender_female"] +=  int(annoBinary[1])
        classDict["all_gender_unknown"] +=  int(annoBinary[2])
        classDict["all_age_infant"] +=  int(annoBinary[3])
        classDict["all_age_child"] +=  int(annoBinary[4])
        classDict["all_age_teenager"] +=  int(annoBinary[5])
        classDict["all_age_adult"] +=  int(annoBinary[6])
        classDict["all_age_oldperson"] +=  int(annoBinary[7])
        classDict["all_backpack"] +=  int(annoBinary[8])
        classDict["all_handbag"] +=  int(annoBinary[9])
        classDict["all_shoulderbag"] +=  int(annoBinary[10])
        classDict["all_plasticbag"] +=  int(annoBinary[11])
        classDict["all_unknown_bag"] +=  int(annoBinary[12])
        classDict["all_bagless"] +=  int(annoBinary[13])
        classDict["all_bag_red"] +=  int(annoBinary[14])
        classDict["all_bag_yellow"] +=  int(annoBinary[15])
        classDict["all_bag_green"] +=  int(annoBinary[16])
        classDict["all_bag_blue"] +=  int(annoBinary[17])
        classDict["all_bag_brown"] +=  int(annoBinary[18])
        classDict["all_bag_pink"] +=  int(annoBinary[19])
        classDict["all_bag_grey"] +=  int(annoBinary[20])
        classDict["all_bag_black"] +=  int(annoBinary[21])
        classDict["all_bag_white"] +=  int(annoBinary[22]) 
        classDict["all_bag_color_unknown"] +=  int(annoBinary[23])
        
def makeStatisticsFile(_type, classdict):
    f = open(os.path.join(newImageRootpath, ".." , _type+ "_statistics.txt"), "w")
    f.write("head_hair_short: {}\n".format(classdict["head_hair_short"]))
    f.write("head_hair_long: {}\n".format(classdict["head_hair_long"]))
    f.write("head_hair_bald: {}\n".format(classdict["head_hair_bald"]))
    f.write("head_hair_unknown: {}\n".format(classdict["head_hair_unknown"]))
    f.write("head_hat_red: {}\n".format(classdict["head_hat_red"]))
    f.write("head_hat_yellow: {}\n".format(classdict["head_hat_yellow"]))
    f.write("head_hat_green: {}\n".format(classdict["head_hat_green"]))
    f.write("head_hat_blue: {}\n".format(classdict["head_hat_blue"]))
    f.write("head_hat_brown: {}\n".format(classdict["head_hat_brown"]))
    f.write("head_hat_pink: {}\n".format(classdict["head_hat_pink"]))
    f.write("head_hat_grey: {}\n".format(classdict["head_hat_grey"]))
    f.write("head_hat_black: {}\n".format(classdict["head_hat_black"]))
    f.write("head_hat_white: {}\n".format(classdict["head_hat_white"]))
    f.write("head_hat_color_unknown: {}\n".format(classdict["head_hat_color_unknown"]))
    f.write("head_hat_hatless: {}\n".format(classdict["head_hat_hatless"]))
    f.write("head_hat_cap: {}\n".format(classdict["head_hat_cap"]))
    f.write("head_hat_brimmed: {}\n".format(classdict["head_hat_brimmed"]))
    f.write("head_hat_brimless: {}\n".format(classdict["head_hat_brimless"]))
    f.write("head_hat_helmat: {}\n".format(classdict["head_hat_helmat"]))
    f.write("head_hat_hood: {}\n".format(classdict["head_hat_hood"]))
    f.write("head_hat_unknown: {}\n".format(classdict["head_hat_unknown"]))
    f.write("all_gender_male: {}\n".format(classdict["all_gender_male"]))
    f.write("all_gender_female: {}\n".format(classdict["all_gender_female"]))
    f.write("all_gender_unknown: {}\n".format(classdict["all_gender_unknown"]))
    f.write("all_age_infant: {}\n".format(classdict["all_age_infant"]))
    f.write("all_age_child: {}\n".format(classdict["all_age_child"]))
    f.write("all_age_teenager: {}\n".format(classdict["all_age_teenager"]))
    f.write("all_age_adult: {}\n".format(classdict["all_age_adult"]))
    f.write("all_age_oldperson: {}\n".format(classdict["all_age_oldperson"]))
    f.write("all_bag_red: {}\n".format(classdict["all_bag_red"]))
    f.write("all_bag_yellow: {}\n".format(classdict["all_bag_yellow"]))
    f.write("all_bag_green: {}\n".format(classdict["all_bag_green"]))
    f.write("all_bag_blue: {}\n".format(classdict["all_bag_blue"]))
    f.write("all_bag_brown: {}\n".format(classdict["all_bag_brown"]))
    f.write("all_bag_pink: {}\n".format(classdict["all_bag_pink"]))
    f.write("all_bag_grey: {}\n".format(classdict["all_bag_grey"]))
    f.write("all_bag_black: {}\n".format(classdict["all_bag_black"]))
    f.write("all_bag_white: {}\n".format(classdict["all_bag_white"]))
    f.write("all_bag_color_unknown: {}\n".format(classdict["all_bag_color_unknown"]))
    f.write("all_unknown_bag: {}\n".format(classdict["all_unknown_bag"]))
    f.write("all_plasticbag: {}\n".format(classdict["all_plasticbag"]))
    f.write("all_shoulderbag: {}\n".format(classdict["all_shoulderbag"]))
    f.write("all_handbag: {}\n".format(classdict["all_handbag"]))
    f.write("all_backpack: {}\n".format(classdict["all_backpack"]))
    f.write("all_bagless: {}\n".format(classdict["all_bagless"]))
    f.write("upper_top_long_sleeve: {}\n".format(classdict["upper_top_long_sleeve"]))
    f.write("upper_top_short_sleeve: {}\n".format(classdict["upper_top_short_sleeve"]))
    f.write("upper_top_unknown_sleeve: {}\n".format(classdict["upper_top_unknown_sleeve"]))
    f.write("upper_top_red: {}\n".format(classdict["upper_top_red"]))
    f.write("upper_top_yellow: {}\n".format(classdict["upper_top_yellow"]))
    f.write("upper_top_green: {}\n".format(classdict["upper_top_green"]))
    f.write("upper_top_blue: {}\n".format(classdict["upper_top_blue"]))
    f.write("upper_top_brown: {}\n".format(classdict["upper_top_brown"]))
    f.write("upper_top_pink: {}\n".format(classdict["upper_top_pink"]))
    f.write("upper_top_grey: {}\n".format(classdict["upper_top_grey"]))
    f.write("upper_top_black: {}\n".format(classdict["upper_top_black"]))
    f.write("upper_top_white: {}\n".format(classdict["upper_top_white"]))
    f.write("upper_top_color_unknown: {}\n".format(classdict["upper_top_color_unknown"]))
    f.write("lower_bottom_long_pants: {}\n".format(classdict["lower_bottom_long_pants"]))
    f.write("lower_bottom_short_pants: {}\n".format(classdict["lower_bottom_short_pants"]))
    f.write("lower_bottom_long_skirt: {}\n".format(classdict["lower_bottom_long_skirt"]))
    f.write("lower_bottom_short_skirt: {}\n".format(classdict["lower_bottom_short_skirt"]))
    f.write("lower_bottom_unknown_bottom: {}\n".format(classdict["lower_bottom_unknown_bottom"]))
    f.write("lower_shoes_red: {}\n".format(classdict["lower_shoes_red"]))
    f.write("lower_shoes_yellow: {}\n".format(classdict["lower_shoes_yellow"]))
    f.write("lower_shoes_green: {}\n".format(classdict["lower_shoes_green"]))
    f.write("lower_shoes_blue: {}\n".format(classdict["lower_shoes_blue"]))
    f.write("lower_shoes_brown: {}\n".format(classdict["lower_shoes_brown"]))
    f.write("lower_shoes_pink: {}\n".format(classdict["lower_shoes_pink"]))
    f.write("lower_shoes_grey: {}\n".format(classdict["lower_shoes_grey"]))
    f.write("lower_shoes_black: {}\n".format(classdict["lower_shoes_black"]))
    f.write("lower_shoes_white: {}\n".format(classdict["lower_shoes_white"]))
    f.write("lower_shoes_color_unknown: {}\n".format(classdict["lower_shoes_color_unknown"]))
    f.write("lower_bottom_red: {}\n".format(classdict["lower_bottom_red"]))
    f.write("lower_bottom_yellow: {}\n".format(classdict["lower_bottom_yellow"]))
    f.write("lower_bottom_green: {}\n".format(classdict["lower_bottom_green"]))
    f.write("lower_bottom_blue: {}\n".format(classdict["lower_bottom_blue"]))
    f.write("lower_bottom_brown: {}\n".format(classdict["lower_bottom_brown"]))
    f.write("lower_bottom_pink: {}\n".format(classdict["lower_bottom_pink"]))
    f.write("lower_bottom_grey: {}\n".format(classdict["lower_bottom_grey"]))
    f.write("lower_bottom_black: {}\n".format(classdict["lower_bottom_black"]))
    f.write("lower_bottom_white: {}\n".format(classdict["lower_bottom_white"]))
    f.write("lower_bottom_color_unknown: {}\n".format(classdict["lower_bottom_color_unknown"]))
    f.close()
    


def makeDataset(maxCount, classname, classdict):
    testCount = 0

    
    if classname == "common":    
        train_all_imageRootpath = os.path.join(newImageRootpath, "train","common", "common_images")
    elif classname == "head":
        train_head_imageRootpath = os.path.join(newImageRootpath,  "train","head","head_images")
    elif classname == "upper":
        train_upper_imageRootpath = os.path.join(newImageRootpath,  "train","upper","upper_images")
    else:
        train_lower_imageRootpath = os.path.join(newImageRootpath,  "train","lower","lower_images")
    
    
    test_all_imageRootpath = os.path.join(newImageRootpath, "test","common", "common_images")
    test_head_imageRootpath = os.path.join(newImageRootpath,  "test","head","head_images")
    test_upper_imageRootpath = os.path.join(newImageRootpath,  "test","upper","upper_images")
    test_lower_imageRootpath = os.path.join(newImageRootpath,  "test","lower","lower_images")
    
    if classname == "common":   
        os.makedirs(train_all_imageRootpath,exist_ok=True)
        os.makedirs(test_all_imageRootpath,exist_ok=True)
        train_allAttributeFile = open(os.path.join(train_all_imageRootpath, "..", "common_attribute_annotation.txt"), "w")
        test_allAttributeFile = open(os.path.join(test_all_imageRootpath, "..", "common_attribute_annotation.txt"), "w")
    elif classname == "head":
        os.makedirs(train_head_imageRootpath,exist_ok=True)
        os.makedirs(test_head_imageRootpath,exist_ok=True)
        train_headAttributeFile = open(os.path.join(train_head_imageRootpath, "..", "head_attribute_annotation.txt"), "w")
        test_headAttributeFile = open(os.path.join(test_head_imageRootpath, "..", "head_attribute_annotation.txt"), "w")
    elif classname == "upper":
        os.makedirs(train_upper_imageRootpath,exist_ok=True)
        os.makedirs(test_upper_imageRootpath,exist_ok=True)
        train_upperAttributeFile = open(os.path.join(train_upper_imageRootpath, "..", "upper_attribute_annotation.txt"), "w")
        test_upperAttributeFile = open(os.path.join(test_upper_imageRootpath, "..", "upper_attribute_annotation.txt"), "w")
    else:
        os.makedirs(train_lower_imageRootpath,exist_ok=True)
        os.makedirs(test_lower_imageRootpath,exist_ok=True)
        train_lowerAttributeFile = open(os.path.join(train_lower_imageRootpath, "..", "lower_attribute_annotation.txt"), "w")
        test_lowerAttributeFile = open(os.path.join(test_lower_imageRootpath, "..", "lower_attribute_annotation.txt"), "w")


    
    randomIndexList = []
    for i in range(len(image_list)):
        randomIndexList.append(i)
    random.shuffle(randomIndexList)
    
   
    
    
    ## classname에는 head, upper, lower, common or all 들어감.


    ## 가장 작은 것 부터 test셋으로 옮김.
    
    
    testCount = 0
    trainCount = 0
    
    testIndex = []
    
    i = 0
    testClassDict = makeClassDict()
    trainClassDict = makeClassDict()
    while testCount < maxCount:
        
        min_attribute = getMin(classname, classdict)  ## all_bag_color_unknown 이런식으로 리턴됨.
    
        if classname == "head":
            annoBinary = head_anno_list[randomIndexList[i]]
        elif classname == "upper":
            annoBinary = upper_anno_list[randomIndexList[i]]
        elif classname == "lower":
            annoBinary = lower_anno_list[randomIndexList[i]]
        else:
            annoBinary = all_anno_list[randomIndexList[i]]

        if attributeCheck(min_attribute, annoBinary):
            print(min_attribute+"매치됨.")
            testIndex.append(randomIndexList[i])
            subBinary(classname, annoBinary, classdict)
            addBinary(classname, annoBinary, testClassDict)
            ########################################
#            stream = open(os.path.join(image_list[randomIndexList[i]]), "rb")
#            _bytes = bytearray(stream.read())
#            numpyarray = numpy.asarray(_bytes, dtype=numpy.uint8)
#            img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            
            if not ONLY_VIEW_DOCUMENTS:
                shutil.copy(os.path.join(image_list[randomIndexList[i]]), "temp_image.jpg")
                img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
                
                src = img.copy()
            
            if classname == "head":   
                if not ONLY_VIEW_DOCUMENTS:
                    hxtl = head_bbox_list[randomIndexList[i]][0]
                    hytl = head_bbox_list[randomIndexList[i]][1]
                    hxbr = head_bbox_list[randomIndexList[i]][2]
                    hybr = head_bbox_list[randomIndexList[i]][3]
                    head_croped = src[hytl:hybr, hxtl:hxbr]
                    cv2.imwrite("temp2_image.jpg", head_croped)
                    shutil.move("temp2_image.jpg", os.path.join(test_head_imageRootpath,naming(testCount)+".jpg"))
                test_headAttributeFile.write(head_anno_list[randomIndexList[i]])
                test_headAttributeFile.write("\n")
                
            elif classname == "upper":   
                if not ONLY_VIEW_DOCUMENTS:
                    uxtl = upper_bbox_list[randomIndexList[i]][0]
                    uytl = upper_bbox_list[randomIndexList[i]][1]
                    uxbr = upper_bbox_list[randomIndexList[i]][2]
                    uybr = upper_bbox_list[randomIndexList[i]][3]
                    upper_croped = src[uytl:uybr, uxtl:uxbr]
                    cv2.imwrite("temp2_image.jpg", upper_croped)
                    shutil.move("temp2_image.jpg", os.path.join(test_upper_imageRootpath,naming(testCount)+".jpg"))
                test_upperAttributeFile.write(upper_anno_list[randomIndexList[i]])
                test_upperAttributeFile.write("\n")
                
                
            elif classname == "lower":   
                if not ONLY_VIEW_DOCUMENTS:
                    lxtl = lower_bbox_list[randomIndexList[i]][0]
                    lytl = lower_bbox_list[randomIndexList[i]][1]
                    lxbr = lower_bbox_list[randomIndexList[i]][2]
                    lybr = lower_bbox_list[randomIndexList[i]][3]
                    lower_croped = src[lytl:lybr, lxtl:lxbr]
                    cv2.imwrite("temp2_image.jpg", lower_croped)
                    shutil.move("temp2_image.jpg", os.path.join(test_lower_imageRootpath,naming(testCount)+".jpg"))
                test_lowerAttributeFile.write(lower_anno_list[randomIndexList[i]])
                test_lowerAttributeFile.write("\n")
                
            else:
                if not ONLY_VIEW_DOCUMENTS:
                    axtl = all_bbox_list[randomIndexList[i]][0]
                    aytl = all_bbox_list[randomIndexList[i]][1]
                    axbr = all_bbox_list[randomIndexList[i]][2]
                    aybr = all_bbox_list[randomIndexList[i]][3]
                    all_croped = src[aytl:aybr, axtl:axbr]
                    cv2.imwrite("temp2_image.jpg", all_croped)
                    shutil.move("temp2_image.jpg", os.path.join(test_all_imageRootpath,naming(testCount)+".jpg"))
                test_allAttributeFile.write(all_anno_list[randomIndexList[i]])
                test_allAttributeFile.write("\n")
  
            testCount  += 1
        
        else: ##해당 이미지는 최소가 아닌경우.
            pass
        
        i += 1
        
        if i >= len(randomIndexList):
            i = 0
            randomIndexList = list(set(randomIndexList) - set(testIndex))
                
    print("{}장이 테스트셋으로 옮겨짐.".format(testCount))
    trainList = list(set(randomIndexList) - set(testIndex))
    
    makeStatisticsFile("test", testClassDict)

    for i in trainList:
#        stream = open(os.path.join(image_list[i]), "rb")
#        _bytes = bytearray(stream.read())
#        numpyarray = numpy.asarray(_bytes, dtype=numpy.uint8)
#        img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        
        if classname == "head":
            annoBinary = head_anno_list[i]
        elif classname == "upper":
            annoBinary = upper_anno_list[i]
        elif classname == "lower":
            annoBinary = lower_anno_list[i]
        else:
            annoBinary = all_anno_list[i]
        
        
        addBinary(classname, annoBinary, trainClassDict)
        
        if not ONLY_VIEW_DOCUMENTS:
            shutil.copy(os.path.join(image_list[i]), "temp_image.jpg")
            img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
        
            src = img.copy()
        
        if classname == "head":   
            if not ONLY_VIEW_DOCUMENTS:
                hxtl = head_bbox_list[i][0]
                hytl = head_bbox_list[i][1]
                hxbr = head_bbox_list[i][2]
                hybr = head_bbox_list[i][3]
                head_croped = src[hytl:hybr, hxtl:hxbr]
                cv2.imwrite("temp2_image.jpg", head_croped)
                shutil.move("temp2_image.jpg", os.path.join(train_head_imageRootpath,naming(trainCount)+".jpg"))
            train_headAttributeFile.write(head_anno_list[i])
            train_headAttributeFile.write("\n")
        
        
        elif classname == "upper":   
            if not ONLY_VIEW_DOCUMENTS:
                uxtl = upper_bbox_list[i][0]
                uytl = upper_bbox_list[i][1]
                uxbr = upper_bbox_list[i][2]
                uybr = upper_bbox_list[i][3]
                upper_croped = src[uytl:uybr, uxtl:uxbr]
                cv2.imwrite("temp2_image.jpg", upper_croped)
                shutil.move("temp2_image.jpg", os.path.join(train_upper_imageRootpath,naming(trainCount)+".jpg"))
            train_upperAttributeFile.write(upper_anno_list[i])
            train_upperAttributeFile.write("\n")
        
        
        elif classname == "lower":   
            if not ONLY_VIEW_DOCUMENTS:
                lxtl = lower_bbox_list[i][0]
                lytl = lower_bbox_list[i][1]
                lxbr = lower_bbox_list[i][2]
                lybr = lower_bbox_list[i][3]
                lower_croped = src[lytl:lybr, lxtl:lxbr]
                cv2.imwrite("temp2_image.jpg", lower_croped)
                shutil.move("temp2_image.jpg", os.path.join(train_lower_imageRootpath,naming(trainCount)+".jpg"))
            train_lowerAttributeFile.write(lower_anno_list[i])
            train_lowerAttributeFile.write("\n")
        else:
            if not ONLY_VIEW_DOCUMENTS:
                axtl = all_bbox_list[i][0]
                aytl = all_bbox_list[i][1]
                axbr = all_bbox_list[i][2]
                aybr = all_bbox_list[i][3]
                all_croped = src[aytl:aybr, axtl:axbr]
                cv2.imwrite("temp2_image.jpg", all_croped)
                shutil.move("temp2_image.jpg", os.path.join(train_all_imageRootpath,naming(trainCount)+".jpg"))
            train_allAttributeFile.write(all_anno_list[i])
            train_allAttributeFile.write("\n")
    
        trainCount  += 1
        
        
    makeStatisticsFile("train", trainClassDict)
    print("{}장이 트레인셋으로 옮겨짐.".format(trainCount))

    if classname == "common":   
        train_allAttributeFile.close()
        test_allAttributeFile.close()
    elif classname == "head":   
        train_headAttributeFile.close()
        test_headAttributeFile.close()
    elif classname == "upper":      
        train_upperAttributeFile.close()
        test_upperAttributeFile.close()
    else:
        train_lowerAttributeFile.close()
        test_lowerAttributeFile.close()
    

start = time.time()
totalClassDict = {}

startFrameNumber, totalClassDict =  readCvatxml()

if MAX > startFrameNumber:
    MAX = startFrameNumber
makeDataset(MAX, CLASS, totalClassDict)

end = time.time()
print("걸린시간 : {}s".format(end-start))


while True:
    pass