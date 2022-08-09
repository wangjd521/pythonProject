import re

with open('switch-voice-vlan.txt', 'r') as f:
    test = f.read()

re_pattern_switch_interface_with_mode_access = r'(interface.*/\d{1,2})\n.*?(switchport mode access)\n'

re_pattern_switch_interface_with_voice_vlan = r'(interface.*/\d{1,2})\n.*?(switchport mode access)\n.*?(switchport voice vlan \d{1,3})\n'

re_pattern_switch_data = r'(devices device.*?CHN-DLN.*?\d{1,2})#'

re_pattern_switch_name = r'devices device (CHN-DLN-GSD-ACC-SW-\d{1,3}F\d{1,3}) live-status exec'

list_switch_data = re.findall(re_pattern_switch_data, test, re.DOTALL)

for i in list_switch_data:

    list_interface_need_with_voice_vlan = []

    list_interface_with_mode_access = re.findall(re_pattern_switch_interface_with_mode_access, i)

    list_interface_with_voice_vlan = re.findall(re_pattern_switch_interface_with_voice_vlan, i)

    switch_name = re.findall(re_pattern_switch_name, i)

    for j in list_interface_with_mode_access:

        flag = 0

        for k in list_interface_with_voice_vlan:

            if j[0] == k[0]:
                flag += 1

        if flag == 0:

            list_interface_need_with_voice_vlan.append(j[0])

    if len(list_interface_need_with_voice_vlan) != 0:

        with open(switch_name[0], 'w') as f:

            for m in list_interface_need_with_voice_vlan:
                f.write(m + '\n')
                f.write('switchport voice vlan 74\n')
    else:
        print(switch_name[0] + ' has been configured all interface with voice vlan')
