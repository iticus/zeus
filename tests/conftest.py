"""
Created on Nov 10, 2020

@author: ionut
"""

from pytest import fixture
from main import make_app


pytest_plugins = "aiohttp.pytest_plugin"


@fixture
def zeus(loop, aiohttp_client):
    app = make_app()
    return loop.run_until_complete(aiohttp_client(app))
