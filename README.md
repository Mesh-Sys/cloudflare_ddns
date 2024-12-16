# CLOUDFLARE DDNS
Implement a Dynamic Domain Name System (DDNS) Using the Cloudflare Api, Works for only Ipv4 Addresses For Now

# INSTALL
  clone the repo

   ```bash
   git clone https://github.com/Mesh-Sys/cloudflare_ddns.git
   cd cloudflare_ddns
   pip install requests
   sudo ./install.sh
   ```

# UNINSTALL
  ```bash
  sudo /opt/cloudflare_ddns/uninstall.sh
  ```

# CONFIGURATION
  config can be set through OS environment variable

  for os environment variables
  ```bash
  export CLOUDFLARE_API_KEY=YOUR_API_KEY
  export CLOUDFLARE_AUTH_EMAIL=YOUR_AUTHENTICATION_EMAIL
  export CLOUDFLARE_ZONE_ID=YOUR_ZONE_ID
  export CLOUDFLARE_DOMAIN=YOUR_DOMAIN_NAME
  export CLOUDFLARE_TTU=TIME_TO_UPDATE #DEFAULT VALUE IS 5 minutes
  ```
  and restart the service
  ```bash
  sudo systemctl restart cloudflare_ddns.service
  ```
  NOTE: TIME_TO_UPDATE is the time taken for it to refresh and update the ip address on cloudflare