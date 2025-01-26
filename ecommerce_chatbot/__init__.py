"""E-commerce chatbot package."""

from .chatbot import create_chatbot, get_initial_message
from .inventory import INVENTORY

__all__ = ['create_chatbot', 'get_initial_message', 'INVENTORY']
