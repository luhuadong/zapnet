import socket
import click
import os
import threading
from .utils.logger import DataLogger
from .utils.network import get_protocol_family, get_local_ips
from .utils.errors import (
    ConnectionError,
    ResolutionError,
    TransmissionError
)

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
    def __init__(self, host, port, timeout=5):
        try:
            # DNS解析与预连接检查
            self.addr = self._resolve_address(host, port)
            self.timeout = timeout
        except socket.gaierror as e:
            raise ResolutionError(
                f"Unable to resolve host address {host}",
                suggestion="Please check that the hostname is correct, or try using the IP address."
            ) from e

    def _resolve_address(self, host, port):
        """执行带错误处理的地址解析"""
        try:
            info = socket.getaddrinfo(
                host, port,
                family=socket.AF_UNSPEC,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP
            )
            return info[0][4]  # 取第一个结果 (host, port)
        except socket.gaierror as e:
            if "nodename nor servname" in str(e):
                msg = f"Unknown host or service: {host}:{port}"
            else:
                msg = f"Address resolution failed: {host}:{port}"
            raise ResolutionError(msg) from e
        
    def send(self, data=None, hex_data=None, file_path=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        # 连接阶段
        try:
            click.echo(f"🔄 Connecting {self.addr[0]}:{self.addr[1]} ...")
            sock.connect(self.addr)
            click.echo("✅ Connection established successfully.")
        except ConnectionRefusedError:
            raise ConnectionError(
                "Connection refused",
                suggestion="Please confirm that the target service is running and the port is correct."
            )
        except socket.timeout:
            raise ConnectionError(
                "Connection timeout",
                suggestion="Check firewall settings or increase timeout (--timeout)."
            )
        except OSError as e:
            if "Network is unreachable" in str(e):
                raise ConnectionError("Network unreachable") from e
            raise

        # 数据传输阶段
        try:
            if file_path:
                self._send_file(sock, file_path)
            elif hex_data:
                sock.sendall(bytes.fromhex(hex_data))
            elif data:
                sock.sendall(data.encode())
            
            click.echo("📤 Data sent successfully.")
        except BrokenPipeError:
            raise TransmissionError(
                "Unexpected connection interruption",
                suggestion="Please check network stability."
            )
        except Exception as e:
            raise TransmissionError(f"Data transfer failed: {str(e)}") from e
        finally:
            sock.close()
        
    def _send_file(self, sock, path):
        """带进度显示的文件传输"""
        try:
            total = os.path.getsize(path)
            with open(path, 'rb') as f, click.progressbar(length=total, label='📂 Sending file') as bar:
                for chunk in iter(lambda: f.read(4096), b''):
                    sock.sendall(chunk)
                    bar.update(len(chunk))
        except FileNotFoundError:
            raise TransmissionError(f"File does not exist: {path}")
        except PermissionError:
            raise TransmissionError(f"No permission to read file: {path}")
        