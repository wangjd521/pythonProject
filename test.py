import paramiko

server_connect = paramiko.Transport(("58.2.216.212", 22))

server_connect.connect(username="root", password="19870424")

ssh = paramiko.SSHClient()
ssh._transport = server_connect

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(r"ls -l /")

print(ssh_stdout.read().decode())

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(r"df -h")

print(ssh_stdout.read().decode())

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(r"ncs_cli -C -u admin")

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(r"pwd")

print(ssh_stdout.read().decode())

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(r"devices device CHN-DLN-GSD-ACC-SW-07F* check-sync")

print(ssh_stdout.read().decode())

ssh.close()

#devices device CHN-DLN-GSD-ACC-SW-07F* check-sync