import click
import sys
import functools
from .tcp_engine import TCPServer, TCPClient
from .udp_engine import UDPServer, UDPClient
from .utils.network import parse_target
from .utils.errors import ZapnetError

def handle_errors(func):
    """装饰器统一处理异常"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZapnetError as e:
            click.secho(f"❌ Error: {e}", fg='red', bold=True)
            if e.suggestion:
                click.secho(f"💡 Tips: {e.suggestion}", fg='yellow')
            sys.exit(1)
        except Exception as e:
            click.secho(f"❌ Unhandled Exception: {str(e)}", fg='magenta')
            sys.exit(2)
    return wrapper

@click.group()
def cli():
    """Network diagnostics toolkit"""

@cli.group()
def tcp():
    """TCP operations"""

@tcp.command()
@handle_errors
@click.pass_context
@click.option("--port", required=True, type=int)
@click.option("--max-conn", default=100, help="Maximum connections")
@click.option("--output", type=click.Path(), help="Save received data")
@click.option("--hex", is_flag=True, help="Display data in hexadecimal")
def server(ctx, port, max_conn, output, hex):
    """Start TCP server"""
    TCPServer(port, max_conn, output, hex_mode=hex).run()

@tcp.command()
@handle_errors
@click.pass_context
@click.option("--target", help="Target IP (host:port)")
@click.option("--host", help="Target Host")
@click.option("--port", type=int, help="Target port")
@click.option("--data", help="Text data to send")
@click.option("--hex", help="Hex data to send")
@click.option("--file", type=click.Path(), help="File to send")
def client(ctx, target, host, port, data, hex, file):
    """TCP client mode"""
    if target and (host or port):
        raise click.UsageError("Cannot use both --target and --host/--port")
    if not target and not (host and port):
        raise click.UsageError("Must specify either --target or both --host and --port")
    
    final_host, final_port = parse_target(target, host, port)
    TCPClient(final_host, final_port).send(data, hex, file)

@cli.group()
def udp():
    """UDP operations"""

@udp.command()
@handle_errors
@click.pass_context
@click.option("--port", required=True, type=int)
@click.option("--output", type=click.Path(), help="Save received data")
@click.option("--hex", is_flag=True, help="Display data in hexadecimal")
@click.option("--broadcast", is_flag=True, help="Enable broadcast")
def server(ctx, port, output, hex, broadcast):
    """UDP server mode"""
    UDPServer(port, output, broadcast, hex_mode=hex).run()

@udp.command()
@handle_errors
@click.pass_context
@click.option("--target", help="Target IP (host:port)")
@click.option("--host", help="Target Host")
@click.option("--port", type=int, help="Target port")
@click.option("--data", help="Text data to send")
@click.option("--hex", help="Hex data to send")
@click.option("--broadcast", is_flag=True, help="Enable broadcast")
def client(ctx, target, host, port, data, hex, broadcast):
    """UDP client mode"""
    if target and (host or port):
        raise click.UsageError("Cannot use both --target and --host/--port")
    if not target and not (host and port):
        raise click.UsageError("Must specify either --target or both --host and --port")
    
    final_host, final_port = parse_target(target, host, port)
    UDPClient(final_host, final_port).send(data, hex, broadcast)
