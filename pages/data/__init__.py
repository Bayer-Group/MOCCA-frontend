"""
The data upload page
"""

# The layout function has to be imported to be accessed from app.py
from pages.data.layout import get_layout

# Import the callbacks that handle user interatctions (e.g. uploading files, submitting the form, ...)
from pages.data import callbacks
