#!/bin/bash

if [ $(id -u) -ne 0 ]; then
	echo 'please run command as root'
	exit
fi

sudo systemctl disable --now cloudflare_ddns.service
sudo rm /usr/lib/systemd/system/cloudflare_ddns.service
sudo rm -r /opt/cloudflare_ddns
echo "DONE"
echo "LOGFILE STILL EXISTS FOR DEBUGGING PURPOSES RUN 'sudo rm /var/log/cloudflare_ddns.log' TO REMOVE THE LOGFILE"