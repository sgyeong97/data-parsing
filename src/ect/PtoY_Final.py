
###최신. 2020-02-04버전임.


import json
import xml.etree.ElementTree as ET
import os
import shutil


dir_name = r"D:\신지영_업무\dataset\0723_dataset(아산and성남)\아산토탈\end\Xmls" #.xml파일의 위치를 전부 로드한다.(이미지 섞여있어도 됨.) (절대경로)
save_dir = r"D:\신지영_업무\dataset\0723_dataset(아산and성남)\아산토탈\end"           #yolo style txt 저장 위치. (절대경로)
info_dir = r"D:\신지영_업무\dataset\0723_dataset(아산and성남)\아산토탈"
category_dir = r"D:\신지영_업무\dataset\0723_dataset(아산and성남)\Train.names" #카테고리 로드 (절대경로)

person_count = 0
car_count = 0
face_count = 0
license_count = 0

#적어놓은 카테고리를 리스트화
with open(category_dir, 'r') as categorys:
    namelist = [cate.strip() for cate in categorys]
    
#작업을 진행할 디렉토리 지정
file_list = os.listdir(dir_name)
print(len(file_list), end="")
print("개 작업 예정.")



if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
#결과를 저장할 디렉토리 오픈 혹은 생성
    

def convert_xywh(width,height,xmin,xmax,ymin,ymax):
    dw = 1/width
    dy = 1/height

    #[x,y,w,h]
    xywh = [str(((xmin+xmax)/2.0)*dw),str(((ymin+ymax)/2.0)*dy),str((xmax-xmin)*dw),str((ymax-ymin)*dy)] #YOLO의 영역 표시방법을 계산식으로 써놓은 모습.
    
    return xywh


for file in file_list:


    if file.endswith(".xml"): #확장자가 xml이라면 작업 시행
        tree = ET.parse(os.path.join(dir_name,str(file)))
        note = tree.getroot()
        
        fname = note.find('filename').text
        
        size = note.find('size')
        height = int(size.find('height').text) #이미지의 height
        width = int(size.find('width').text) #이미지의 width

        result = open(os.path.join(save_dir, file[:-4]+".txt"),"w")
        info_txt = open(os.path.join(info_dir, "class_info.txt"), "w")
        
        # print(fname[:-4])
        
        for child in note.findall('object'): #모든 객체에 대한 작업 실행
            name = child.find('name').text #객체의 카테고리 이름
            
            #-------------------------------------------------
            
            if name == "bus" or name == "truck" or name == "excavator" or name == "forklift" or name == "ladder truck" or name == "unknown car" :
                name = "car"
                
            #-------------------------------------------------
            
            
            count = 0
            if name in namelist: #category list에 해당하는 카테고리의 이름이 있다면 작업 실행
                name = child.find('name').text
                bndbox = child.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                
                yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)
                #VOC 영역표시법을 YOLO로 변환하는 함수 실행
                
                if name == namelist[0].strip():
                    result.write("0"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
                    person_count += 1
                elif name == namelist[1].strip():
                    result.write("1"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
                    car_count += 1
                # elif name == namelist[2].strip(): #face
                #     w = xmax-xmin
                #     h = ymax-ymin
                #     result.write("2" + " " + yolo_data[0] + " " + yolo_data[1] + " " + yolo_data[2] + " " + yolo_data[3] + "\n")
                #     face_count += 1
                #     count += 1
                # elif name == namelist[3].strip(): #license plate'''
                #     w = xmax-xmin
                #     h = ymax-ymin
                #     result.write("3" + " " + yolo_data[0] + " " + yolo_data[1] + " " + yolo_data[2] + " " + yolo_data[3] + "\n")
                #     license_count += 1
                #     count += 1
            pass
        #if count == 0:
            #result.close()
            #os.remove(os.path.join(save_dir, file[:-4]+'.txt'))
        info_txt.write("[객체 정보]\n" + "Person = " + str(person_count) + "\nCar = " + str(car_count) + "\nFace = " + str(face_count) + "\nLicense plate = " + str(license_count)
                       + "\nTotal = " + str(person_count+car_count+face_count+license_count))
        result.close()
