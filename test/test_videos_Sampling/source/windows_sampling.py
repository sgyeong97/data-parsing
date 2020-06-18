#OpenCV 모듈 참조
import cv2

#파일, 디렉터리를 다루기 위해 참조
import os
import sys
from os import listdir
from os.path import isfile, join
#한글 경로 문제 발생 해결을 위해 참조
import numpy as np

#img 파일명 저장 리스트 초기화
file_name = []
#파일 경로를 저장하는 전역변수 리스트 초기화
mp4_path = []
img_path = []
#디렉터리 절대 주소 값을 넣을 변수 초기화
imgDir = ''
mp4Dir = ''

#디렉터리와 파일 정보를 얻어오는 모듈
def get_fileList():
    #전역변수값 수정을 위해 globar 선언
    global mp4Dir, imgDir
    #temp에 현재 코드가 들어있는 디렉터리의 절대경로 정보가 들어가있음
    temp = os.getcwd()
    #프로젝트 root directory 경로를 root_dir에 저장
    root_dir = os.path.dirname((temp))
    #root_dir 내부 디렉터리 리스트를 temp에 저장
    temp = os.listdir(root_dir)
    for x in temp:
        #Video 디렉터리가 있어야함
        if x == 'Video':
            #Video 디렉터리 내부에 있는 파일들을 리스트화 해서 temp_path에 저장
            temp_path = os.path.join(root_dir, x)
            mp4Dir = temp_path
            temp_path = os.listdir(temp_path)
            for y in temp_path:
                #파일들 중 mp4 확장자 파일만 file_name 리스트에 저장
                #mp4_path에는 mp4 확장자 파일들의 절대 주소를 저장
                filename, z = y.split('.')
                if z == 'mp4':
                    file_name.append(filename)
                    mp4_path.append(os.path.join(root_dir, x, y))
        #Image 디렉터리 절대 주소를 imgDir에 저장
        elif x == 'Image':
            imgDir = os.path.join(root_dir, x)

def sampling():

    #영상별 img추가를 위한 디렉터리 생성 처리
    for x in range(0, len(file_name)):
        #디렉터리가 있는 경우에만 생성, 없으면 아무 동작 안함
        temp = os.path.join(imgDir,file_name[x])
        if not(os.path.exists(temp)):
            print("%s 디렉터리 생성" % temp)
            os.mkdir(temp)
            #생성한 img디렉터리 절대 주소를 img_path 리스트에 추가

        img_path.append(temp)

    for x in range(0, len(file_name)):
        #동영상 파일을 지정하여 VideoCapture 객체를 vidcap으로 정의
        vidcap = cv2.VideoCapture(mp4_path[x])
        count = ret = 1

        while ret:
            #ret = bool 요소로 사용
            #image = numpy 클래스 타입
            #image속에 동영상의 이미지 정보가 배열 형식으로 저장
            ret, image = vidcap.read()

            #sampling image를 150장으로 맞추는 구문
            frameId = int(round(vidcap.get(1)))
            length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            multiplier = length/150
            #count<151로 overflow시도 방지

            if frameId % multiplier <= 1 and count < 151:
                str_count = "{0:03d}".format(count)
                temp = os.path.join(img_path[x], file_name[x]+'_'+str_count+'.jpg')

                #한글 경로 문제 해결 구문
                ext = os.path.splitext(temp)[1]
                result, n = cv2.imencode(ext, image, None)
                if result:
                #Jpg 이미지 생성 구문
                    with open(temp, mode="w+b") as f:
                        n.tofile(f)
                count += 1

        print("%s 영상 이미지 %s개 생성" % (file_name[x], count-1))

        #이미지 원본 영상관련 txt 파일 생성 구문
        txt_path = os.path.join(img_path[x], file_name[x]+'.txt')
        print("%s.txt 생성" % (file_name[x]))

        writefile = open(txt_path, 'w')
        writefile.write(("""<INFO>
file_name = %s
file_path = %s""")%(file_name[x], mp4_path[x]))

        #종료
        writefile.close()
        vidcap.release()

#이 코드를 메인으로 돌릴 경우 실행하는 코드
if __name__ == '__main__':
    #get_fileList 모듈 실행
    get_fileList()
    sampling()