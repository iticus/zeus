"""
Created on May 29, 2019

@author: ionut
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# Logging config
logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# aiohttp settings
ADDRESS = "0.0.0.0"
PORT = 8000
FOLDER = Path(__file__).parent
TEMPLATE_PATH = FOLDER / "templates"
STATIC_PATH = FOLDER / "static"

# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
