# fun-with-python
random scripts working with python and android sdk tools

apkshark v0.1.py:
Searches for .apk files in a given directory and constructs a .csv consisting of the apk files' names and their package names (necessary for launching an app via adb).

monkey.py:
Performs a set of actions on an AVD for each .apk:
   - Install the .apk
   - Start tcpdump to capture packets
   - Launch the app using monkey and wait some time for packets to be captured
   - Kill tcpdump and pull the .pcap file off the AVD
   - Uninstall the .apk
