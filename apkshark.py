#! /usr/bin/env python

__author__ = 'jjiang'

import sys
import os
import time
import re
import subprocess
from subprocess import PIPE, Popen

apk_regex = '.+(.apk)'

def find_names(apkname, namefile):
    name = subprocess.check_output('./package_name.sh ' + apkname, shell=True, universal_newlines=True)
    namefile.write(''.join([apkname, ',', name]))

# more modular - can insert location of aapt
def find_names2(pathname, apkname, namefile):
    p = subprocess.Popen('echo `/usr/share/android-sdk/sdk/build-tools/android-4.4W/aapt dump badging ' + pathname +
                         ' | grep package | awk \'{print $2}\' | sed s/name=//g | sed s/\\\'//g`', shell=True,
                         stdout=PIPE, universal_newlines=True)
    name = p.communicate()[0]
    namefile.write(''.join([apkname, ',', name]))

start_time = time.time()

# check for path as argument
if len(sys.argv) < 2:
    print('Please specify the directory of the .apk files')
    sys.exit(-1)
elif len(sys.argv) > 2:
    print('Please specify only the directory of the .apk files')
    sys.exit(-1)
else:
    directory = sys.argv[1]

# prompt if directory is correct / continue
do_continue = ''
while do_continue != 'y' and do_continue != 'n':
    do_continue = raw_input('The specified directory is ' + directory + '. Continue? [y/n]')
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
    regex_match = re.match(apk_regex, apk_name)
    if regex_match:
        pathname = ''.join([directory, '/', apk_name])
        find_names2(pathname, apk_name, package_output)
        count += 1
        if size%1 == 0:
            print(str(count) + '/' + str(size) + ' processed.')
print(str(size-count) + ' non-apk file(s)')
# save list
package_output.close()

print("--- %s seconds ---" % (time.time() - start_time))

