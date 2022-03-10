# -*- coding: utf-8 -*-
"""
v1.0
pureExtractorV1.3을 바탕으로 만듬.
일단 임시코드이며, 머리만 체크함. 추후 확장 예정임.

v1.1 0511
모든 어트리뷰트로 확장함.
숄더백, 백팩 수정해야함.(cvat 라벨에서 수정하고 코드에서도 수정할것_수정완료)

v1.1 0629
가방이 두개 있는 경우 버림.

"""

import os
import xml.etree.ElementTree as ET
import shutil
from xml.dom import minidom
import cv2


cvatxmlRootpath = r"C:\Users\kth\Documents\카카오톡 받은 파일\0708어또리뷰또\통합cvatxmls"
newImageRootpath = os.path.join(cvatxmlRootpath, "..")


onlyStatistics = True


## 이미지 원본 있는 패스.
imageRootpath = r"F:\Annotation_tasks"



all_newImageRootpath = os.path.join(newImageRootpath, "common", "common_images")
head_newImageRootpath = os.path.join(newImageRootpath, "head","head_images")
upper_newImageRootpath = os.path.join(newImageRootpath, "upper","upper_images")
lower_newImageRootpath = os.path.join(newImageRootpath, "lower","lower_images")


if not onlyStatistics:
    os.makedirs(all_newImageRootpath,exist_ok=True)
    os.makedirs(head_newImageRootpath,exist_ok=True)
    os.makedirs(upper_newImageRootpath,exist_ok=True)
    os.makedirs(lower_newImageRootpath,exist_ok=True)




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
                return os.path.join(path, filename)


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
 


