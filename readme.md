This project implements a Flask-based REST API to execute various tasks, including starting and stopping an HTTP server, DNS queries, and HTTP GET requests. The API is designed with the **Command Design Pattern** and uses an in-memory database to manage the HTTP server state.

---

## Prerequisites

Ensure the following are installed on your system:

1. **Python** (>=3.8)
2. **pip** (Python package manager)

---

## Installation

### 1. Extract the Files From the Zip
download the project files to your local machine.

### 2. Set Up the Environment
It is recommended to use a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```
###3. Install Dependencies
Create a requirements.txt file in the project directory with the following content:
```
flask
flask-swagger-ui
requests
```
Then install the dependencies using:
```
pip install -r requirements.txt
```

Running the Application
Start the Flask application:

```
python api_server.py
```
The API will start on http://127.0.0.1:5000 by default.

To access the Swagger UI documentation, visit:

http://127.0.0.1:5000/swagger


##API Endpoints
###1. Start HTTP Server
Endpoint: /run_task/start_server
Method: POST
Description: Starts an HTTP server on the specified port and page URI. Returns a unique UUID for the server.

Request Body:
```
{
  "port": 8080,
  "uri": "/test",
  "data_to_return": "Hello, world!"
}
```
Example Response:
```
{
    "result": {
        "message": "Server started on port 8084 with path 127.0.0.1/test1",
        "status": "success",
        "uuid": "c41ae6db-126b-4138-93fa-dd1670e0a355"
    },
    "status": "success"
}
```
###2. Stop HTTP Server
Endpoint: /run_task/stop_server
Method: POST
Description: Stops the HTTP server identified by the UUID. Returns a list of IP addresses that accessed the server.

Request Body:
```
{
  "uuid": "uuid-1234-5678-90ab"
}
```
Example Response:
```
  {
    "result": {
        "message": "Server 32897469-36bc-4782-b475-4843b5100432 stopped",
        "status": "success",
        "uuid": "32897469-36bc-4782-b475-4843b5100432",
        "visitors": ["192.168.1.100", "192.168.1.101"]
    },
    "status": "success"
}
```
###3. DNS Query Task
Endpoint: /run_task/dns_query

Method: POST

Description: Resolves the given domain to an IP address.

Request Body:
```
{
  "domain": "google.com"
}
```
Example Response:
```
{
  "status": "success",
  "result": "142.250.72.14"
}
```
###4. HTTP GET Task
Endpoint: /run_task/http_get

Method: POST

Description: Performs an HTTP GET request to the specified domain or IP and returns the response data.

Request Body:
```
{"domain": "jsonplaceholder.typicode.com","port":80, "uri":"/posts/1"}
```
Example Response:
```
{
  "status": "success",
  "result": "<!doctype html> <html> ..."
}
```
