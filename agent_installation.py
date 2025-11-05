import paramiko
import os
import time
# Create an SSH client instance
ssh = paramiko.SSHClient()

# Automatically add unknown host keys (optional but useful for automation)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#commands_vars
certs_path="/hzp"
TLS_portal="sudo kubectl get secret -n dapo tls-credential -o jsonpath=\"{.data.cacert}\" | base64 -d > /home/dell/orchestrator_ca.crt"
TLS_DAPO="sudo kubectl get secret -n dapp tls-credential -o jsonpath=\"{.data.cacert}\" | base64 -d > /home/dell/portal_ca.crt"
pod_name_cmd="sudo kubectl get pods -n dapo | grep fusion-mgmtworker | cut -d ' ' -f1"
agent_folder='mkdir -p /hzp/ece-agent'
pod_path='/home/dell/test.py'

#files_url
agent_file_url="https://isgedge.artifactory.cec.lab.emc.com/artifactory/isgedge-deb-virtual/pool/rel/dap-1.0.0.0/e/ece-agent/ece-agent_deb-dap-3.2.0.0-13776d9a-30_amd64.deb"
Ismrfutil_url="https://hopjpd.artifactory.cec.lab.emc.com:443/artifactory/isgedge-generic-virtual/hzp/ece/rfutil/rel/dap-1.0.0.0/3.2.0.0-f58b2d2-1/hzp-ece-rfutil"

#Dapo details
dapo_hostname='100.96.54.171'
dapo_ssh_port='22'
dapo_username='dell'
dapo_password='Sigsaly@123'

# ece-node details
node_hostname='100.98.68.25'
node_ssh_port='22'
node_username='root'
node_password='Dell'

remote_dapo_files = [
    "/home/dell/orchestrator_ca.crt",
    "/home/dell/portal_ca.crt"
]
local_files = [
    "orchestrator_ca.crt",
    "portal_ca.crt"
]
new_local_path='ece.conf'
new_remote_path="/home/dell/ece.conf"
remote_node_path = "/hzp/"
new_remote_node_path="/hzp/ece-agent/ece.conf"
modify_script = "modify_ece_conf.sh"
remote_modify_path = "/hzp/modify_ece_conf.sh"
CLIENT_ID = "e187a2ac-ffdd-43c2-994e-09131fb5a0c3"
CLIENT_SECRET = "8ZsybWbbzSIZnQREsUa3TuRycCEDEtoq2JR3++J5u0k="
ORG_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
download_script = "install_agent_files.sh"
remote_download_path = "/hzp/install_agent_files.sh"
additional_binaries_local_path="additional_binaries.sh"
additional_binaries_remote_path="/root/additional_binaries.sh"



try:
    ssh.connect(node_hostname, node_ssh_port, node_username, node_password)
    ssh.exec_command(agent_folder)

except Exception as e:
    print(f"Failed to connect to {node_hostname}: {e}")
ssh.close()

try:
    ssh.connect(dapo_hostname, dapo_ssh_port, dapo_username, dapo_password)
    sftp = ssh.open_sftp()
    local_path = "test.py"               # Local path on your machine
    remote_path = "/home/dell/test.py"   # Temporary location on DAPO server
    sftp.put(local_path, remote_path)
    print("test.py uploaded to DAPO")
    ssh.exec_command(TLS_portal)
    ssh.exec_command(TLS_DAPO)
    
    stdin, stdout, stderr = ssh.exec_command(pod_name_cmd)
    pod_name = stdout.read().decode().strip()
    if not pod_name:
        raise ValueError("Pod name not found!")
    print(f"Pod Name: {pod_name}")
    copy_test_py= f"sudo kubectl cp -n dapo  {pod_path} {pod_name}:/opt/test.py"
    stdin, stdout, stderr= ssh.exec_command(copy_test_py)
    stdin.close()
    stdout.close()
    stderr.close()
    gen_secret=f"bash -lc 'sudo kubectl exec -n dapo -i {pod_name} -- python3 /opt/test.py > /home/dell/ece.conf 2>&1\'"
    ssh.exec_command(gen_secret)
    time.sleep(15)
    for remote, local in zip(remote_dapo_files, local_files):
        sftp.get(remote, local)
    sftp.get(new_remote_path, new_local_path)
    sftp.close()    
except Exception as e:
    print(f"Failed to connect to {dapo_hostname}: {e}")
ssh.close()

try:
    ssh.connect(node_hostname, node_ssh_port, node_username, node_password)
    sftp = ssh.open_sftp()
    for local in local_files:
        remote_path = os.path.join(remote_node_path, os.path.basename(local))
        sftp.put(local, remote_path)
    sftp.put(new_local_path, new_remote_node_path)
    sftp.put(modify_script, remote_modify_path)
    sftp.put(download_script, remote_download_path)
    sftp.put(additional_binaries_local_path, additional_binaries_remote_path)
    ssh.exec_command(f"chmod +x {remote_modify_path}")
    cmd = f"cd /hzp/ece-agent && bash {remote_modify_path} '{CLIENT_ID}' '{CLIENT_SECRET}' '{ORG_ID}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    new_cmd= f"bash {remote_download_path}"
    stdin, stdout, stderr =ssh.exec_command(new_cmd)
    stdout.channel.recv_exit_status()
    add_bin=f"cd /root && bash {additional_binaries_local_path}"
    stdin, stdout, stderr =ssh.exec_command(add_bin)
    stdout.channel.recv_exit_status()
    
except Exception as e:
    print(f"Failed to connect to {node_hostname}: {e}")
    sftp.close()
ssh.close()

