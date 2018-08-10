#!/usr/bin/env python3

import json
from urllib.request import urlopen
import time

import colorama
colorama.init()
#start = "\033[1;31m"
#end = "\033[0;0m"
green = colorama.Fore.GREEN
red = colorama.Fore.RED
blue = colorama.Fore.BLUE
cyan = colorama.Fore.CYAN
bright = colorama.Style.BRIGHT
end = colorama.Style.RESET_ALL

d = {}
with open('IPs.txt') as f:
    for line in f:
        (key, val) = line.split()
        d[int(key)] = val

d_enabled = {}
d_expired = {}
last_paid = {}
#late_payment = {}
listed_count = 0
total_count = len(d)
with urlopen('http://api-aegeus.mn.zone/masternodes') as r:
    result = json.loads(r.read().decode(r.headers.get_content_charset('utf-8')))
    api_ip_list = result['nodes']
    for node in api_ip_list:
        for key, value in d.items():
            if value in node.get('ip'):
                if node.get('status') == 'ENABLED':
                    d_enabled[key] = value
                    last_paid[key] = node.get('last_paid')
                    listed_count += 1
                elif node.get('status') == 'EXPIRED':
                    d_expired[key] = value
                    last_paid[key] = node.get('last_paid')
                    listed_count += 1

for key, value in sorted(last_paid.items()):
    if (time.time() - 86400) <= value:
        #late_payment[key] = False
        last_paid[key] = time.strftime("{0}%Y-%m-%d %I:%M:%S%p{1}".format(green, end), time.localtime(value))
    elif(time.time() - 86400) >= value:
        #late_payment[key] = True
        if value != 0:
            last_paid[key] = time.strftime("{0}%Y-%m-%d %I:%M:%S%p{1}".format(red, end), time.localtime(value))
        elif value == 0:
            last_paid[key] = "{0}Never Paid{1}".format(red, end)

for key, value in sorted(d_enabled.items()):
    print("{0}MN{1}:{2} {3} {4}{5}ENABLED{6}".format(cyan, str(key), end, value, bright, green, end))
    print("{0}MN{1}{2} Last Payment: {3}".format(cyan, str(key), end, last_paid[key]))
    print("{0}========================================{1}".format(blue, end))

for key, value in sorted(d_expired.items()):
    print("{0}MN{1}:{2} {3} {4}{5}EXPIRED{6}".format(cyan, str(key), end, value, bright, red, end))
    print("{0}MN{1}{2} Last Payment: {3}".format(cyan, str(key), end, last_paid[key]))
    print("{0}========================================{1}".format(blue, end))

print("Total listed nodes: {0}".format(listed_count))
print("Total owned nodes: {0}".format(total_count))
