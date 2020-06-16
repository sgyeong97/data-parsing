import exifread
import sys
import cv2
import os
import numpy as np #필요없음
from os import listdir
from os.path import isfile, join

file_name = []
mp4_path = []
img_path = []

rootDir = '../'
imgDir = '../Image'

file_max = 0
file_type = '.mp4'

def get_filelist():
    try:
        files = [f for f in listdir(rootDir) if isfile(join(rootDir, f))]
    except:
        print("Directory file is gone")
        print("EXIT")
        sys.exit()

    for item in files:
        if item.find(file_type) != -1:
            filename, temp = item.split('.')
            file_name.append(filename)

            mp4_path.append(rootDir+filename+file_type)
            img_path.append(imgDir+filename)
        else:
            pass
    print(file_name)

    file_max = len(file_name)
    if file_max == 0:
        print("mp4 file is gone")
        print("EXIT")
        sys.exit()
    return file_max

def sampling():
    dir_path = []
    for x in range(0, file_max): #디렉토리 생성
        dir_name = "Databaset_{0:=06d}".format(x+1)
        if not (os.path.isdir("../Image/%s" % dir_name)):
            print("%s 디렉토리 생성" % dir_name)
            os.system("mkdir ../Image/%s" % dir_name)
            dir_path.append(dir_name)
        else:
            print("디렉토리 중복 발생")
    try: 
        for x in range(0, file_max): #실질적인 이미지 추출
            vidcap = cv2.VideoCapture("../%s.mp4" %(file_name[x]))
            count = 1
            seconds = 0.2
            ret = 1

            fps = vidcap.get(cv2.CAP_PROP_FPS)
            multiplier = fps * seconds
            while ret:
                ret, image = vidcap.read()
                frameId = int(round(vidcap.get(1)))
                if frameId % multiplier < 1:
                    str_count = "{0:05d}".format(count)
                    str_filename = "Databaset_{0:=06d}".format(x+1)
                    cv2.imwrite("../Image/%s/%s_%s.jpg" % (dir_path[x],str_filename, str_count), image)
                    print("../Image/%s/%s_%s.jpg 생성" % (dir_path[x], str_filename, str_count))
                    count += 1

            txt_path = '../Image/%s/%s' % (dir_path[x], (dir_path[x]+'.txt'))
        
            writefile = open(txt_path, 'w')
            writefile.write(("""<Info>
file_name = %s
file_path = %s
""" % (file_name[x], dir_path[x])))
            writefile.close()
            print("sampling end")
            vidcap.release()
    except:
       print("Sampling end")

if __name__ == '__main__':
    file_max = get_filelist()
    sampling()
