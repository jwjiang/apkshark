#! /usr/bin/env python3

__author__ = 'jjiang'

import sys
import os
import stat
import time
import signal
import subprocess
from subprocess import PIPE, Popen

def find_names(apkname, namefile):
    name = subprocess.check_output('./package_name.sh ' + apkname, shell=True, universal_newlines=True)
    namefile.write(apkname + ',' + name)

# make script file executable
st = os.stat('package_name.sh')
os.chmod('package_name.sh', st.st_mode | stat.S_IEXEC)

# check for path as argument
if len(sys.argv) < 2:
    print("Please specify only the directory of the .apk files")
    sys.exit(-1)
else:
    directory = sys.argv[1]

# prompt if directory is correct / continue
do_continue = ''
while do_continue != 'y' and do_continue != 'n':
    do_continue = input('The specified directory is ' + directory + '. Continue? [y/n]')
if do_continue == 'n':
    sys.exit()

# validate directory
if not os.path.isabs(directory):
    directory = os.path.abspath(directory)
if not os.path.isdir(directory):
    print('Path is invalid.')
    sys.exit(-1)

# get list of all files in directory
apk_list = os.listdir(directory)
size = len(apk_list)
if size == 0:
    print('Directory is empty.')
    sys.exit(-1)

# only deal with .apk's and create list of package names
package_output = open('package_table.csv', 'a')
count = 0
print('Sanitizing directory list to exclude non-.apk files and constructing table of package names...')
for apk_name in apk_list:
    if apk_name[len(apk_name)-4:] != '.apk':
        apk_list.remove(apk_name)
    else:
        find_names(apk_name, package_output)
        count += 1
        if size%1 == 0:
            print(str(count) + '/' + str(size) + ' processed.')
print(str(size-count) + ' non-apk files')
# save list
package_output.close()

