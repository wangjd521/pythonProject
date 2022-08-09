import pandas as pd

def get_interface_number(x):
    return x.rsplit("-", 1)[-1]

def get_switch_name(x):
    return x.rsplit("-", 1)[0]

data = pd.read_excel('./switch_interface_vlan_mapping_template.xlsx')

data["Port"] = data["Switch"].map(get_interface_number)

data["Switch"] = data["Switch"].map(get_switch_name)

group = data.groupby('Switch')

config_file_name = "config.txt"

with open(config_file_name, "a") as f:
    for x, y in group:
        device_name = x
        f.write("devices device " + device_name + "\n")
        f.write("config" + "\n")
        for i in y.index:
            interface_number = "interface FastEthernet0/" + str(y["Port"][i]) + "\n"
            vlan_number = "switchport access vlan " + str(y["Vlan"][i]) + "\n"
            no_shutdown = "no shutdown" + "\n"
            f.write(interface_number)
            f.write(vlan_number)
            f.write(no_shutdown)

'''
通过Excel生产交换机VLAN配置
'''