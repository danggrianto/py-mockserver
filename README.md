# py-mockserver
mockserver client for james bloom's mockserver https://github.com/jamesdbloom/mockserver

## installation

```
pip install py-mockserver
```

## Usage
For detail instruction how to use mockserver see this [documentation](http://www.mock-server.com/mock_server/getting_started.html)

### Creating Expectations
```
from pymockserver import Client, Request, Response

def create_expectation(self):
    client = Client('localhost', 1080)
	request = Request('/somepath', 'POST')
	response = Response('')
	client.expectation(request, response)
```
