# UpdatEngine-client

UpdatEngine-client allow computer and server to be inventoried automatically on an updatengine server and to deploy softwares

- [Installation](#installation)
- [Links](#links)
- [License](#license)

## Installation
### Windows
The installation can be done by the graphical interface of the setup. Below only silent command line installations are presented.
#### Example with an SSL certificat and immediate replacement of an existing installation
If installed from an UE-Server then there is no 'Operation completed' in deployment history.
```
updatengine-client-setup-3.1.exe /verysilent /server=https://UE-SERVER_IP:1979 /noproxy /delay=30 /cert="%CD%\cacert.pem" /norestart /forceinstall
```

### Linux
```
wget -O /tmp/install-updatengine-client.sh https://raw.githubusercontent.com/noelmartinon/updatengine-client/master/Linux/setup/install-updatengine-client.sh --no-check-certificate && chmod +x /tmp/install-updatengine-client.sh && sudo /tmp/install-updatengine-client.sh -s "https://UE-SERVER_IP:1979" -m 30 -c mycert.pem -n
```
 
## Links
- French Google discussion group : https://groups.google.com/forum/#!forum/updatengine-fr
- Old official site : https://updatengine.com/
- Site archive : https://web.archive.org/web/20170318143615/http://www.updatengine.com:80/

## License
GPL-2.0
