import requests
from requests_chain import chain_requests

proxychains = [
        "http://localhost:8888",
        "http://localhost:8889"
]

chain_requests(proxychains) # Proxychains everything in requests


while 1:
    a = requests.get('http://api.ipify.org?format=json')
    print(a.text)


