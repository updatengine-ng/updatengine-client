#!/bin/bash

## Debian/Ubuntu installation script

## One shot installation command (just specify your UE-SERVER_IP) :
#
# wget -O /tmp/install-updatengine-client.sh https://raw.githubusercontent.com/noelmartinon/updatengine-client/nm-dev/LinuxDpkg/setup/install-updatengine-client.sh --no-check-certificate && chmod +x /tmp/install-updatengine-client.sh && sudo /tmp/install-updatengine-client.sh "https://UE-SERVER_IP:1979"
##

# Only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get install python-dmidecode python-libxml2 python-lxml python-netifaces git-core
cd /opt
git clone https://github.com/noelmartinon/updatengine-client.git
chmod +x /opt/updatengine-client/LinuxDpkg/updatengine-client.py
echo "*/30 * * * *   root   /opt/updatengine-client/LinuxDpkg/updatengine-client.py -i -s $1" > /etc/cron.d/updatengine-client
/opt/updatengine-client/LinuxDpkg/updatengine-client.py -i -s $1
