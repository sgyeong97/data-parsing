import datetime #현재 날짜 정보 얻는 모듈
import os
import shutil
import sys
from os import listdir
from os.path import isfile, join
from dateutil.relativedelta import relativedelta #시간 연산을 위한 모듈
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, ElementTree

global date, date_dir, last_month
global root_dir
global dataset_dir, dataset_dir_list
global images_dir, images_dir_list
global videos_dir
global uniTrainSet_dir_path
global uniTrainSet_cvatxmls_path, uniTrainSet_documents_path
global uniTrainSet_notpure_path, uniTrainSet_pure_path
global uniTrainSet_xmls_path
global totalCarCountBox, totalPersonCountBox, totalImageCount
totalImageCount=totalCarCountBox=totalPersonCountBox = 0


uniTrainSet_cvatxmls_list = []
uniTrainSet_xmls_list = []
xml_name_list = []
xml_path_list = []
cars = ["car", "bus", "truck", "excavator", "ladder truck", "unknown car"]

def get_date():
    global date, last_month
    now = datetime.datetime.now()
    date = now.strftime('%Y_%m')
    last_month = (datetime.datetime.now() - relativedelta(months=1)).strftime('%Y_%m')

def get_dir_path():
    temp = os.getcwd()
    global root_dir, dataset_dir, dataset_dir_list, images_dir, images_dir_list, videos_dir
    root_dir = os.path.dirname(temp)
    temp = os.listdir(root_dir)
    for x in temp:
        #DataSet 디렉터리에서 처리해야할 일
        if x == 'DataSets':
            dataset_dir = os.path.join(root_dir, x)
            dataset_dir_list = os.listdir(dataset_dir)

        elif x == 'Images':
            images_dir = os.path.join(root_dir, x)
            images_dir_list = os.listdir(images_dir)

        elif x == 'Videos':
            videos_dir = os.path.join(root_dir, x)

def set_dir_dataSets(): #DataSets 하위 디렉터리 생성 진행
    x = 'DataSets'
    temp2 = os.path.join(root_dir, x)
    temp2_list = os.listdir(temp2)
    global date_dir, bool_temp
    bool_temp = False
    for y in temp2_list:
        date_dir = os.path.join(temp2, date)
        if y == date:
            bool_temp = True
            break
    if not bool_temp:
        print("%s 디렉터리 생성" % date)
        os.mkdir(date_dir)

    temp = os.listdir(date_dir)
    temp2 = os.path.join(dataset_dir, last_month)
    if temp:
        file_name, last_num = os.listdir(date_dir)[-1].split('_')
    #지난달 디렉터리가 있는지 확인
    elif os.path.isdir(temp2):
        temp2_list = os.listdir(temp2)
        file_name, last_num = temp2_list[-1].split('_')

    else: #지난달 디렉터리 정보도 없을 경우 input()값을 받음
        print("UniTrainSet_ 디렉터리 생산 도중 문제가 생겼습니다.")
        print("UniTrainSet_ 마지막 으로 몇번 디렉터리를 생성했는지 입력해주세요.")
        last_num = input()
        file_name = 'UniTrainSet'
    temp2 = int(last_num) + 1
    new_num = str(temp2)
    global uniTrainSet_dir_path
    global uniTrainSet_cvatxmls_path, uniTrainSet_documents_path
    global uniTrainSet_notpure_path, uniTrainSet_pure_path
    global uniTrainSet_xmls_path
    uniTrainSet_dir_path = os.path.join(date_dir,'%s_%s'%(file_name, new_num))
    try:
        os.mkdir(uniTrainSet_dir_path)
        print("%s_%s 디렉터리 생성 완료" % (file_name, new_num))
    except:
        print("%s 디렉터리 생성 실패" % uniTrainSet_dir_path)

    uniTrainSet_cvatxmls_path = os.path.join(uniTrainSet_dir_path, 'cvatxmls')
    uniTrainSet_documents_path = os.path.join(uniTrainSet_dir_path, 'documnets')
    uniTrainSet_notpure_path = os.path.join(uniTrainSet_dir_path, 'notpure')
    uniTrainSet_pure_path = os.path.join(uniTrainSet_dir_path, 'pure')
    uniTrainSet_xmls_path = os.path.join(uniTrainSet_dir_path, 'xmls')
    try:
        os.mkdir(uniTrainSet_cvatxmls_path)
        os.mkdir(uniTrainSet_documents_path)
        os.mkdir(uniTrainSet_notpure_path)
        os.mkdir(uniTrainSet_pure_path)
        os.mkdir(uniTrainSet_xmls_path)
        print("%s%s 디렉터리 하위 디렉터리 생성 완료" %(file_name, new_num))
    except:
        print("%s 하위 디렉터리 생성 실패" % uniTrainSet_dir_path)


