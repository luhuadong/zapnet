import socket
import netifaces
import ipaddress
from typing import Tuple

def parse_address(address: str) -> Tuple[str, int]:
    """解析 host:port 格式的地址字符串
    
    Args:
        address: 目标地址，格式如 "192.168.1.1:8080" 或 "[::1]:9000"
    
    Returns:
        (host, port) 元组
        
    Raises:
        ValueError: 当格式无效时抛出
    """
    try:
        if address.startswith("["):  # IPv6处理
            host, port = address.rsplit("]", 1)
            host = host[1:]  # 移除开头的 [
            port = int(port[1:])  # 移除冒号
        else:
            host, port = address.rsplit(":", 1)
            port = int(port)
            
        return host, port
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid address format: {address}") from e

def is_valid_ip(address: str) -> bool:
    """验证是否为合法的IPv4/IPv6地址"""
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def resolve_host(host: str) -> str:
    """解析主机名为IP地址
    
    Returns:
        优先返回IPv4地址，否则返回IPv6地址
    """
    try:
        # 获取地址信息列表
        addr_info = socket.getaddrinfo(
            host, 
            None,  # port
            family=socket.AF_UNSPEC,
            type=socket.SOCK_DGRAM
        )
        
        # 优先选择IPv4
        for info in addr_info:
            if info[0] == socket.AF_INET:
                return info[4][0]
        
        # 回退到IPv6
        return addr_info[0][4][0]
    except socket.gaierror:
        raise ValueError(f"Cannot resolve host: {host}")

def is_broadcast_address(ip: str) -> bool:
    """判断是否为广播地址"""
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        return (
            ip_obj.is_multicast or 
            str(ip_obj).endswith(".255") or 
            ip == "255.255.255.255"
        )
    except ipaddress.AddressValueError:
        return False

def get_protocol_family(sock):
    family = sock.family
    return "IPv4" if family == socket.AF_INET else "IPv6"

def get_local_ips():
    ips = []
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for link in addrs[netifaces.AF_INET]:
                ips.append(link['addr'])
    return ips

def create_socket(protocol: str) -> socket.socket:
    """创建协议对应的socket对象
    
    Args:
        protocol: 'tcp' 或 'udp'
    
    Returns:
        配置好的socket实例
    """
    if protocol.lower() == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    elif protocol.lower() == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")
    
    return sock