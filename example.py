import requests
from requests_chains import chain_requests

proxychains = [
  "socks5://127.0.0.1:9050"
]

chain_requests(proxychains) # Proxychains everything in requests


s = requests.Session()

while 1:
  a = s.get('http://api.ipify.org?format=json')
  print(a.text)


