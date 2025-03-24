import socket
import click
from .utils.logger import DataLogger
from .utils.network import parse_address

class UDPServer:
    def __init__(self, port, output, broadcast, hex_mode=False):
        self.port = port
        self.logger = DataLogger(output)
        self.broadcast = broadcast
        self.hex_mode = hex_mode
        
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', self.port))

        bound_ip, bound_port = sock.getsockname()
        broadcast_status = "Enabled" if self.broadcast else "Disabled"
        status_color = "yellow" if self.broadcast else "blue"

        click.echo(click.style(
            f"⚡ UDP Server listening on {bound_ip}:{bound_port}",
            fg="green",
            bold=True
        ))
        click.echo(click.style(
            f"📡 Broadcast: {broadcast_status} | "
            f"Buffer size: 4096 bytes",
            fg=status_color
        ))
        click.echo(click.style(
            "🔍 Ready to receive datagrams...",
            fg="blue"
        ))
        
        while True:
            data, addr = sock.recvfrom(4096)
            formatted = self._format_data(data)
            log_entry = f"[TCP] {addr} => {formatted}"
            self.logger.write(log_entry)
    
    def _format_data(self, data: bytes) -> str:
        if self.hex_mode:
            return ' '.join(f"{b:02x}" for b in data)
        
        try:
            return data.decode('utf-8', errors='replace')
        except UnicodeDecodeError:
            return ' '.join(f"{b:02x}" for b in data)

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