import pandas as pd
import os
import datetime
import paramiko


def get_interface_number(x):
    return x.rsplit("-", 1)[-1]


def get_switch_name(x):
    return x.rsplit("-", 1)[0]


def generate_configuration(excel_path):
    data = pd.read_excel(excel_path)

    data["Port"] = data["Switch"].map(get_interface_number)

    data["Switch"] = data["Switch"].map(get_switch_name)

    group = data.groupby('Switch')

    config_folder_path = str(datetime.datetime.now())

    config_folder_path = config_folder_path.replace(" ", "-")

    config_folder_path = config_folder_path.replace(":", "-")

    config_folder_path = config_folder_path.replace(".", "-")

    os.mkdir(config_folder_path)

    os.chdir(config_folder_path)

    for x, y in group:
        config_file_name = x + ".txt"
        with open(config_file_name, "a") as f:
            for i in y.index:
                interface_number = "interface FastEthernet0/" + str(y["Port"][i]) + "\n"
                vlan_number = "switchport access vlan " + str(y["Vlan"][i]) + "\n"
                no_shutdown = "no shutdown" + "\n"
                f.write(interface_number)
                f.write(vlan_number)
                f.write(no_shutdown)
        with open("load_command.txt", "a") as f:
            f.write(
                r"devices device " + x + r" load-native-config file " + r"/" + config_folder_path + r"/" + x + ".txt\n")

    os.chdir(os.path.pardir)

    return config_folder_path


def upload_file(host, port, user, passwd, folder_name):

    server_connect = paramiko.Transport((host, port))

    server_connect.connect(username=user, password=passwd)

    scp = paramiko.SFTPClient.from_transport(server_connect)

    for root, folder, files in os.walk(folder_name):
        scp.mkdir(r"/" + root)
        os.chdir(root)
        for i in files:
            scp.put(i, r"/" + root + r"/" + i)


if __name__ == "__main__":

    file_name = generate_configuration('./switch_interface_vlan_mapping_template.xlsx')

    upload_file("58.2.216.212", 22, "root", "19870424", file_name)
