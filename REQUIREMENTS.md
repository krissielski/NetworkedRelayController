# Networked Relay Controller

## Project Overview
Create a **Networked Relay Controller** system for Raspberry Pi 3 with a 4-port relay hat. The system should provide network-accessible API control of individual relays through a clean, modular Python codebase.

## Technical Specifications

### **Hardware Platform**
- Raspberry Pi 3 with 4-port relay hat
- Relay pin mappings:
  - Relay 1 → GPIO Pin 31
  - Relay 2 → GPIO Pin 33  
  - Relay 3 → GPIO Pin 35
  - Relay 4 → GPIO Pin 37

### **Core Requirements**

#### **API Functionality**
Implement a REST API server accessible via network (Ethernet/WiFi) supporting these endpoints:

| Endpoint | Method | Description | Example Response |
|----------|--------|-------------|------------------|
| `/relay/all/on` | POST | Turn all relays ON | `{"status": "success", "message": "All relays turned ON"}` |
| `/relay/all/off` | POST | Turn all relays OFF | `{"status": "success", "message": "All relays turned OFF"}` |
| `/relay/{id}/on` | POST | Turn specific relay ON (1-4) | `{"status": "success", "relay": 1, "state": "ON"}` |
| `/relay/{id}/off` | POST | Turn specific relay OFF (1-4) | `{"status": "success", "relay": 1, "state": "OFF"}` |
| `/relay/status` | GET | Get status of all relays | `{"relays": [{"id": 1, "state": "ON"}, {"id": 2, "state": "OFF"}...]}` |
| `/system/version` | GET | Get software version | `{"version": "1.0.0", "build_date": "2024-01-01"}` |
| `/system/health`  | GET | Get system health | `{"status": "healthy"}` |

#### **Architecture Requirements**
- **Modular Design**: Implement clean separation of concerns
- **Extensible**: Easy to add new API endpoints and functionality
- **Error Handling**: Comprehensive error handling with meaningful responses
- **Logging**: Structured logging for debugging and monitoring
- **Configuration**: External configuration file for settings

## Complete Project Structure

```
/
├── README.md                       # Main project documentation
│
├── config/                         # Configuration files
│   └── settings.yaml               # Default configuration
│
├── src/                           # Source code
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── api_server.py              # REST API server implementation
│   ├── relay_controller.py        # Hardware relay control logic
│   ├── config_manager.py          # Configuration management
│   └── logger.py                  # Logging setup
│
├── tests/
│   ├── __init__.py
│   ├── test_relay_controller.py
│   ├── test_api_server.py
│   ├── test_config_manager.py
│   └── test_logger.py
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── version.txt            # Version information
```

## Detailed Module Specifications

### **main.py**
- Application entry point
- Initialize configuration, logging, relay controller, and API server
- Handle graceful shutdown
- Basic command-line argument parsing

### **relay_controller.py**
- GPIO pin management and relay control
- Methods: `turn_on(relay_id)`, `turn_off(relay_id)`, `turn_all_on()`, `turn_all_off()`, `get_status()`
- Input validation (relay IDs 1-4)
- Hardware abstraction layer

### **api_server.py**  
- Flask-based REST API server
- Route handlers for all endpoints
- JSON response formatting
- Input validation and error handling
- Integration with relay controller

### **config_manager.py**
- YAML configuration file parsing
- Default configuration values
- Configuration validation
- Settings for: API port, relay pin mappings, logging levels, etc.

### **logger.py**
- Structured logging setup
- File and console output
- Configurable log levels
- Timestamp and module identification


## Quality Requirements

### **Error Handling**
- Invalid relay IDs (not 1-4)
- GPIO hardware failures
- Network connectivity issues  
- Malformed API requests
- Configuration file errors

### **Testing Strategy**
- Unit tests for all modules except main.py
- Mock GPIO operations for testing without hardware
- API endpoint testing with sample requests
- Configuration validation testing
- Minimum 80% code coverage target


### **Configuration (settings.yaml)**
```yaml
api:
  host: "0.0.0.0"
  port: 5000
  
relays:
  pins:
    1: 31
    2: 33  
    3: 35
    4: 37
    
logging:
  level: "INFO"
  file: "relay_controller.log"
  
system:
  version: "1.0.0"
```

## Dependencies & Libraries
- **Flask**: REST API framework
- **RPi.GPIO**: Raspberry Pi GPIO control
- **PyYAML**: Configuration file parsing
- **pytest**: Unit testing framework
- **requests**: HTTP client for testing

## Success Criteria
- All API endpoints functional and tested
- Modular code architecture with proper separation
- Comprehensive unit test suite  
- Clear documentation and setup instructions
- Easy to extend with new functionality
- Robust error handling and logging

## Implementation Guidelines

### **Python Best Practices**
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Implement proper exception handling
- Use context managers for resource management
- Follow SOLID principles for class design

### **Security Considerations**
- Input validation for all API endpoints
- Rate limiting for API requests
- Proper error messages that don't expose system internals
- Optional basic authentication support

### **Performance Requirements**
- API response time under 100ms for relay operations
- Support for concurrent API requests
- Efficient GPIO operations
- Minimal memory footprint

Create a production-ready system that follows Python best practices, includes comprehensive testing, and can be easily maintained and extended.


