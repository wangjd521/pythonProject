#!/usr/bin/python

import pandas as pd
import sys
import os
import shutil

def get_interface_number(x):
    return x.rsplit("-", 1)[-1]

def get_switch_name(x):
    return x.rsplit("-", 1)[0]

data = pd.read_csv(sys.argv[1])

data["Port"] = data["Switch"].map(get_interface_number)

data["Switch"] = data["Switch"].map(get_switch_name)

group = data.groupby('Switch')

config_folder_name = sys.argv[1].rsplit(".",1)[0]

if not os.path.exists(config_folder_name):
    os.mkdir("./"+config_folder_name)
else:
    shutil.rmtree(config_folder_name)
    os.mkdir("./"+config_folder_name)

os.chdir(config_folder_name)

for x, y in group:

    config_file_name = x + ".txt"
    with open(config_file_name, "a") as f:
        for i in y.index:
            interface_number = "interface fa0/" + str(y["Port"][i]) + "\n"
            vlan_number = "switch access vlan " + str(y["Vlan"][i]) + "\n"
            no_shutdown = "no shutdown" + "\n"
            f.write(interface_number)
            f.write(vlan_number)
            f.write(no_shutdown)