#!/bin/bash

if [ $(id -u) -ne 0 ]; then
	echo 'please run command as root'
	exit
fi

sudo mkdir /opt/cloudflare_ddns
sudo cp cloudflare_ddns.py /opt/cloudflare_ddns/cloudflare_ddns.py
sudo cp cloudflare_ddns.config /opt/cloudflare_ddns/cloudflare_ddns.config
sudo cp cloudflare_ddns.service /usr/lib/systemd/system/cloudflare_ddns.service
sudo cp uninstall.sh /opt/cloudflare_ddns/uninstall.sh
sudo systemctl daemon-reload
sudo systemctl enable --now cloudflare_ddns.service

echo "IF CONFIGS SUCH AS THE API KEY HAS NOT BEEN SET,"
echo "THE CONFIG FILE IS LOCATED AT /opt/cloudflare_ddns/cloudflare_ddns.config"
echo "THE LOGFILE IS LOCATED AT /var/log/cloudflare_ddns.log"
echo "ADD COFIG AND RESTART THE SERVCE WITH COMMAND 'sudo systemctl restart cloudflare_ddns.service'"
echo "TO UNINSTALL RUN /opt/cloudflare_ddns/uninstall.sh as root 'sudo /opt/cloudflare_ddns/uninstall.sh'"