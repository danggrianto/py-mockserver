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
from pymockserver import RequestTimes

# without times
def create_expectation(self):
    client = Client('localhost', 1080)
	request = Request('/somepath', 'POST')
	response = Response('')
	client.expectation(request, response)

# with times
def create_expectation(self):
    client = Client('localhost', 1080)
	request = Request('/somepath', 'POST')
	response = Response('')
    times = Times()
	client.expectation(request, response, times)
```
`RequestTimes` is optional to specify if you don't want that fake endpoint to live forever

### Getting recorded requests

```
from pymockserver import Client, Request

# get all recorded requests
client = Client('localhost', 1080)

def get_all_recorded():
   requests = client.retrieve_requests()
   # do something with array requests

def get_recorded_request_match():
    request = Request('/hello', 'POST')
    requests = client.retrieve_requests(request)
```

