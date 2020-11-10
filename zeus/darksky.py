"""
Created on May 29, 2019

@author: ionut
"""

from aiohttp import ClientSession
from urllib.parse import urljoin


class DarkSky:
    """Dark Sky weather forecast async implementation"""

    def __init__(self, api_key, session=None):
        self.api_key = api_key
        self.base_url = "https://api.darksky.net"
        self.session = session

    async def get_forecast(self, lat, lng):
        """
        Retrieve weather forecast
        :param lat: latitude for location
        :param lng: longitude for location
        :return: forecast data
        """
        url = urljoin(self.base_url, "forecast/%s/" % self.api_key)
        url = urljoin(url, "%s,%s?extend=hourly" % (lat, lng))
        if not self.session:
            self.session = ClientSession()
        response = await self.session.get(url)
        data = await response.json(content_type=None)  # fix for text/plain
        return data
