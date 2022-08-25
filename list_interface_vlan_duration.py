import paramiko
import datetime
import re
import pandas as pd
import os
import time

cmd_list = ('ncs_cli -C -u admin', 'devices device CHN-DLN-GSD-ACC-SW-09F* live-status exec any show interfaces \| in line\|Last input', 'devices device CHN-DLN-GSD-ACC-SW-09F* live-status exec any show run \| in interface\|access vlan')


def list_interface_vlan_duration(var_path):

    os.chdir(var_path)

    with open('interface_duration_file.txt', 'r') as f:
        data_interface_duration = f.read()

    with open('interface_vlan_file.txt', 'r') as f:
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

    final_data = pd.merge(final_data_interface_duration, final_data_interface_vlan, how='left',
                          left_on=['Switch Name', 'Interface No'], right_on=['Switch Name', 'Interface No'])

    final_data.fillna('Na', inplace=True)

    final_data.to_excel('list_interface_vlan_duration.xlsx', index=False)

    return final_data


def run_command_on_nso(var_list):

    config_folder = str(datetime.datetime.now())
    config_folder = config_folder.replace(" ", "-")
    config_folder = config_folder.replace(":", "-")
    config_folder = config_folder.replace(".", "-")
    os.mkdir(config_folder)
    os.chdir(config_folder)
    print(os.getcwd())
    cmd_count = 0
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="58.2.216.212", port=22, username="root", password="19870424")
    ssh_channel = ssh_client.invoke_shell()
    ssh_channel.settimeout(1000)
    time.sleep(2)

    for cmd in var_list:

        if cmd_count == 0:
            ssh_buffer = ''
            ssh_receive = ''
            while not ssh_buffer.endswith('# '):
                ssh_receive = ssh_channel.recv(1024).decode('utf-8')
                ssh_buffer += ssh_receive
            print(ssh_buffer, end='')

        ssh_buffer = ''
        ssh_receive = ''
        ssh_channel.send(cmd + '\n')
        while not ssh_buffer.endswith('# '):
            ssh_receive = ssh_channel.recv(1024).decode('utf-8').replace('\r', '')
            ssh_buffer += ssh_receive
        print(ssh_buffer, end='')
        cmd_count += 1

        if cmd_count == 2:
            with open('interface_duration_file.txt', 'w') as f:
                f.write(ssh_buffer)

        if cmd_count == 3:
            with open('interface_vlan_file.txt', 'w') as f:
                f.write(ssh_buffer)

    ssh_channel.close()
    ssh_client.close()

    return os.getcwd()


if __name__ == "__main__":

    config_path = run_command_on_nso(cmd_list)

    list_interface_vlan_duration(config_path)