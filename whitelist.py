#! /usr/bin/env python

__author__ = 'jjiang'

import sys
import os
import logging
import pyshark as ps
import re
import tldextract as tex

logging.basicConfig()

pcap_regex = '.+(.pcap)'
directory = ''
new_domains = 0

def get_tld(full_domain):
    return tex.extract(full_domain).registered_domain

def scan_packet(pathname, whitelist_output, domains):
    global new_domains
    pcap = ps.FileCapture(pathname, display_filter="http")
    for packet in pcap:
        try:
            host = packet.http.host.rstrip()
        except AttributeError:
            pass
        host = get_tld(host)
        if host not in domains:
            new_domains += 1
            domains.add(host)
            whitelist_output.write(''.join([host, '\n']))


def verify():
    global directory
    # check for path as argument
    if len(sys.argv) < 2:
        print('Please specify the directory of the .pcap files')
        sys.exit(-1)
    elif len(sys.argv) > 2:
        print('Please specify only the directory of the .pcap files')
        sys.exit(-1)
    else:
        namefile = sys.argv[1]

    if not os.path.isabs(namefile):
        namefile = os.path.abspath(namefile)
        print(namefile)
    if not os.path.isfile(namefile):
        print(namefile)
        print('File is invalid.')
        sys.exit(-1)

def make_whitelist(pcap_list, size):
    # only deal with .pcap's and create list of whitelisted domains
    # (predicated upon the fact that all captures are from known benign apps)
    whitelist_output = open('whitelist.txt', 'a+')

    # populate set with current entries
    whitelist_output.seek(0)

    current_list = whitelist_output.read().split()
    domains = set(current_list)
    count = 0
    print('Sanitizing directory list to exclude non-.pcap files and constructing whitelist...')
    for pcap_name in pcap_list:
        regex_match = re.match(pcap_regex, pcap_name)
        if regex_match:
            pathname = ''.join([directory, '/', pcap_name])
            scan_packet(pathname, whitelist_output, domains)
            count += 1
            if size%1 == 0:
                print(str(count) + '/' + str(size) + ' processed.')
    print(str(size-count) + ' non-pcap file(s)')

    whitelist_output = open('whitelist.txt', 'r')
    length = len(whitelist_output.readlines())

    # save list
    whitelist_output.close()

    print(''.join(['Whitelist contains ', str(length), ' domains.']))
    print(''.join([str(new_domains), ' new domains added.']))

def main():
    verify()
    # get list of all files in directory
    pcap_list = os.listdir(directory)
    size = len(pcap_list)
    if size == 0:
        print('Directory is empty.')
        sys.exit(-1)

    make_whitelist(pcap_list, size)

if __name__ == "__main__":
    main()
