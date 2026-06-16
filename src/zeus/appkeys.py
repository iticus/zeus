"""Created on 2026-06-15

@author: iticus
"""

import types

from aiohttp import ClientSession, web


config = web.AppKey("config", types.ModuleType)
cache = web.AppKey("cache", dict)
client = web.AppKey("client", ClientSession)
