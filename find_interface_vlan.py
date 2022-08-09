import re

with open('switch-interface-vlan.txt', 'r') as f:
    data = f.read()

re_pattern_switch_interface_with_vlan = r'(interface.*/\d{1,2})\n.*?(switchport access vlan 82)\n'

re_pattern_all_switch_data = r'(devices device.*?CHN-DLN.*?\d{1,2})#'

re_pattern_switch_name = r'devices device (CHN-DLN-GSD-ACC-SW-\d{1,3}F\d{1,3}) live-status exec'

all_switch_data = re.findall(re_pattern_all_switch_data, data, re.DOTALL)

for i in all_switch_data:

    switch_name = re.findall(re_pattern_switch_name, i)

    switch_interface_with_vlan = re.findall(re_pattern_switch_interface_with_vlan, i)

    if len(switch_interface_with_vlan) != 0:

        with open(switch_name[0] + '.txt', 'w') as f:

            for j in switch_interface_with_vlan:

                f.write(j[0] + '\n')

                f.write('no ' + j[1] + '\n')

    else:

        continue














