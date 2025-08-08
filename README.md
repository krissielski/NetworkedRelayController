# Networked Relay Controller

## Overview
A production-ready, modular Python system for controlling a 4-port relay hat on Raspberry Pi 3 via a REST API. Designed for extensibility, robust error handling, and easy configuration.

## Features
- Control individual or all relays over the network
- REST API endpoints for relay and system management
- Modular codebase with clear separation of concerns
- Structured logging and external YAML configuration
- Unit tests with mock GPIO for hardware-free testing

## Project Structure
```
/
├── config/settings.yaml         # Configuration file
├── src/                        # Source code
│   ├── main.py                 # Entry point
│   ├── api_server.py           # REST API server
│   ├── relay_controller.py     # Relay control logic
│   ├── config_manager.py       # Config management
│   └── logger.py               # Logging setup
├── tests/                      # Unit tests
│   ├── test_relay_controller.py
│   ├── test_api_server.py
│   ├── test_config_manager.py
│   └── test_logger.py
├── requirements.txt            # Python dependencies
├── version.txt                 # Version info
└── README.md                   # Documentation
```

## Setup Instructions
1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
2. **Configure settings:**
   Edit `config/settings.yaml` as needed for your environment.
3. **Run the server:**
   ```powershell
   python src/main.py
   ```
4. **Run tests:**
   ```powershell
   pytest
   ```

## API Endpoints
| Endpoint             | Method | Description                  |
|----------------------|--------|------------------------------|
| `/relay/all/on`      | POST   | Turn all relays ON           |
| `/relay/all/off`     | POST   | Turn all relays OFF          |
| `/relay/{id}/on`     | POST   | Turn specific relay ON (1-4) |
| `/relay/{id}/off`    | POST   | Turn specific relay OFF (1-4)|
| `/relay/status`      | GET    | Get status of all relays     |
| `/system/version`    | GET    | Get software version         |
| `/system/health`     | GET    | Get system health            |

## Testing
- All modules except `main.py` are covered by unit tests
- GPIO operations are mocked for safe testing
- Minimum 80% code coverage target

## Extending
- Add new endpoints in `api_server.py`
- Add new config options in `settings.yaml` and `config_manager.py`

## License
MIT
