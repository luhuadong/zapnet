import click
from .tcp_engine import TCPServer, TCPClient
from .udp_engine import UDPServer, UDPClient

@click.group()
def cli():
    """Network diagnostics toolkit"""

@cli.group()
def tcp():
    """TCP operations"""

@tcp.command()
@click.option("--port", required=True, type=int)
@click.option("--max-conn", default=100, help="Maximum connections")
@click.option("--output", type=click.Path(), help="Save received data")
@click.option("--hex", is_flag=True, help="Display data in hexadecimal")
def server(port, max_conn, output, hex):
    """Start TCP server"""
    TCPServer(port, max_conn, output, hex_mode=hex).run()

@tcp.command()
@click.option("--host", required=True)
@click.option("--port", required=True, type=int)
@click.option("--data", help="Text data to send")
@click.option("--hex", help="Hex data to send")
@click.option("--file", type=click.Path(), help="File to send")
def client(host, port, data, hex, file):
    """TCP client mode"""
    TCPClient(host, port).send(data, hex, file)

@cli.group()
def udp():
    """UDP operations"""

@udp.command()
@click.option("--port", required=True, type=int)
@click.option("--output", type=click.Path(), help="Save received data")
@click.option("--hex", is_flag=True, help="Display data in hexadecimal")
@click.option("--broadcast", is_flag=True, help="Enable broadcast")
def server(port, output, hex, broadcast):
    """UDP server mode"""
    UDPServer(port, output, broadcast, hex_mode=hex).run()

@udp.command()
@click.option("--target", required=True)
@click.option("--data", help="Text data to send")
@click.option("--hex", help="Hex data to send")
@click.option("--broadcast", is_flag=True, help="Enable broadcast")
def client(target, data, hex, broadcast):
    """UDP client mode"""
    UDPClient.parse_target(target).send(data, hex, broadcast)