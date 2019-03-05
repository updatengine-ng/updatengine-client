#!/bin/bash

## Debian/Ubuntu installation script

## One shot installation command (just specify your UE-SERVER_URL and optionally the execution delay) :
#
# wget -O /tmp/install-updatengine-client.sh https://raw.githubusercontent.com/noelmartinon/updatengine-client/nm-dev/LinuxDpkg/setup/install-updatengine-client.sh --no-check-certificate && chmod +x /tmp/install-updatengine-client.sh && sudo /tmp/install-updatengine-client.sh "https://UE-SERVER_IP:1979"
##

# Only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

UE_url=$1
UE_delay=$2

if [ -z "$UE_url" ];
 then
   echo "The UpdatEngine web server is required" 1>&2
   exit 1
fi

if [ -z "$UE_delay" ];
 then
   echo "Delay is set to default value (30 minutes)" 1>&2
   UE_delay=30
fi

apt-get install python-dmidecode python-libxml2 python-lxml python-netifaces python-psutil git-core
cd /opt
git clone https://github.com/noelmartinon/updatengine-client.git
chmod +x /opt/updatengine-client/LinuxDpkg/updatengine-client.py
echo "*/$UE_delay * * * *   root   /opt/updatengine-client/LinuxDpkg/updatengine-client.py -i -s $UE_url -m $UE_delay" > /etc/cron.d/updatengine-client
nohup /opt/updatengine-client/LinuxDpkg/updatengine-client.py -i -s $UE_url -m $UE_delay >/dev/null 2>&1 &
