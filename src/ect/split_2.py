import os
import sys
from os import listdir
from os.path import join

root_dir = 'D:\신지영_업무\dataset\\0625_번호판\LPdataTest0629'
target_root = 'D:\신지영_업무\dataset\\0625_번호판\LPdataTest0629\lp만분류'
temp_list = os.listdir(root_dir)
file_name_list = []

for x in temp_list:
    if x.endswith('txt'):
        file_name, type = x.split('.')
        file_name_list.append(file_name)

for x in file_name_list:
    temp = os.path.join(root_dir, x+'.txt')
    f = open(temp, 'r')
    contants = ''
    while True:
        line = f.readline()
        if not line: break
        if line.startswith('3'):
            contants += line
        else:
            pass
    f.close()
    temp2 = os.path.join(target_root, x+'.txt')
    if not contants: break
    else:
        file = open(temp2, 'w')
        file.write(contants)
        file.close()