"""
Created on May 29, 2019

@author: ionut
"""

import logging

# Logging config
logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                    format="[%(asctime)s] - %(levelname)s - %(message)s")
logging.getLogger("tornado.access").setLevel(logging.WARNING)

# Tornado settings
ADDRESS = "127.0.0.1"
PORT = 8000
TEMPLATE_PATH = "templates"
STATIC_PATH = "static"
DARKSKY_API_KEY = ""
GOOGLE_API_KEY = ""
