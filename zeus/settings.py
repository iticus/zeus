"""
Created on May 29, 2019

@author: ionut
"""

import logging

# Logging config
logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] - %(levelname)s - %(message)s")

# aiohttp settings
ADDRESS = "127.0.0.1"
PORT = 8000
TEMPLATE_PATH = "templates"
STATIC_PATH = "static"

# keys
DARKSKY_API_KEY = "500a0dfb5388a9b9f1d4b431d5767db0"
GOOGLE_API_KEY = "AIzaSyAX_5oYAKeJENjlBGmw1N3lIJjtzgjOKDI"
