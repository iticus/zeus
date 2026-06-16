"""
Created on May 29, 2019

@author: ionut
"""

from aiohttp.test_utils import TestClient


lat = 45.696496
lng = 21.238764
address = "Giroc"


async def test_homepage(zeus_app: TestClient) -> None:
    response = await zeus_app.get("/")
    assert response.status == 200
    text = await response.text()
    assert "Zeus Weather" in text
    assert "error" not in text


async def test_forward_geocoding(zeus_app: TestClient) -> None:
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


async def test_reverse_geocoding(zeus_app: TestClient) -> None:
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


async def test_retrieve_weather(zeus_app: TestClient) -> None:
    """Test that we can retrieve the current weather data"""
    response = await zeus_app.get("/weather", params={"lat": lat, "lng": lng})
    assert response.status == 200
    data = await response.json()
    assert data["timezone"] in [7200, 10800], f"expected Europe/Bucharest timezone offsets in {data}"
    assert "weather" in data, f"no weather data found in {data}"
    assert "main" in data, f"no main data found in {data}"
    assert "wind" in data, f"no wind data found in {data}"
    assert "clouds" in data, f"no clouds data found in {data}"
    assert "temp" in data["main"], f"no main temp data found in {data}"


async def test_retrieve_forecast(zeus_app: TestClient) -> None:
    """Test that we can retrieve a forecast object"""
    response = await zeus_app.get("/weather", params={"lat": lat, "lng": lng, "operation": "forecast"})
    assert response.status == 200
    data = await response.json()
    assert "list" in data, f"no forecast data available in {data}"
    for item in data["list"]:
        assert isinstance(item["dt"], int), f"invalid dt in {item}"
        assert isinstance(item["dt"], int), f"invalid dt in {item}"
        assert "main" in item, f"no main data found in {item}"
        assert "temp" in item["main"], f"no temp data found in {item}"
