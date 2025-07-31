"""
AxoDen Client - Custom exceptions
"""


class AxoDenError(Exception):
    """Base exception for AxoDen client errors"""
    pass


class AuthenticationError(AxoDenError):
    """Raised when authentication fails"""
    pass


class MethodologyNotFoundError(AxoDenError):
    """Raised when no methodology recommendation is found"""
    pass


class ConfigurationError(AxoDenError):
    """Raised when configuration is invalid"""
    pass


class NetworkError(AxoDenError):
    """Raised when network communication fails"""
    pass