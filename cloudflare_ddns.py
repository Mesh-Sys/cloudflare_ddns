# cloudflare ddns v0.1.0
VERSION = "v0.1.0"

import requests
from datetime import datetime
import json
import time
import sys
import os
import re

CONFIG_DIRECTORY = "/opt/cloudflare_ddns/cloudflare_ddns.config"
LOG_DIR = "/var/log/cloudflare_ddns.log"

URL = str()
ZONE_ID = str()
AUTH_EMAIL = str()
API_KEY = str()
DOMAIN = str()

# in minutes
TIME = int()

def log(message):
	log_file = open(LOG_DIR, "a")
	message = f"\n{datetime.now()}\n{message}\n"
	log_file.write(message)
	log_file.close()

def load_config(config_directory):
	global URL,ZONE_ID,AUTH_EMAIL,API_KEY,DOMAIN,TIME

	config_file = open(config_directory, "r")
	configs = json.load(config_file)
	config_file.close()

	URL = configs["URL"]
	ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID", configs["ZONE_ID"])
	AUTH_EMAIL = os.environ.get("CLOUDFLARE_AUTH_EMAIL", configs["AUTH_EMAIL"])
	API_KEY = os.environ.get("CLOUDFLARE_API_KEY", configs["API_KEY"])
	DOMAIN = os.environ.get("CLOUDFLARE_DOMAIN", configs["DOMAIN"])
	TIME = int(os.environ.get("CLOUDFLARE_TTU", configs["TTU"]))

	URL = re.sub("zone_id", ZONE_ID, URL)

	log(f"CLOUDFLARE DDNS {VERSION}")
	log(f"URL: {URL}\nZONE_ID: {ZONE_ID}\nAUTH_EMAIL: {AUTH_EMAIL}\nAPI_KEY: {API_KEY}\nDOMAIN: {DOMAIN}")

def fetch_public_ip():
	fetch_url = "https://api.ipify.org"
	public_ip_response = requests.get(fetch_url)

	if public_ip_response.status_code == 200:
		return str(public_ip_response.text)
	else:
		log(f"fetch_public_ip\nERROR {public_ip_response.status_code} - {public_ip_response.text}")

def fetch_record(domain, url, headers):
	record_response = requests.get(url, headers=headers)

	if record_response.status_code == 200:
		result = record_response.json()
		for record in result["result"]:
			if record["name"] == domain:
				return record
	else:
		log(f"fetch_record\nERROR {record_response.status_code}\n{json.dumps(record_response.json(), indent=4)}")

def update_record(record, content, url, headers):
	url += f"/{record["id"]}"
	data = {
		"content": content,
		"type": "A"
	}

	update_response = requests.patch(url, json=data, headers=headers)

	if update_response.status_code == 200:
		log(json.dumps(update_response.json(), indent=4))
	else:
		log(f"update_record\nERROR {update_response.status_code}\n{json.dumps(update_response.json(), indent=4)}")

def main():
	load_config(CONFIG_DIRECTORY)

	headers = {
		"Content-Type": "application/json",
		"X-Auth-Email": AUTH_EMAIL,
		"X-Auth-Key": API_KEY
	}
	
	time_delay = TIME * 60
	
	while True:
		if ZONE_ID == "ENVIRON" and AUTH_EMAIL == "ENVIRON"  and API_KEY == "ENVIRON"  and DOMAIN == "ENVIRON":
			log("INVALID CONFIGURATION, UPDATE CONFIG FILE OR ADD ENVIROMENT VARIABLES")
			continue
		current_ip = fetch_public_ip()
		
		current_record = fetch_record(DOMAIN, URL, headers)
		
		if current_record["content"] != current_ip:
			update_record(current_record, current_ip, URL, headers)
	
		time.sleep(float(time_delay))

if __name__ == "__main__":
	main()
