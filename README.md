# fun-with-python
scripts using python and android tools to automate collection of packet dumps collected with tcpdump in a sandboxed emulator environment.

apkshark.py:
-----------
Searches for .apk files in a given directory and constructs a .csv consisting of the apk files' names and their package names (necessary for launching an app via adb).

Instructions:
Edit line 20 of apkshark.py to include the correct location of aapt from the Android SDK build tools.
Easiest way to use these scripts is to have all the .apk's and the scripts in the same directory.

Run apkshark.py using '.' as the directory argument (assuming apk's are in the same directory).

monkey.py:
----------
Performs a set of actions on an AVD for each .apk:
   - Install the .apk
   - Start tcpdump to capture packets
   - Launch the app using monkey and wait some time for packets to be captured
   - Kill tcpdump and pull the .pcap file off the AVD
   - Uninstall the .apk

Instructions:
Install pexpect from https://pexpect.readthedocs.org/en/latest/install.html.
Edit line 101 of monkey.py to have the correct name of the AVD you will use. For example, if you have an AVD called 'testavd1', the line should be changed to include '-avd testavd1' (the rest should remain unchanged).

You can change the time to let the app run before killing it (and tcpdump) in line 63 of monkey.py.
Then run monkey.py with 'package_table.csv' (output of apkshark.py) as the argument.

whitelist.py:
-------------
Creates a whitelist of safe TLDs given a directory of packet captures from apps known to be non-malicious.

Instructions:
Install pyshark and tldextract (both available on pip).
Run with the path of a directory of .pcap files as the sole command-line argument. Outputs results to a file called 'whitelist.txt'.

permissions.py:
---------------
Generates a list of all the permissions required by a given .apk.


readme updated: 29 june 2015
