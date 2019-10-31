"""
Created on May 29, 2019

@author: ionut
"""

import json
import logging
from tornado.httputil import url_concat
from tornado.testing import AsyncHTTPTestCase, gen_test

import zeus


class APITestCase(AsyncHTTPTestCase):
    """
    Test main HTTP API calls
    """

    def get_app(self):
        """
        Create Tornado main application dev instance for running tests
        :returns: Tornado main application dev instance
        """
        return zeus.make_app(self.io_loop)

    def setUp(self):
        super().setUp()
        logging.getLogger("tornado.access").setLevel(logging.ERROR)
        self.address = "Giroc"
        self.lat = 45.696496
        self.lng = 21.238764
        self.app = self.get_app()

    @gen_test
    def test_forward_geocoding(self):
        """Test that we can forward geocode an address"""
        url = self.get_url("/geocode")
        url = url_concat(url, {"address": self.address})
        response = yield self.http_client.fetch(url)
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertEqual(data["status"], "OK")
        self.assertGreaterEqual(len(data["results"]), 1)
        address = data["results"][0]
        self.assertEqual(address["formatted_address"], "Giroc, Romania")
        self.assertGreaterEqual(address["geometry"]["location"]["lat"], 45)
        self.assertLessEqual(address["geometry"]["location"]["lat"], 46)
        self.assertGreaterEqual(address["geometry"]["location"]["lng"], 21)
        self.assertLessEqual(address["geometry"]["location"]["lng"], 22)

    @gen_test
    def test_reverse_geocoding(self):
        """Test that we can reverse geocode a pair of coordinates"""
        url = self.get_url("/geocode")
        url = url_concat(url, {"lat": "%.6f" % self.lat, "lng": "%.6f" % self.lng})
        response = yield self.http_client.fetch(url)
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertEqual(data["status"], "OK")
        self.assertGreaterEqual(len(data["results"]), 1)
        address = data["results"][0]
        components = address["address_components"]
        for component in components:
            if "locality" in component["types"]:
                self.assertEqual(component["long_name"], "Giroc")
            if "country" in component["types"]:
                self.assertEqual(component["long_name"], "Romania")

    @gen_test
    def test_retrieve_forecast(self):
        """Test that we can retrieve a forecast object"""
        url = self.get_url("/forecast")
        url = url_concat(url, {"lat": "%.6f" % self.lat, "lng": "%.6f" % self.lng})
        response = yield self.http_client.fetch(url)
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode())
        self.assertEqual(data["timezone"], "Europe/Bucharest")
        self.assertIn(data["offset"], [2, 3])
        self.assertIn("currently", data)
        self.assertIn("hourly", data)
