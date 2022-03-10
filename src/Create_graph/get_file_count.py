import os
from os import listdir
from os.path import isfile, join

root_path = 'D:\신지영_업무\\0709_어트리뷰트인수인계\\attribute_images'

dir_list = os.listdir(root_path)

for dir_name in dir_list:
    file_count = 0
    dir_path = os.path.join(root_path, dir_name)
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        if file_name.endswith('png') or file_name.endswith('jpg'):
            file_count += 1

    print("%s 디렉터리 내부 파일 개수 = %d" % (dir_name, file_count))