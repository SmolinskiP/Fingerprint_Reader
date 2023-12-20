import paramiko

def SSH_Connect():

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.10.1", username="wakeonlan", password="81d7a5c58", port=4224)
    return ssh
    
def WakeComputer(card_id, mac_addr, ssh):
    
    cmd_to_execute = "sudo etherwake -i enp3s0f0 " + mac_addr
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
        
    if card_id == "0004293363" or card_id == "0003472198":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 88:51:FB:67:91:55")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 20:47:47:B5:00:C3")
    if card_id == "0004365562" or card_id == "0002002502" or card_id == "0004388356" or card_id == "0004427606" or card_id == "0004336582" or card_id == "0004176737" or card_id == "0002001285" or card_id == "0004328792" or card_id == "0004405307":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:6A:49:96")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:AE:69:4D")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:A3:8C:D9")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 B8:27:EB:A2:31:4F")
