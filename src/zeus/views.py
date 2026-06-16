"""
Created on May 29, 2019

@author: iticus
"""

import aiohttp_jinja2
from aiohttp import web


from zeus import appkeys
from zeus.weather import OpenWeather
from zeus.geocoding import Geocoding


class BaseView(web.View):
    """Base View to be inherited / implemented by subsequent views"""

    def __init__(self, request):
        super().__init__(request)
        self.cache = request.app[appkeys.cache]  # TODO: replace with redis
        self.config = request.app[appkeys.config]
        self.client = request.app[appkeys.client]


class Home(BaseView):
    """View for "/", render home template"""

    async def get(self):
        return aiohttp_jinja2.render_template("home.html", self.request, context={})


class Weather(BaseView):
    """View for forecast and current weather data"""

    async def get(self):
        """Return forecast data for location"""
        operation = self.request.query.get("operation", "weather")
        lat = self.request.query.get("lat", "")
        lng = self.request.query.get("lng", "")
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return web.json_response(data={"status": "error", "data": "invalid coordinates"}, status=400)
        open_weather = OpenWeather(self.config.WEATHER_API_KEY, session=self.client)
        if operation == "weather":
            data = await open_weather.get_weather(lat, lng)
        else:
            data = await open_weather.get_forecast(lat, lng)
        return web.json_response(data)


class Geocoder(BaseView):
    """View for "/geocode"""

    async def get(self):
        """Return geocoding information (forward/reverse)"""
        geocoding = Geocoding(self.config.GOOGLE_API_KEY, self.client)
        address = self.request.query.get("address", "")
        if address:
            geo = await geocoding.forward_geocode(address)
            return web.json_response(geo)
        else:
            lat = self.request.query.get("lat", "")
            lng = self.request.query.get("lng", "")
            try:
                lat = float(lat)
                lng = float(lng)
            except ValueError:
                return web.json_response(data={"status": "error", "data": "invalid coordinates"}, status=400)
            if not lat or not lng:
                return web.json_response({"error": "provide either address or lat/lng"}, status=400)
            addr = await geocoding.reverse_geocode(lat, lng)
            return web.json_response(addr)
