import re
import pandas as pd

with open('interface_duration.txt', 'r') as f:
    data_interface_duration = f.read()

with open('interface_vlan.txt', 'r') as f:
    data_interface_vlan = f.read()

re_pattern_all_switch_data = r'(devices device.*?CHN-DLN.*?\d{1,2})#'

re_pattern_switch_name = r'devices device (CHN-DLN-GSD-ACC-SW-\d{1,3}F\d{1,3}) live-status exec'

re_pattern_switch_interface_duration = r'(\w*?Ethernet(1/)?\d/\d{1,2}).*?\n.*?Last input (.*?),.*?\n'

re_pattern_switch_interface_vlan = r'(\w*?Ethernet(1/)?\d/\d{1,2}).*?\n.*?switchport access vlan (\d{1,4})\n'

all_switch_data_interface_duration = re.findall(re_pattern_all_switch_data, data_interface_duration, re.DOTALL)

all_switch_data_interface_vlan = re.findall(re_pattern_all_switch_data, data_interface_vlan, re.DOTALL)

output_interface_duration = []

output_interface_vlan = []

for i in all_switch_data_interface_duration:

    switch_name = re.findall(re_pattern_switch_name, i)

    switch_interface_duration = re.findall(re_pattern_switch_interface_duration, i)

    for k in switch_interface_duration:

        m = list(k)
        m.pop(1)
        m.insert(0, switch_name[0])

        output_interface_duration.append(m)

final_data_interface_duration = pd.DataFrame(output_interface_duration, columns=['Switch Name', 'Interface No', 'Duration'])

for i in all_switch_data_interface_vlan:

    switch_name = re.findall(re_pattern_switch_name, i)

    switch_interface_vlan = re.findall(re_pattern_switch_interface_vlan, i)

    for k in switch_interface_vlan:

        m = list(k)
        m.pop(1)
        m.insert(0, switch_name[0])

        output_interface_vlan.append(m)

final_data_interface_vlan = pd.DataFrame(output_interface_vlan, columns=['Switch Name', 'Interface No', 'Vlan No'])

final_data = pd.merge(final_data_interface_duration, final_data_interface_vlan, how='left', left_on=['Switch Name', 'Interface No'], right_on=['Switch Name', 'Interface No'])

final_data.fillna('Na', inplace=True)

final_data.to_excel('list_interface_vlan_duration.xlsx', index=False)

'''
devices authgroups group genpact-access-switch default-map remote-name USER remote-password PASS
devices device CHN-DLN-GSD-ACC-SW-07F* live-status exec any show interfaces \| in line\|Last input | save interface_duration.txt
devices device CHN-DLN-GSD-ACC-SW-07F* live-status exec any show run \| in interface\|access vlan | save interface_vlan.txt
'''