def readCvatxml():
    startFrameNumber = 0
    
    if not onlyStatistics:
        allAttributeFile = open(os.path.join(all_newImageRootpath, "..", "common_attribute_annotation.txt"), "w")
        headAttributeFile = open(os.path.join(head_newImageRootpath, "..", "head_attribute_annotation.txt"), "w")
        upperAttributeFile = open(os.path.join(upper_newImageRootpath, "..", "upper_attribute_annotation.txt"), "w")
        lowerAttributeFile = open(os.path.join(lower_newImageRootpath, "..", "lower_attribute_annotation.txt"), "w")
        #f = open(os.path.join(newImageRootpath, "dfdf.txt"), "w")

    

    cvatxmllist = os.listdir(cvatxmlRootpath)
    cvatxmlNameList = []
    for line in cvatxmllist:
        cvatxmlNameList.append(line[:-4])

    
    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            
            
            
             
            for image in note.findall("image"):
                imageName= image.get("name")
                #_id = image.get("id")
                
                ## 기본적으로 한개도 안쳐져있는 경우 cvatxmls에 기록이 안됨.
                
            
                ### 가방이 두개 있는 경우 버림.
                MOREBAG = False
                bagdk = 0
                plasticbag = 0
                shoulderbag = 0
                totebag = 0
                backpack = 0
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
                    #print(imageName)
                    continue
                #--------------------
            
            
                ### 4개여도 같은 박스중첩이 있을 경우 버림. 
                labelList = []
                for box in image.findall("box"):
                    labelList.append(box.get("label"))
                if not (len(set(labelList)) == 4):
                    #print(imageName)
                    continue
                #-------------------
                
                
                
                
                
                
                                
                                
                
                for box in image.findall("box"):
                    label = box.get("label")
                    
                    
                    if label == "all":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)
                        
                        
                        if not onlyStatistics:
                            shutil.copy(getImagePath(imageName), "temp_image.jpg")
                            img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
                            #img = cv2.imread(os.path.join(getImagePath(imageName)), cv2.IMREAD_COLOR)
                            
                            
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            cv2.imwrite(os.path.join(all_newImageRootpath,naming(startFrameNumber)+".jpg"), croped)
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "gender":
                                gender = attribute.text
                                if gender == "male":
                                    man, woman, unknown_gender = 1,0,0
                                elif gender == "female":
                                    man, woman, unknown_gender = 0,1,0
                                else: ##unknown gender
                                    man, woman, unknown_gender = 0,0,1
                               
                                
                            elif attribute.get("name") == "age":
                                age = attribute.text
                                if age == "20~70":
                                    infant,clild,teenager,adult,oldperson = 0,0,0,1,0
                                elif age == "0~7":
                                    infant,clild,teenager,adult,oldperson = 1,0,0,0,0
                                elif age == "8~13":
                                    infant,clild,teenager,adult,oldperson = 0,1,0,0,0
                                elif age == "14~19":
                                    infant,clild,teenager,adult,oldperson = 0,0,1,0,0
                                else: ## 70~
                                    infant,clild,teenager,adult,oldperson = 0,0,0,0,1
                               
                                
                            elif attribute.get("name") == "bag_color_unknown":
                                bag_color_unknown = attribute.text
                                bag_color_unknown = readBoodreturnInt(bag_color_unknown)
                                    
                            elif attribute.get("name") == "bag_white":
                                bag_white = attribute.text
                                bag_white = readBoodreturnInt(bag_white)
                            
                            elif attribute.get("name") == "bag_black":
                                bag_black = attribute.text
                                bag_black = readBoodreturnInt(bag_black)
                                
                            elif attribute.get("name") == "bag_grey":
                                bag_grey = attribute.text
                                bag_grey = readBoodreturnInt(bag_grey)
                                
                            elif attribute.get("name") == "bag_pink":
                                bag_pink = attribute.text
                                bag_pink = readBoodreturnInt(bag_pink)
                                
                            elif attribute.get("name") == "bag_brown":
                                bag_brown = attribute.text
                                bag_brown = readBoodreturnInt(bag_brown)
                                
                            elif attribute.get("name") == "bag_blue":
                                bag_blue = attribute.text
                                bag_blue = readBoodreturnInt(bag_blue)
                                
                            elif attribute.get("name") == "bag_green":
                                bag_green = attribute.text
                                bag_green = readBoodreturnInt(bag_green)
                                
                            elif attribute.get("name") == "bag_yellow":
                                bag_yellow = attribute.text
                                bag_yellow = readBoodreturnInt(bag_yellow)
                                
                            elif attribute.get("name") == "bag_red":
                                bag_red = attribute.text
                                bag_red = readBoodreturnInt(bag_red)
                                
                            elif attribute.get("name") == "unknown_bag":
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
                                
                            elif attribute.get("name") == "bagless":
                                bagless = attribute.text
                                bagless = readBoodreturnInt(bagless)
                                bagnone = bagless

                        ALL_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(man,woman,unknown_gender,infant,clild,teenager,adult,oldperson,backpack,totebag,shoulderbag,plasticbag,bagdk,bagnone, bag_red, bag_yellow, bag_green, bag_blue, bag_brown, bag_pink, bag_grey, bag_black, bag_white, bag_color_unknown)
                        #classesCOMmon = ['man','woman','genderdk','infant','clild','teenager','adult','oldperson','backpack','totebag','shoulderbag','plasticbag','bagdk','bagnone','begred','begyellow','beggreen','begblue','begbrown','begpink','beggray','begblack','begwhite','begcolordk'] 
                        if not onlyStatistics:
                            allAttributeFile.write(ALL_classes+"\n")
                    
                    
                    elif label == "head":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)
                        
                        if not onlyStatistics:
                            shutil.copy(getImagePath(imageName), "temp_image.jpg")
                            img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
                            #img = cv2.imread(os.path.join(getImagePath(imageName)), cv2.IMREAD_COLOR)
                
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            cv2.imwrite(os.path.join(head_newImageRootpath,naming(startFrameNumber)+".jpg"), croped)
                        for attribute in box.findall("attribute"):
                                
                            if attribute.get("name") == "hair":
                                hair = attribute.text
                                if hair == "short":
                                    short, long, bald, hairdk = 1,0,0,0
                                elif hair == "long":
                                    short, long, bald, hairdk = 0,1,0,0
                                elif hair == "bald":
                                    short, long, bald, hairdk = 0,0,1,0
                                elif hair == "unknown":
                                    short, long, bald, hairdk = 0,0,0,1
                               
                                
                            elif attribute.get("name") == "hat_red":
                                hat_red = attribute.text
                                hat_red = readBoodreturnInt(hat_red)
                                    
                                
                            elif attribute.get("name") == "hat_yellow":
                                hat_yellow = attribute.text
                                hat_yellow = readBoodreturnInt(hat_yellow)
                                
                            elif attribute.get("name") == "hat_green":
                                hat_green = attribute.text
                                hat_green = readBoodreturnInt(hat_green)
                                
                            elif attribute.get("name") == "hat_blue":
                                hat_blue = attribute.text
                                hat_blue = readBoodreturnInt(hat_blue)
                                
                            elif attribute.get("name") == "hat_brown":
                                hat_brown = attribute.text
                                hat_brown = readBoodreturnInt(hat_brown)
                                
                            elif attribute.get("name") == "hat_pink":
                                hat_pink = attribute.text
                                hat_pink = readBoodreturnInt(hat_pink)
                                
                            elif attribute.get("name") == "hat_grey":
                                hat_grey = attribute.text
                                hat_grey = readBoodreturnInt(hat_grey)
                                
                            elif attribute.get("name") == "hat_black":
                                hat_black = attribute.text
                                hat_black = readBoodreturnInt(hat_black)
                                
                            elif attribute.get("name") == "hat_white":
                                hat_white = attribute.text
                                hat_white = readBoodreturnInt(hat_white)
                                
                            elif attribute.get("name") == "hat_color_unknown":
                                hat_color_unknown = attribute.text
                                hat_color_unknown = readBoodreturnInt(hat_color_unknown)
                            
                            elif attribute.get("name") == "hat":
                                hat = attribute.text
                                if hat == "hatless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,1,0
                                    
                                    #어노테이터 실수 제거 코드.
                                    hat_red, hat_yellow, hat_green, hat_blue, hat_brown, hat_pink, hat_grey, hat_black, hat_white, hat_color_unknown = 0,0,0,0,0, 0,0,0,0,0
                                    
                                elif hat == "cap":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 1,0,0,0,0,0,0
                                elif hat == "brimmed":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,1,0,0,0,0,0
                                elif hat == "brimless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,1,0,0,0,0
                                elif hat == "helmat":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,1,0,0,0
                                elif hat == "hood":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,1,0,0
                                elif hat == "unknown":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,0,1

                        HEAD_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(cap, visor, novisor, helmat, hood, nohat, hatdk,hat_red,hat_yellow,hat_green,hat_blue,hat_brown,hat_pink,hat_grey,hat_black,hat_white,hat_color_unknown, short, long, bald, hairdk)
                        #classesHEad =                                                 ['cap','visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrown','hatpink','hatgray','hatblack','hatwhite','hatcolordk','shot','long','bald','hairdk']
                        if not onlyStatistics:
                            headAttributeFile.write(HEAD_classes+"\n")

                    elif label == "upper":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)
                        
                        if not onlyStatistics:
                            shutil.copy(getImagePath(imageName), "temp_image.jpg")
                            img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
                            #img = cv2.imread(os.path.join(getImagePath(imageName)), cv2.IMREAD_COLOR)

                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            cv2.imwrite(os.path.join(upper_newImageRootpath,naming(startFrameNumber)+".jpg"), croped)
                        for attribute in box.findall("attribute"):

                            if attribute.get("name") == "top_white":
                                top_white = attribute.text
                                top_white = readBoodreturnInt(top_white)
                                
                            elif attribute.get("name") == "top_color_unknown":
                                top_color_unknown = attribute.text
                                top_color_unknown = readBoodreturnInt(top_color_unknown)
                            
                            elif attribute.get("name") == "top_black":
                                top_black = attribute.text
                                top_black = readBoodreturnInt(top_black)
                            
                            elif attribute.get("name") == "top_color_unknown":
                                top_color_unknown = attribute.text
                                top_color_unknown = readBoodreturnInt(top_color_unknown)

                            elif attribute.get("name") == "top_grey":
                                top_grey = attribute.text
                                top_grey = readBoodreturnInt(top_grey)
                            
                            elif attribute.get("name") == "top_pink":
                                top_pink = attribute.text
                                top_pink = readBoodreturnInt(top_pink)
                            
                            elif attribute.get("name") == "top_brown":
                                top_brown = attribute.text
                                top_brown = readBoodreturnInt(top_brown)
                            
                            elif attribute.get("name") == "top_blue":
                                top_blue = attribute.text
                                top_blue = readBoodreturnInt(top_blue)
                            
                            elif attribute.get("name") == "top_green":
                                top_green = attribute.text
                                top_green = readBoodreturnInt(top_green)
                            
                            elif attribute.get("name") == "top_yellow":
                                top_yellow = attribute.text
                                top_yellow = readBoodreturnInt(top_yellow)
                            
                            elif attribute.get("name") == "top_red":
                                top_red = attribute.text
                                top_red = readBoodreturnInt(top_red)
                            
                            elif attribute.get("name") == "top":
                                top = attribute.text
                                if top == "long_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 1,0,0
                                elif top == "short_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,1,0
                                else: ##unknown sleeve
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,0,1
                                longshirt = long_sleeve
                                shortshirt = short_sleeve
                    
                        UPPER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(longshirt,shortshirt, unknown_sleeve, top_red,top_yellow,top_green,top_blue,top_brown,top_pink,top_grey,top_black,top_white,top_color_unknown)
                        
                        if not onlyStatistics:
                            upperAttributeFile.write(UPPER_classes+"\n")
                        
                    elif label == "lower":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)
                        
                        if not onlyStatistics:
                            shutil.copy(getImagePath(imageName), "temp_image.jpg")
                            img = cv2.imread("temp_image.jpg", cv2.IMREAD_COLOR)
                            #img = cv2.imread(os.path.join(getImagePath(imageName)), cv2.IMREAD_COLOR)
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            cv2.imwrite(os.path.join(lower_newImageRootpath,naming(startFrameNumber)+".jpg"), croped)
                        for attribute in box.findall("attribute"):
                            
                            if attribute.get("name") == "bottom_color_unknown":
                                bottom_color_unknown = attribute.text
                                bottom_color_unknown = readBoodreturnInt(bottom_color_unknown)
                                
                            elif attribute.get("name") == "bottom_white":
                                bottom_white = attribute.text
                                bottom_white = readBoodreturnInt(bottom_white)
                            
                            elif attribute.get("name") == "bottom_black":
                                bottom_black = attribute.text
                                bottom_black = readBoodreturnInt(bottom_black)
                            
                            elif attribute.get("name") == "bottom_grey":
                                bottom_grey = attribute.text
                                bottom_grey = readBoodreturnInt(bottom_grey)
                            
                            elif attribute.get("name") == "bottom_pink":
                                bottom_pink = attribute.text
                                bottom_pink = readBoodreturnInt(bottom_pink)
                            
                            elif attribute.get("name") == "bottom_brown":
                                bottom_brown = attribute.text
                                bottom_brown = readBoodreturnInt(bottom_brown)
                            
                            elif attribute.get("name") == "bottom_blue":
                                bottom_blue = attribute.text
                                bottom_blue = readBoodreturnInt(bottom_blue)
                            
                            elif attribute.get("name") == "bottom_green":
                                bottom_green = attribute.text
                                bottom_green = readBoodreturnInt(bottom_green)
                            
                            elif attribute.get("name") == "bottom_yellow":
                                bottom_yellow = attribute.text
                                bottom_yellow = readBoodreturnInt(bottom_yellow)
                            
                            elif attribute.get("name") == "bottom_red":
                                bottom_red = attribute.text
                                bottom_red = readBoodreturnInt(bottom_red)
                            
                            elif attribute.get("name") == "bottom":
                                bottom = attribute.text
                                if bottom == "long_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 1,0,0,0,0
                                elif bottom == "short_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,1,0,0,0
                                elif bottom == "long_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,1,0,0
                                elif bottom == "short_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,1,0
                                else: # unknown bottom
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,0,1
                            elif attribute.get("name") == "shoes_color":
                                shoes_color = attribute.text
                                if shoes_color == "shoes_red":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 1,0,0,0,0,0,0,0,0,0
                                elif shoes_color == "shoes_yellow":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,1,0,0,0,0,0,0,0,0
                                elif shoes_color == "shoes_green":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,1,0,0,0,0,0,0,0
                                elif shoes_color == "shoes_blue":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,1,0,0,0,0,0,0
                                elif shoes_color == "shoes_brown":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,1,0,0,0,0,0
                                elif shoes_color == "shoes_pink":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,1,0,0,0,0
                                elif shoes_color == "shoes_grey":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,1,0,0,0
                                elif shoes_color == "shoes_black":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,1,0,0
                                elif shoes_color == "shoes_white":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,1,0
                                else: #shoes_color_unknown
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,0,1
                                                                                                                                                                                                                                                       
                        LOWER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(long_pants, short_pants, long_skirt, short_skirt, unknown_bottom, bottom_red, bottom_yellow, bottom_green, bottom_blue, bottom_brown, bottom_pink, bottom_grey, bottom_black, bottom_white, bottom_color_unknown,shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown)
                        
                        if not onlyStatistics:
                            lowerAttributeFile.write(LOWER_classes+"\n")
                    else:
                        #print(label)
                        pass

                startFrameNumber += 1

    if not onlyStatistics:          
        allAttributeFile.close()
        headAttributeFile.close()   
        upperAttributeFile.close()
        lowerAttributeFile.close()
    
#    f.close()
    
    print("완료")
                    

readCvatxml()

while True:
    pass

    
    
    
    

