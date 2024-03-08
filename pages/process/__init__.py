"""
The data processing page
"""

# The layout function has to be imported to be accessed from app.py
from pages.process.layout import get_layout

# Import the callbacks that handle user interatctions (e.g. uploading files, submitting the form, ...)
from pages.process import callbacks