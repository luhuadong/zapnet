import socket
import click
import threading
from .utils.logger import DataLogger
from .utils.network import get_protocol_family, get_local_ips

class TCPServer:
    def __init__(self, port, max_conn, output, hex_mode=False):
        self.port = port
        self.max_conn = max_conn
        self.logger = DataLogger(output)
        self.hex_mode = hex_mode
        
    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(4096)
                if not data: break

                formatted = self._format_data(data)
                log_entry = f"[TCP] {addr} => {formatted}"
                self.logger.write(log_entry)
        finally:
            conn.close()
    
    def _format_data(self, data: bytes) -> str:
        """智能数据格式化"""
        if self.hex_mode:
            return ' '.join(f"{b:02x}" for b in data)
        
        try:
            # 尝试解码为UTF-8，保留非ASCII字符
            return data.decode('utf-8', errors='replace')
        except UnicodeDecodeError:
            # 自动回退到HEX显示
            return ' '.join(f"{b:02x}" for b in data)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(self.max_conn)

        bound_ip, bound_port = sock.getsockname()
        click.echo(click.style(
            f"⚡ TCP Server running on {bound_ip}:{bound_port} "
            f"[Max connections: {self.max_conn}]",
            fg="green",
            bold=True
        ))
        click.echo(click.style(f"🌐 Protocol: {get_protocol_family(sock)}", fg="cyan"))
        click.echo(click.style(f"🏠 Local IPs: {', '.join(get_local_ips())}", fg="magenta"))
        click.echo(click.style(
            f"🔍 Listening for incoming connections...",
            fg="blue"
        ))
        
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

class TCPClient:
    def __init__(self, host, port):
        self.addr = (host, port)
        
    def send(self, data=None, hex_data=None, file_path=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.addr)
        
        if file_path:
            with open(file_path, 'rb') as f:
                sock.sendall(f.read())
        elif hex_data:
            sock.sendall(bytes.fromhex(hex_data))
        elif data:
            sock.sendall(data.encode())
            
        sock.close()