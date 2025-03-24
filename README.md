# ZapNet ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![PyPI Version](https://img.shields.io/pypi/v/zapnet.svg)](https://pypi.org/project/zapnet/)

[中文](README_zh.md) | [English](README.md)

ZapNet is a high-performance network diagnostics toolkit with Multi-Protocol Support, including TCP and UDP.

## Key Features

- 🚀 **Dual Protocol Engine**: TCP full-duplex / UDP broadcast
- 📊 **Traffic Analytics**: Real-time connection monitoring
- 🔧 **Smart Config**: YAML-driven test scenarios
- 💾 **Data Archiving**: Raw packet capture (ASCII/Hex)
- 🌍 **Cross-Platform**: Windows/macOS/Linux support

## Installation

```python
# For production use
pip install zapnet

# Development setup
git clone https://github.com/luhuadong/zapnet.git
cd zapnet && pip install -e .[dev]
```

## Quick Start

### TCP Server/Client

```bash
# Start TCP server
zapnet tcp server --port 5555

# Start TCP client
zapnet tcp client --host 127.0.0.1 --port 5555 --data "Hello, World"
# Send hexadecimal content
zapnet tcp client --host 127.0.0.1 --port 5555 --hex "A1B2C3D4"
# Another form to fill in target IP and port
zapnet tcp client --target 127.0.0.1:5555 --hex "A1B2C3D4"
```

### UDP Server/Client

```bash
# Start UDP server
zapnet udp server --port 6666

# Start UDP client
zapnet udp client --host 127.0.0.1 --port 6666 --data "Hello, World"
# Send hexadecimal content
zapnet udp client --host 127.0.0.1 --port 6666 --hex "A1B2C3D4"
# Another form to fill in target IP and port
zapnet udp client --target 127.0.0.1:6666 --hex "A1B2C3D4"
```

### Device Discovery (UDP Broadcast)

```bash
# Send probe broadcast
zapnet udp client --target 192.168.1.255:9999 --broadcast --hex "A1B2C3D4"

# Monitor responses
zapnet udp server --port 9999 --filter "hex_contains(payload, 'C3D4')" --output devices.log
```

### Network Sniffing (UDP)

```bash
# Capture DNS queries
zapnet udp server --port 53 --hex --stats 5

# Send custom DNS query
zapnet udp client --target 8.8.8.8:53 --hex "b362010000010000000000000377777706676f6f676c6503636f6d0000010001"
```

### TCP Stress Testing

```bash
# Start TCP server
zapnet tcp server --port 9000 --max-conn 50 --timeout 300

# Simulate high concurrency
zapnet tcp client --host 127.0.0.1 --port 9000 --threads 10 --duration 60 --message "LOAD_TEST"
```

### File Transfer

```bash
# Send file (TCP)
zapnet tcp client --host 192.168.1.100 --port 8888 --file data.zip

# Receive files
zapnet tcp server --port 8888 --output received_files/
```

## Advanced Configuration

You can set default parameters through ZapNet's configuration file `config.yaml`, for example:

```yaml
network:
  tcp:
    buffer_size: 4096
    keepalive: true
  udp:
    broadcast_ttl: 64

logging:
  level: debug
  rotation: 100MB

security:
  allowed_ips: ["192.168.1.0/24"]
```

Launch with:

```bash
zapnet --config config.yaml
```

## License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.
