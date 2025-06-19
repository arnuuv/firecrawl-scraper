"""
VC Form Filling AI Agent

An intelligent AI agent that automatically fills out Venture Capital application forms.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.agent import FormFillingAgent
from .core.browser import BrowserManager
from .utils.data_manager import DataManager
from .templates.base import FormTemplate

__all__ = [
    "FormFillingAgent",
    "BrowserManager", 
    "DataManager",
    "FormTemplate"
] 