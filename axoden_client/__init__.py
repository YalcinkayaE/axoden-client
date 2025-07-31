"""
AxoDen Client - Bridge between AxoDen's AI guidance system and Claude Code
"""

__version__ = "0.1.0"
__author__ = "Luminescence Limited"

from .client import AxoDenClient
from .config import AxoDenConfig
from .exceptions import AxoDenError, AuthenticationError, MethodologyNotFoundError

__all__ = [
    "AxoDenClient",
    "AxoDenConfig", 
    "AxoDenError",
    "AuthenticationError",
    "MethodologyNotFoundError",
]