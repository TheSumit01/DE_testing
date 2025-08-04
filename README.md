# Network Protocol Educational Simulator

## Overview
This repository contains a Python script designed for educational purposes to demonstrate how different network protocols (HTTP, HTTPS, and ICMP) work. The script simulates legitimate network requests at a controlled rate with built-in safety features to prevent misuse.

## Educational Purpose
This tool is created strictly for educational purposes to help understand:
- How HTTP and HTTPS requests work
- Basic network connectivity testing concepts
- Network protocol headers and responses
- Request/response timing and analysis

## Features
- Supports HTTP, HTTPS, and ICMP protocol simulation
- Built-in rate limiting and request caps for safety
- Detailed output of request/response headers
- Educational notes and explanations
- Whitelist protection (only allows localhost by default)

## Safety Measures
- Maximum request limit (20 requests)
- Minimum delay between requests (1 second)
- Target whitelist (only localhost/127.0.0.1 by default)
- Comprehensive warning messages

## Usage
```
python network_protocol_simulator.py --target 127.0.0.1 --port 8080 --protocol http --requests 5 --delay 1
```

### Parameters
- `--target`: Target host (default: 127.0.0.1)
- `--port`: Target port (default: 80)
- `--protocol`: Protocol to simulate [http, https, icmp] (default: http)
- `--requests`: Number of requests to send (default: 5, max: 20)
- `--delay`: Delay between requests in seconds (default: 1.0, min: 1.0)
- `--path`: Path for HTTP/HTTPS requests (default: /)

## Legal and Ethical Notice
This tool should only be used in controlled environments against targets you own or have explicit permission to test. Using this or similar tools against unauthorized targets may be illegal and unethical.

## Requirements
- Python 3.6+
- requests library (`pip install requests`)

## Example Output
The script provides detailed information about each request, including:
- Request headers sent
- Response headers received
- Status codes
- Response times
- Response sizes
- Summary statistics

## Educational Resources
To learn more about network protocols and ethical network testing, consider these resources:
- [Mozilla Developer Network (MDN) HTTP documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Wireshark University](https://www.wireshark.org/docs/)