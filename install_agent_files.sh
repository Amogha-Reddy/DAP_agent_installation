path="/hzp/ece-agent/"
absolute_path="/usr/local/bin/"

file1='ece-agent_deb-dap-3.2.0.0-13776d9a-30_amd64.deb'
file2='hzp-ece-rfutil'

agent_file_url="https://isgedge.artifactory.cec.lab.emc.com/artifactory/isgedge-deb-virtual/pool/rel/dap-1.0.0.0/e/ece-agent/ece-agent_deb-dap-3.2.0.0-13776d9a-30_amd64.deb"
Ismrfutil_url="https://hopjpd.artifactory.cec.lab.emc.com:443/artifactory/isgedge-generic-virtual/hzp/ece/rfutil/rel/dap-1.0.0.0/3.2.0.0-f58b2d2-1/hzp-ece-rfutil"

cd "$path"
wget "$agent_file_url" --no-check-certificate
wget "$Ismrfutil_url" --no-check-certificate

mv $file2 ismrfutil && chmod +x ismrfutil && mv ismrfutil $absolute_path
cd "$path"
dpkg -i $file1
systemctl enable ece-agent.service
dpkg -i $file1
systemctl start ece-agent.service