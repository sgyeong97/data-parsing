import sys
import os
import shutil  # 파일 복사에 도움을 주는 모듈 (파이썬 내장 모듈)

from xml.etree.ElementTree import Element, SubElement, ElementTree
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

temp_list = []
video_name_list = []
copy_dir_list = []
xmls_list = []


def get_directory():  # 디렉터리 주소 리스트 추가
    for x in os.listdir(images_dir):  # 디렉터리 원본 절대 주소
        video_name_list.append(x)
        temp_list.append(images_dir + '/' + x)

    for x in range(0, len(temp_list)):  # 복사 디렉터리 절대 주소
        copy_dir_list.append(database_dir + '/' + video_name_list[x])


def set_directory():  # 디렉터리 복사 및 추가 생성
    print("Image 디렉터리 복사를 시도합니다.")

    for x in range(0, len(temp_list)):
        try:
            shutil.copytree(temp_list[x], copy_dir_list[x])
            print("[%s] 디렉터리 복사" % temp_list[x])
            os.mkdir("%s/xmls" % copy_dir_list[x])
            print("%s/xmls 디렉터리 생성" % copy_dir_list[x])
        except:
            break
    print("디렉터리가 이미 있습니다.")


def get_xmls():
    for x in os.listdir(cvatxmls_dir):
        temp = cvatxmls_dir + '/' + x
        xmls_list.append(temp)


def write_xmls():
    for x in xmls_list:
        f = open(x, 'r')
        lines = ''
        while True:
            line = f.readline()
            if not line: break
            lines += line
        f.close()

        bs = BeautifulSoup(lines, 'html.parser')

        for img in bs.find_all('image'):
            name = img.get("name")
            width = img.get("width")
            height = img.get("height")
            label_list = []
            xtl_list = []
            ytl_list = []
            xbr_list = []
            ybr_list = []

            for box in bs.find_all('box'):
                label_list.append(box.get("label"))
                xtl_list.append(box.get("xtl"))
                ytl_list.append(box.get("ytl"))
                xbr_list.append(box.get("xbr"))
                ybr_list.append(box.get("ybr"))

            label = 'cross'

            root = Element('annotaion')
            SubElement(root, 'folder').text = ""
            SubElement(root, 'filename').text = name

            sourceTag = SubElement(root, 'source')
            SubElement(sourceTag, 'database').text = 'Unknown'

            sizeTag = SubElement(root, 'size')
            SubElement(sizeTag, 'width').text = width
            SubElement(sizeTag, 'height').text = height
            SubElement(sizeTag, 'depth').text = '3'

            SubElement(root, 'segmented').text = '0'

            for x in range(0, len(label_list)):
                objTag = SubElement(root, 'object')
                SubElement(objTag, 'name').text = label_list[x]
                SubElement(objTag, 'pose').text = 'Unspecified'
                SubElement(objTag, 'truncated').text = '0'
                SubElement(objTag, 'difficult').text = '0'

                bndboxTag = SubElement(objTag, 'bndbox')
                SubElement(bndboxTag, 'xmin').text = xtl_list[x]
                SubElement(bndboxTag, 'ymin').text = ytl_list[x]
                SubElement(bndboxTag, 'xmax').text = xbr_list[x]
                SubElement(bndboxTag, 'ymax').text = ybr_list[x]

            tree = ElementTree(root)
            filename, temp = name.split('.')
            temp = database_dir + '/' + filename[:-5] + '/xmls/' + filename + '.xml'
            tree.write(temp)
            print("%s.xml 파일 생성" % (filename))


if __name__ == '__main__':
    # 이 코드가 실행 코드일때
    get_directory()
    set_directory()
    get_xmls()
    write_xmls()