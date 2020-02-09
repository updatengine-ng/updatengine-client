#!/bin/bash

## Debian/Ubuntu installation script

## One shot installation command (just specify your UE-SERVER_URL and optionally the client execution delay in minutes and SSL cert) :
#
# wget -O /tmp/install-updatengine-client.sh https://raw.githubusercontent.com/updatengine-ng/updatengine-client/master/Linux/setup/install-updatengine-client.sh --no-check-certificate && chmod +x /tmp/install-updatengine-client.sh && sudo /tmp/install-updatengine-client.sh -s "https://UE-SERVER_IP:1979" -m 30 -c mycert.pem -n
##

# Only root can run this script
if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

UE_url=""
UE_delay=""
UE_cert=""
UE_noproxy=""

# Get arguments
while getopts s:m:c:n option
do
  case "${option}"
  in
    s) UE_url=${OPTARG};;
    m) UE_delay=${OPTARG};;
    c) UE_cert=${OPTARG};;
    n) UE_noproxy=" -n";;
  esac
done

if [ -z "$UE_url" ]; then
  echo "The UpdatEngine web server is required" 1>&2
  exit 1
fi

if [ -z "$UE_delay" ]; then
  echo "Delay is set to default value (30 minutes)"
  UE_delay=30
fi

#apt install python-dmidecode python-libxml2 python-lxml python-netifaces python-psutil unzip
sudo apt-get install python3.7 python3.7-dev
sudo pip3 install testresources setuptools dmiparse psutil lxml py-dmidecode netifaces
pkill -f updatengine-client.py
wget https://github.com/updatengine-ng/updatengine-client/archive/master.zip -O /tmp/ue-client.zip && unzip -o /tmp/ue-client.zip -d /tmp/ && rm /tmp/ue-client.zip
mkdir -p /opt/updatengine-client
yes | cp -rf /tmp/updatengine-client-master/* /opt/updatengine-client/

if [ -n "$UE_cert" ]; then
  echo "Copy SSL cert '$UE_cert' to '/opt/updatengine-client/Linux/cacert.pem'"
  yes | cp -rf "$UE_cert"  "/opt/updatengine-client/Linux/cacert.pem" > /dev/null 2>&1
  if [ "$?" -gt "0" ]; then
    echo "Error: Problem with SSL cert. Installation aborted"
    exit 1
  fi
  UE_cert=" -c /opt/updatengine-client/Linux/cacert.pem"
fi

chmod +x /opt/updatengine-client/Linux/updatengine-client.py
echo "*/$UE_delay * * * *   root   cd /opt/updatengine-client && /opt/updatengine-client/Linux/updatengine-client.py -i -s $UE_url -m $UE_delay$UE_cert$UE_noproxy" > /etc/cron.d/updatengine-client
cd /opt/updatengine-client
nohup /opt/updatengine-client/Linux/updatengine-client.py -i -s $UE_url -m $UE_delay$UE_cert$UE_noproxy >/dev/null 2>&1 &
cd - > /dev/null
echo "Installation completed"
