import os
 
portal_base_path = os.getenv('DAP_PORTAL_URL','')
 
print("---------------All DAP Env variables---------------------")
print(f"EO_DOMAIN=mtls-{os.getenv('EO_FQDN', '')}")
print(f"CLIENT_ID={os.getenv('DAP_AGENT_CLIENT_ID', '')}")
print(f"CLIENT_SECRET={os.getenv('DAP_AGENT_CLIENT_SECRET', '')}")
print(f"ORG_ID={os.getenv('DAP_AGENT_CLIENT_ORG_ID', '')}")
print(f"ORCHESTRATOR_DOMAIN={os.getenv('EO_FQDN', '')}")
print(f"ORCHESTRATOR_CA_CERT_PATH=/hzp/orchestrator_ca.crt")
print(f"PORTAL_DOMAIN={portal_base_path.split('https://')[1]}")
print(f"PORTAL_CA_CERT_PATH=/hzp/portal_ca.crt")
print("Note: Copy the following ca certs to dap agent node at /hzp folder and rename it accordingly in case of On-Prem Mode")
print("ORCHESTRATOR CA cert file is found at : /tmp/certs/dapo/cacert (In On-Prem Mode)")
print("PORTAL CA cert file is found at : /tmp/certs/dapp/tlscacert (In On-Prem Mode")
