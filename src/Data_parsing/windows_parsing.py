#-------모듈 참조-------
import os
import shutil
#요구사항에 맞춘 xml을 생성하는데 사용
from xml.etree.ElementTree import Element, SubElement, ElementTree
#html형식의 xml 내부 요소를 다루는데 사용
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
#------------------------

#-----전역변수 선언------
temp_list = []
image_name_list = []
img_dir_list = []
dir_name_list = []
xml_list = []
create_false_list = []
copy_dir_list = []

parsing_dir_list = []
parsing_dir = ''
#------------------------

#디렉터리 내부 정보의 파일명 및 위치 정보를 얻음
def get_directory():
    temp = os.getcwd()
    root_dir = os.path.dirname(temp)
    temp = os.listdir(root_dir)

    for x in temp:
        #Images 디렉터리 내부 파일, 디렉터리 정보 저장
        if x == 'Images':
            images_dir = os.path.join(root_dir, x)
            temp_list = os.listdir(images_dir)
            global dir_name_list
            dir_name_list = temp_list

            #image 파일 이름 리스트 추가 및 image 디렉터리 위치 저장
            for y in temp_list:
                temp_path = os.path.join(images_dir, y)
                temp2_list = os.listdir(temp_path)
                img_dir_list.append(temp_path)
                for z in temp2_list:
                    filename, file_type = z.split('.')
                    if file_type == 'jpg':
                        image_name_list.append(filename)

        #Xmls 하위 xml들 파일 리스트를 xml_list에 추가 및 xmls 디렉터리 위치 저장
        elif x == 'Xmls':
            xmls_dir = os.path.join(root_dir, x)
            temp_path = os.listdir(xmls_dir)

            for y in temp_path:
                filename, z = y.split('.')
                if z == 'xml':
                    temp = os.path.join(xmls_dir, filename+'.xml')
                    xml_list.append(temp)
                else:
                    print("xml 파일이 Xmls 디렉터리에 없음")

    global parsing_dir
    parsing_dir = os.path.join(root_dir, 'Parsing_result')

def set_directory():
    #이미지 디렉터리 복사
    for x in range(0, len(img_dir_list)):
        for y in dir_name_list:
            parsing_dir_list.append(os.path.join(parsing_dir, y))
        try:
            shutil.copytree(img_dir_list[x], parsing_dir_list[x])
            copy_dir_list.append(dir_name_list[x])
        except:
            create_false_list.append(dir_name_list[x])
    print("디렉터리 복사 완료")
    print("복사 성공 디렉터리 리스트\n"+str(copy_dir_list))
    print("복사 실패 디렉터리 리스트\n"+str(create_false_list))

def write_xmls():
    global count
    count = 0
    #html 형식의 xml을 읽어들임
    for x in xml_list:
        f = open(x, 'r', encoding='utf-8')
        lines = ''
        while True:
            line = f.readline()
            if not line: break
            lines += line
        f.close()
        #bs를 BeautifulSoup 객체로 초기화
        bs = BeautifulSoup(lines, 'lxml')
        #bs를 이용해 image 하위의 name, width, height 값을 얻음
        for img in bs.find_all('image'):
            name = img.get("name")
            width = img.get("width")
            height = img.get("height")
            test = bs.find_all('image', class_ = name)
            # list 정보 초기화
            label_list = []
            xtl_list = []
            ytl_list = []
            xbr_list = []
            ybr_list = []
            #bs를 이용해  box 하위의 label, xtl, xbr, ybr 값을 얻음
            for box in img.find_all("box"):
                label_list.append(box.get("label"))
                xtl_list.append(box.get("xtl"))
                ytl_list.append(box.get("ytl"))
                xbr_list.append(box.get("xbr"))
                ybr_list.append(box.get("ybr"))
            #xml 하위 Element 모듈을 통해 얻은 값들을 요구하는 형식에 맞게 포맷
            root = Element('annotation')
            SubElement(root, 'folder').text = ""
            SubElement(root, 'filename').text = name

            sourceTag = SubElement(root, 'source')
            SubElement(sourceTag, 'database').text = 'Unknown'

            sizeTag = SubElement(root, 'size')
            SubElement(sizeTag, 'width').text = width
            SubElement(sizeTag, 'height').text = height
            SubElement(sizeTag, 'depth').text = '3'

            SubElement(root, 'segmented').text = '0'

            for y in range(0, len(label_list)):
                objTag = SubElement(root, 'object')
                SubElement(objTag, 'name').text = label_list[y]
                SubElement(objTag, 'pose').text = 'Unspecified'
                SubElement(objTag, 'truncated').text = '0'
                SubElement(objTag, 'difficult').text = '0'

                bndboxTag = SubElement(objTag, 'bndbox')
                SubElement(bndboxTag, 'xmin').text = xtl_list[y]
                SubElement(bndboxTag, 'ymin').text = ytl_list[y]
                SubElement(bndboxTag, 'xmax').text = xbr_list[y]
                SubElement(bndboxTag, 'ymax').text = ybr_list[y]
            #----------------포맷변환 끝-------------------

            #위에서 바꾼 포맷들을 xml파일로 생성
            tree = ElementTree(root)
            filename, temp = name.split('.')
            temp = os.path.join(parsing_dir_list[count], filename+'.xml')
            tree.write(temp)
            print("%s.xml 파일 생성" % (filename))
        count += 1

if __name__ == '__main__':
    get_directory()
    set_directory()
    write_xmls()