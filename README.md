# Requests chains
Adds the ability to use proxy chains directly the python requests module.

# Install the package
```bash
pip install requests-chain
```

## Import necessary modules
```python3
import requests
from requests_chains import chain_requests
```

## Set up proxy chains
```python3
proxychains = [
  "socks5://127.0.0.1:9050",
  "socks5://user:pwd@ip:port"
]

chain_requests(proxychains) # Patch requests to use proxy chains
```
Done.
Any requests from now on will be firstly send thorugh the chain specified.

## How to add another proxy on top of this chain ? Simple!
With requests-chain you can just use the normal requests proxies built-in param to add a proxy, and that will be build on top of the chain specified!
```python3
r1 = s.get('http://api.ipify.org?format=json', proxies={"http":"socks5://proxy1:port1", "https":"socks5://proxy1:port1"})
r2 = s.get('http://api.ipify.org?format=json', proxies={"http":"socks5://proxy2:port2", "https":"socks5://proxy2:port2"})
print(r1.text)
```
- r1 will firstly go through the whole chain and then on proxy1
- r2 will firstly go through the whole chain and then on proxy2
