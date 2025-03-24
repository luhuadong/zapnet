import socket
from utils.logger import DataLogger
from utils.network import parse_address

class UDPServer:
    def __init__(self, port, output, broadcast):
        self.port = port
        self.logger = DataLogger(output)
        self.broadcast = broadcast
        
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', self.port))
        
        while True:
            data, addr = sock.recvfrom(4096)
            log_entry = f"[UDP] From {addr}: {data.hex()}"
            self.logger.write(log_entry)

class UDPClient:
    @staticmethod
    def parse_target(target):
        host, port = target.rsplit(":", 1)
        return UDPClient(host, int(port))
    
    def __init__(self, host, port):
        self.addr = (host, port)
        
    def send(self, data=None, hex_data=None, broadcast=False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
        if data:
            sock.sendto(data.encode(), self.addr)
        elif hex_data:
            sock.sendto(bytes.fromhex(hex_data), self.addr)
            
        sock.close()