def get_dir_download():
    download_dir = 'C:\\Users\\USER\\Downloads'
    temp = os.listdir(download_dir)
    for x in temp:
        try:
            file_name, file_type = x.split('.')
        except:
            pass #디렉터리나 확장자가 없는 파일의 경우
        if file_type == 'xml':
            xml_name_list.append(file_name)
            xml_path_list.append(os.path.join(download_dir, str(file_name+'.'+file_type)))

def set_xml_copy(): #다운로드 디렉터리에 있는 xml 파일들을 cvatxmls 디렉터리로 옮기는 작업 수행
    try:
        for x in xml_path_list:
            shutil.move(x, uniTrainSet_cvatxmls_path)
        for x in xml_name_list:
            uniTrainSet_cvatxmls_list.append(os.path.join(uniTrainSet_cvatxmls_path, x+'.xml'))
    except:
        print("Download에 xml 파일이 없음")
    print("xml 파일 작업 완료")

def create_xmls_dir():
    for x in xml_name_list:
        temp = os.path.join(uniTrainSet_xmls_path, x)
        os.mkdir(temp)
        uniTrainSet_xmls_list.append(temp)

def wirte_xmls():
    count = 0
    print("xml 분할 중")
    for x in uniTrainSet_cvatxmls_list:
        f = open(x, 'r')
        lines = ''
        while True:
            line = f.readline()
            if not line: break
            lines += line
        f.close()
        bs = BeautifulSoup(lines, 'lxml')
        for img in bs.find_all('image'):
            totalImageCount += 1
            pureCount = 0
            boxCount = 0
            inPerson = 0
            inCar = 0
            inOthers = 0
            pureInPerson = 0
            pureInCar = 0
            pureInOthers = 0
            personBoxCountForBoth = 0
            carBoxCountForBoth = 0
            purePersonCountForBoth = 0
            pureCarCountForBoth = 0

            name = img.get("name")
            width = img.get("width")
            height = img.get("height")
            test = bs.find_all("image", class_ = name)
            label_list = []
            xtl_list = []
            ytl_list = []
            xbr_list = []
            ybr_list = []
            for box in img.find_all('box'):
                totalBoxCount += 1
                label_temp = box.get("label")

                if label_temp == 'person':
                    totalPersonBoxCount += 1
                elif label_temp in cars:
                    totalCarBoxCount += 1

                label_list.append(label_temp)
                xtl_list.append(box.get("xtl"))
                ytl_list.append(box.get("ytl"))
                xbr_list.append(box.get("xbr"))
                ybr_list.append(box.get("ybr"))
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

            tree = ElementTree(root)
            filename, temp = name.split('.')
            temp = os.path.join(uniTrainSet_xmls_list[count], filename+'.xml')
            tree.write(temp)
        print("%s 분할 완료 " % uniTrainSet_xmls_list[count])
        print
        count += 1

if __name__ == '__main__':

    get_date()
    get_dir_path()
    set_dir_dataSets()
    get_dir_download()
    set_xml_copy()
    create_xmls_dir()
    wirte_xmls()