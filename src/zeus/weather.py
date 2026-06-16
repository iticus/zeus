"""
Created on May 29, 2019

@author: iticus
"""

from aiohttp import ClientSession
from urllib.parse import urljoin


class OpenWeather:
    """Open Weather async implementation"""

    def __init__(self, api_key: str, version: str = "2.5", session: ClientSession | None = None):
        self.api_key = api_key
        self.version = version
        self.base_url = "https://api.openweathermap.org/data/"
        self.session = session

    async def api_call(self, path: str, lat: float, lng: float) -> dict:
        url = urljoin(self.base_url, f"{self.version}/{path}")
        if not self.session:
            self.session = ClientSession()
        params = {"lat": lat, "lon": lng, "appid": self.api_key}
        response = await self.session.get(url, params=params)
        data = await response.json()
        return data

    async def get_weather(self, lat: float, lng: float) -> dict:
        """
        Retrieve current weather for specified location
        :param lat: latitude for location
        :param lng: longitude for location
        :return: current weather data
        """
        return await self.api_call("weather", lat, lng)

    async def get_forecast(self, lat: float, lng: float) -> dict:
        """
        Retrieve weather forecast
        :param lat: latitude for location
        :param lng: longitude for location
        :return: forecast data
        """
        return await self.api_call("forecast", lat, lng)
