# cdnetworks-cache-api

## Usage

```python
from cdnetworks import CDNetworksAPI, SERVICE_AREA_US_GLOBAL

cdn = CDNetworksAPI('login', 'password', SERVICE_AREA_US_GLOBAL)

cdn.get_pads()
{'pads': [u'cdn1.example.com', u'cdn2.example.com']}

cdn.do_purge('cdn1.example.com')
{'pid': 503653579}

```
