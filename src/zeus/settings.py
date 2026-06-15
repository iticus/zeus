"""
Created on May 29, 2019

@author: ionut
"""

import logging

# Logging config
logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] - %(levelname)s - %(message)s")

# aiohttp settings
ADDRESS = "0.0.0.0"
PORT = 8000
TEMPLATE_PATH = "templates"
STATIC_PATH = "static"

# keys - to be filled
DARKSKY_API_KEY = "a2f53b37d9b8a7fb4eb1b816832af236"
GOOGLE_API_KEY = "AIzaSyBF7V22dXa7iE1tYg3sGzZlrWohqJ7ELKU"
