**This Repo is used to Install the ECE agent on your nodes for Brownfeild Node Onboarding**

**#steps**
1. Run the code from anywhere but have a Virtual Pyhton env with version 3.11 or greater and install paramiko labrary using below command
pip install paramiko

2. clone the repo

3. provide below inputs in agent_installation.py file
a. Node details
b. DAPO VM details
c. Client secret
d. Client ID
e. TLS ID

**#Constraints**
1) all root Previlages should be provide to DAPO VM
  
2) node root details tobe provided and the root login to be enabled

expecting DAPO VM to have user dell
