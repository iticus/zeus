"""
Created on May 29, 2019

@author: ionut
"""

from aiohttp.test_utils import TestClient


lat = 45.696496
lng = 21.238764
address = "Giroc"


async def test_shutdown(zeus_app: TestClient) -> None:
    """Test that the homepage responds with 200 and contains the service name"""
    await zeus_app.app.shutdown()


async def test_homepage(zeus_app):
    response = await zeus_app.get("/")
    assert response.status == 200
    text = await response.text()
    assert "Zeus Weather" in text
    assert "error" not in text


async def test_forward_geocoding(zeus_app) -> None:
    """Test that we can forward geocode an address"""
    response = await zeus_app.get("/geocode", params={"address": address})
    assert response.status == 200
    data = await response.json()
    assert data["status"] == "OK"
    assert len(data["results"]) >= 1
    addr = data["results"][0]
    assert addr["formatted_address"] == "Giroc, Romania"
    assert addr["geometry"]["location"]["lat"] >= 45
    assert addr["geometry"]["location"]["lat"] < 46
    assert addr["geometry"]["location"]["lng"] >= 21
    assert addr["geometry"]["location"]["lng"] < 22


async def test_reverse_geocoding(zeus_app) -> None:
    """Test that we can reverse geocode a pair of coordinates"""
    response = await zeus_app.get("/geocode", params={"lat": "%.6f" % lat, "lng": "%.6f" % lng})
    assert response.status == 200
    data = await response.json()
    assert data["status"] == "OK"
    assert len(data["results"]) >= 1
    addr = data["results"][0]
    components = addr["address_components"]
    for component in components:
        if "locality" in component["types"]:
            assert component["long_name"] == "Giroc"
        if "country" in component["types"]:
            assert component["long_name"] == "Romania"


async def test_retrieve_forecast(zeus_app) -> None:
    """Test that we can retrieve a forecast object"""
    response = await zeus_app.get("/forecast", params={"lat": "%.6f" % lat, "lng": "%.6f" % lng})
    assert response.status == 200
    data = await response.json()
    assert data["timezone"], "Europe/Bucharest"
    assert data["offset"] in [2, 3]
    assert "currently" in data
    assert "hourly" in data
