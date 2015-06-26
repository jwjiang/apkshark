#! /usr/bin/env python

__author__ = 'jjiang'

import sys
import os
import pexpect

suspicious_permissions = set(['android.permission.INTERNET', 'android.permission.ACCESS_NETWORK_STATE',
                              'android.permission.CHANGE_NETWORK_STATE',
                              'android.permission.SEND_SMS', 'android.permission.READ_SMS',
                              'android.permission.INSTALL_PACKAGES', 'android.permission.KILL_BACKGROUND_PROCESSES',
                              'android.permission.DOWNLOAD_WITHOUT_NOTIFICATION'])

def verify(namefile=None):
    if namefile is None:
        # check for path as command-line argument
        if len(sys.argv) < 2:
            print('Please specify the location of the .apk file')
            sys.exit(-1)
        elif len(sys.argv) > 2:
            print('Please specify only the location of the .apk file')
            sys.exit(-1)
        else:
            namefile = sys.argv[1]

        # verify the file exists
        if not os.path.isabs(namefile):
            namefile = os.path.abspath(namefile)
            print(namefile)
        if not os.path.isfile(namefile):
            print(namefile)
            print('File is invalid.')
            sys.exit(-1)

        # get permissions using aapt
        get_permissions(namefile)

    else:
        # verify path function argument
        if not os.path.isabs(namefile):
            namefile = os.path.abspath(namefile)
            print(namefile)
        if not os.path.isfile(namefile):
            print(namefile)
            print('File is invalid.')
            sys.exit(-1)
        return namefile

def get_permissions(apkname):
    command = ''.join(['aapt d permissions ', apkname])
    shell = pexpect.spawn(command)
    permissions = shell.readlines()
    for i,string in enumerate(permissions):
        string = string.rstrip()
        length = len(string)
        if 'uses-permission' in string:
            string = string[string.index("'")+1:length-1]
            permissions[i] = string
        elif 'permission' in string:
            string = string[string.index(' ')+1:length]
            permissions[i] = string
        else:
            pass
    return permissions[1:]

# returns true if has permissions that COULD be used maliciously, false if no suspicious permissions
def check_malicious(apkname):
    result = verify(namefile=apkname)
    permissions = get_permissions(result)
    for item in suspicious_permissions:
        if item in permissions:
            return True
    return False

def main():
    verify()

if __name__ == "__main__":
    main()
