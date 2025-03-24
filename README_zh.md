# ZapNet ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/) [![PyPI Version](https://img.shields.io/pypi/v/zapnet.svg)](https://pypi.org/project/zapnet/)

[English](README.md) | [中文](README_zh.md)

ZapNet 是一个高性能的 TCP/UDP 网络测试诊断工具包，支持 TCP/UDP 协议的多模式测试与流量分析。

## 核心功能

- 🚀 **双协议引擎**：TCP全双工通信 / UDP广播支持
- 📊 **流量可视化**：实时显示连接状态与流量统计
- 🔧 **智能配置**：YAML文件驱动多场景测试
- 💾 **数据归档**：原始报文存储（支持ASCII/Hex）
- 🌍 **跨平台**：Windows/macOS/Linux全支持

## 安装指南

```python
# 生产环境
pip install zapnet

# 开发模式
git clone https://github.com/luhuadong/zapnet.git
cd zapnet && pip install -e .[dev]
```

## 快速开始

### TCP 服务端/客户端

```bash
# 启动 TCP 服务端
zapnet tcp server --port 5555

# 新终端运行 TCP 客户端测试
zapnet tcp client --host 127.0.0.1 --port 5555 --data "Hello, World"
# 发送十六进制内容
zapnet tcp client --host 127.0.0.1 --port 5555 --hex "A1B2C3D4"
# 使用精简模式填写目标 IP 和端口
zapnet tcp client --target 127.0.0.1:5555 --hex "A1B2C3D4"
```

### UDP 服务端/客户端

```bash
# 启动 UDP 服务端
zapnet udp server --port 6666

# 新终端运行 UDP 客户端测试
zapnet udp client --host 127.0.0.1 --port 6666 --data "Hello, World"
# 发送十六进制内容
zapnet udp client --host 127.0.0.1 --port 6666 --hex "A1B2C3D4"
# 使用精简模式填写目标 IP 和端口
zapnet udp client --target 127.0.0.1:6666 --hex "A1B2C3D4"
```

### 设备发现（UDP广播）

```bash
# 发送设备探测广播（全子网）
zapnet udp client --target 192.168.1.255:9999 --broadcast --hex "A1B2C3D4"

# 监听响应（服务端模式）
zapnet udp server --port 9999 --filter "hex_contains(payload, 'C3D4')" --output devices.log
```

### 网络嗅探（UDP诊断）

```bash
# 捕获DNS请求（端口53）
zapnet udp server --port 53 --hex --stats 5

# 发送自定义DNS查询
zapnet udp client --target 8.8.8.8:53 --hex "b362010000010000000000000377777706676f6f676c6503636f6d0000010001"
```

### TCP压力测试

```bash
# 启动TCP压力服务器
zapnet tcp server --port 9000 --max-conn 50 --timeout 300

# 模拟高并发客户端（10线程，持续60秒）
zapnet tcp client --host 127.0.0.1 --port 9000 --threads 10 --duration 60 --message "LOAD_TEST"
```

### 文件传输

```bash
# 发送文件（TCP模式）
zapnet tcp client --host 192.168.1.100 --port 8888 --file data.zip

# 接收文件（自动保存）
zapnet tcp server --port 8888 --output received_files/
```

## 高级配置

可通过 ZapNet 的配置文件 `config.yaml` 设置默认参数，例如：

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

启动配置：

```bash
zapnet --config config.yaml
```

## 许可证

基于MIT许可证分发，详见 [LICENSE](LICENSE.md) 文件。
