class ZapnetError(Exception):
    """Base exception class"""
    def __init__(self, message, suggestion=None):
        super().__init__(message)
        self.suggestion = suggestion or "Please check network connection and try again."

class ConnectionError(ZapnetError):
    """Connection exception class"""

class ResolutionError(ZapnetError):
    """Address resolution exception class"""

class TransmissionError(ZapnetError):
    """Data transmission exception class"""