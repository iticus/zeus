"""
Created on May 29, 2019

@author: ionut
"""

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat


class Geocoding:
    """Google Maps based forward & reverse geocoding implementation"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    @coroutine
    def forward_geocode(self, address):
        """
        Retrieve geographic coordinates for given address
        :param address: address to geocode
        :return: geocoding data
        """
        params = {"address": address, "key": self.api_key}
        url = url_concat(self.base_url, params)
        client = AsyncHTTPClient()
        result = yield client.get(url)
        return result

    @coroutine
    def reverse_geocode(self, lat, lng):
        """
        Rertrieve address for given geographic coordinates
        :param lat: latitude data
        :param lng: longitude data
        :return: address data
        """
        latlng = "%.6f,%.6f" % (lat, lng)
        params = {"latlng": latlng, "key": self.api_key}
        url = url_concat(self.base_url, params)
        client = AsyncHTTPClient()
        result = yield client.get(url)
        return result
