"""
Created on May 29, 2019

@author: ionut
"""

import aiohttp_jinja2
from aiohttp import web


from darksky import DarkSky
from geocoding import Geocoding


class BaseView(web.View):
    """Base View to be inherited / implemented by subsequent views"""

    def __init__(self, request):
        super().__init__(request)
        self.cache = request.app.cache  # TODO: simple in-memory cache
        self.config = request.app.config
        self.client = request.app.client


class Home(BaseView):
    """View for "/", render home template"""

    async def get(self):
        return aiohttp_jinja2.render_template("home.html", self.request, context={})


class Forecast(BaseView):
    """View for "/forecast"""

    async def get(self):
        """Return forecast data for location"""
        lat = self.request.query.get("lat", "")
        lng = self.request.query.get("lng", "")
        dark_sky = DarkSky(self.config.DARKSKY_API_KEY, self.client)
        forecast = await dark_sky.get_forecast(lat, lng)
        return web.json_response(forecast)


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
            if not lat or not lng:
                return web.json_response({"error": "provide either address or lat/lng"}, status=400)
            addr = await geocoding.reverse_geocode(lat, lng)
            return web.json_response(addr)
