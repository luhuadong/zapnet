import socket
import threading
from utils.logger import DataLogger

class TCPServer:
    def __init__(self, port, max_conn, output):
        self.port = port
        self.max_conn = max_conn
        self.logger = DataLogger(output)
        
    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(4096)
                if not data: break
                self.logger.write(f"[TCP] From {addr}: {data.hex()}")
        finally:
            conn.close()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(self.max_conn)
        
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