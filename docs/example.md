# Networked Relay Controller Usage Guide

This document demonstrates how to interact with the Networked Relay Controller using both the GUI application and the REST API directly.

## GUI Application Usage

### Installation
1. Ensure Python is installed on your system
2. Install required dependencies:
```bash
pip install -r app/requirements.txt
```

### Running the GUI
The GUI application can be started in several ways:

```bash
# Connect to localhost (default)
python app/relay_gui.py

# Connect to specific IP address
python app/relay_gui.py --host 192.168.1.100

# Connect to specific IP and port
python app/relay_gui.py --host 192.168.1.100 -p 5000

# Connect to hostname
python app/relay_gui.py --host relay-controller.local
```

### GUI Features
- **Connection Status**: Shows current connection state and server version
- **Global Controls**:
  - `All ON` button: Turns all relays on
  - `All OFF` button: Turns all relays off
  - `Get Status` button: Refreshes the status of all relays
- **Individual Controls**:
  - LED indicators show current state (green = ON, red = OFF)
  - Toggle buttons for each relay
- **Status Bar**: Shows operation results and error messages

## REST API Usage

You can also interact with the controller directly using its REST API. Below are examples using `curl` and Python's `requests` library.

## Base URL
Assume the server is running at `http://<raspberrypi-ip>:5000`

---

## Turn All Relays ON
**Endpoint:** `POST /relay/all/on`

### curl
```sh
curl -X POST http://<raspberrypi-ip>:5000/relay/all/on
```

### Python
```python
import requests
resp = requests.post('http://<raspberrypi-ip>:5000/relay/all/on')
print(resp.json())
```

---

## Turn All Relays OFF
**Endpoint:** `POST /relay/all/off`

### curl
```sh
curl -X POST http://<raspberrypi-ip>:5000/relay/all/off
```

### Python
```python
resp = requests.post('http://<raspberrypi-ip>:5000/relay/all/off')
print(resp.json())
```

---

## Turn Specific Relay ON
**Endpoint:** `POST /relay/{id}/on`

### curl
```sh
curl -X POST http://<raspberrypi-ip>:5000/relay/1/on
```

### Python
```python
resp = requests.post('http://<raspberrypi-ip>:5000/relay/1/on')
print(resp.json())
```

---

## Turn Specific Relay OFF
**Endpoint:** `POST /relay/{id}/off`

### curl
```sh
curl -X POST http://<raspberrypi-ip>:5000/relay/1/off
```

### Python
```python
resp = requests.post('http://<raspberrypi-ip>:5000/relay/1/off')
print(resp.json())
```

---

## Get Status of All Relays
**Endpoint:** `GET /relay/status`

### curl
```sh
curl http://<raspberrypi-ip>:5000/relay/status
```

### Python
```python
resp = requests.get('http://<raspberrypi-ip>:5000/relay/status')
print(resp.json())
```

---

## Get Software Version
**Endpoint:** `GET /system/version`

### curl
```sh
curl http://<raspberrypi-ip>:5000/system/version
```

### Python
```python
resp = requests.get('http://<raspberrypi-ip>:5000/system/version')
print(resp.json())
```

---

## Get System Health
**Endpoint:** `GET /system/health`

### curl
```sh
curl http://<raspberrypi-ip>:5000/system/health
```

### Python
```python
resp = requests.get('http://<raspberrypi-ip>:5000/system/health')
print(resp.json())
```
