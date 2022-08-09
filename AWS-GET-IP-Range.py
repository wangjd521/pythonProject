import requests
import json

proxies = {
    'http': 'http://58.2.216.67:80',
    'https': 'http://58.2.216.67:80'

}

slash_to_mask = (
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.248.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
)

ip_ranges = requests.get(url='https://ip-ranges.amazonaws.com/ip-ranges.json', proxies=proxies).json()[
    'prefixes']

aws_ip_list = []

for item in ip_ranges:
    aws_ip_list.append(item['ip_prefix'])

with open('acl.txt', 'a', encoding='gbk') as f:
    for item in aws_ip_list:
        prefix = item.rsplit('/', 1)[0]
        mask = item.rsplit('/', 1)[-1]
        f.write("permit ip any {0} {1}\n".format(prefix, slash_to_mask[int(mask)]))
