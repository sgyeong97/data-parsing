import cv2
import os
import sys
import shutil
from os import listdir
from os.path import join, isfile

dir_path = 'D:\신지영_업무\아산\sampling_완료_분류영상'
min_path = 'D:\신지영_업무\아산\sampling_완료_분류영상\\1min'
sec_path = 'D:\신지영_업무\아산\sampling_완료_분류영상\\30sec'
garbage_path = 'D:\신지영_업무\아산\sampling_완료_분류영상기준미달'
dir_list = os.listdir(dir_path)

for x in dir_list:
    if x.endswith('avi'):
        file_path = os.path.join(dir_path, x)
        vidcap = cv2.VideoCapture(file_path)
        count = ret = 1
        while ret:
            ret, image = vidcap.read()
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            frameId = round(vidcap.get(1))
            length = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
            vidcap.release()

            try:
                if length == 0:
                    shutil.move(file_path, os.path.join(garbage_path, x))
                    break
                else:
                    video_length = float((length/fps))
                if video_length >= 60 :
                    shutil.move(file_path, os.path.join(min_path,x))
                elif video_length >= 30 and video_length <= 31:
                    shutil.move(file_path, os.path.join(sec_path, x))
                else:
                    shutil.move(file_path, os.path.join(garbage_path, x))
            except:
                pass
    else:
        pass
