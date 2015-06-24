# fun-with-python
random scripts working with python and android sdk tools

apkshark.py:
Searches for .apk files in a given directory and constructs a .csv consisting of the apk files' names and their package names (necessary for launching an app via adb).

monkey.py:
Performs a set of actions on an AVD for each .apk:
   - Install the .apk
   - Start tcpdump to capture packets
   - Launch the app using monkey and wait some time for packets to be captured
   - Kill tcpdump and pull the .pcap file off the AVD
   - Uninstall the .apk

Instructions:

Install pexpect from https://pexpect.readthedocs.org/en/latest/install.html. It's required for automating communication with adb.

Edit line 20 of apkshark.py to include the correct location of aapt from the Android SDK build tools.

Easiest way to use these scripts is to have all the .apk's and the scripts in the same directory. First run apkshark.py using '.' as the directory argument (assumign apk's are in the same directory). Then run monkey.py with 'package_table.csv' as the argument.

You can change the time to let the app run before killing it (and tcpdump) in line 63 of monkey.py.
