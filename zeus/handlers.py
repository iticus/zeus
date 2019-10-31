"""
Created on May 29, 2019

@author: ionut
"""

from tornado.web import RequestHandler
from tornado.gen import coroutine

from darksky import DarkSky
from geocoding import Geocoding


class BaseHandler(RequestHandler):
    """Base Handler to be inherited / implemented by subsequent handlers"""

    def initialize(self):
        self.cache = {}   # TODO: simple in-memory cache
        self.config = self.application.config


class HomeHandler(BaseHandler):
    """Request Handler for "/", render home template"""

    def get(self):
        self.render("home.html")


class ForecastHandler(BaseHandler):
    """Request Handler for "/forecast"""

    @coroutine
    def get(self):
        """Return forecast data for location"""
        lat = self.get_query_argument("lat", "")
        lng = self.get_query_argument("lng", "")
        dark_sky = DarkSky(self.config.DARKSKY_API_KEY)
        forecast = yield dark_sky.get_forecast(lat, lng)
        self.finish(forecast)


class GeocodingHandler(BaseHandler):
    """Request Handler for "/geocode"""

    @coroutine
    def get(self):
        """Return geocoding information (forward/reverse)"""
        geocoding = Geocoding(self.config.GOOGLE_API_KEY)
        address = self.get_query_argument("address", "")
        if address:
            geo = yield geocoding.forward_geocode(address)
            return self.finish(geo)
        else:
            lat = self.get_query_argument("lat", "")
            lng = self.get_query_argument("lng", "")
            if not lat or not lng:
                self.set_status(400)
                return self.finish({"error": "provide either address or lat/lng"})
            addr = yield geocoding.reverse_geocode(lat, lng)
            return self.finish(addr)
