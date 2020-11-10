"""
Created on May 29, 2019

@author: ionut
"""

from aiohttp import ClientSession


class Geocoding:
    """Google Maps based forward & reverse geocoding implementation"""

    def __init__(self, api_key, client=None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.client = client

    async def forward_geocode(self, address):
        """
        Retrieve geographic coordinates for given address
        :param address: address to geocode
        :return: geocoding data
        """
        params = {"address": address, "key": self.api_key}
        if not self.client:
            self.client = ClientSession()
        response = await self.client.get(self.base_url, params=params)
        data = await response.json()
        return data

    async def reverse_geocode(self, lat, lng):
        """
        Retrieve address for given geographic coordinates
        :param lat: latitude data
        :param lng: longitude data
        :return: address data
        """
        latlng = "%.6f,%.6f" % (float(lat), float(lng))
        params = {"latlng": latlng, "key": self.api_key}
        if not self.client:
            self.client = ClientSession()
        response = await self.client.get(self.base_url, params=params)
        data = await response.json()
        return data
