# API Usage Examples

This document demonstrates how to interact with the Networked Relay Controller API using `curl` and Python's `requests` library.

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
