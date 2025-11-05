#!/bin/bash
# Usage: bash modify_ece_conf.sh <CLIENT_ID> <CLIENT_SECRET> <ORG_ID>

CLIENT_ID=$1
CLIENT_SECRET=$2
ORG_ID=$3
FILE="/hzp/ece-agent/ece.conf"
MACHINE_ID=$(dmidecode -t system | awk 'NR==10{print $3}')
# --- Safety check ---
if [ ! -f "$FILE" ]; then
  echo "❌ File not found: $FILE"
  exit 1
fi

# --- Remove first 2 lines and last 3 lines ---
sed -i '1,2d' "$FILE"
sed -i -e :a -e '$d;N;2,3ba' -e 'P;D' "$FILE"

#add machine details
sed -i "2i MACHINE_ID=${MACHINE_ID}" "$FILE"

# --- Update CLIENT_ID, CLIENT_SECRET, and ORG_ID ---
sed -i "s/^CLIENT_ID=.*/CLIENT_ID=$CLIENT_ID/" "$FILE"
sed -i "s/^CLIENT_SECRET=.*/CLIENT_SECRET=$CLIENT_SECRET/" "$FILE"
sed -i "s/^ORG_ID=.*/ORG_ID=$ORG_ID/" "$FILE"

echo "✅ ece.conf updated successfully"
