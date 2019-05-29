"""
Created on May 29, 2019

@author: ionut
"""

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient


class DarkSky:
    """Dark Sky weather forecast async implementation"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.darksky.net/forecast/"

    @coroutine
    def get_forecast(self, lat, lng):
        """
        Retrieve weather forecast
        :param lat: latitude for location
        :param lng: longitude for location
        :return: forecast data
        """
        url = self.base_url + self.api_key + "/"
        url = url + "%s,%s?extend=hourly" % (lat, lng)
        client = AsyncHTTPClient()
        response = yield client.fetch(url)
        return response.body
