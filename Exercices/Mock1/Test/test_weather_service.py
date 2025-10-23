import time
import pytest
from unittest.mock import Mock

import sys, os

# ajoute le dossier parent (Mock1) au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from weather_service import WeatherService, WeatherAPI, WeatherData


@pytest.fixture
def api():
    return Mock(spec=WeatherAPI)


@pytest.fixture
def service(api):
    return WeatherService(api)


def test_get_current_weather_success(service, api):
    api.get_current_weather.return_value = {
        "temp_c": 20,
        "humidity": 50,
        "condition": "Sunny",
    }
    result = service.get_current_weather("Paris")
    assert result.temperature_c == 20
    assert result.condition == "Sunny"
    api.get_current_weather.assert_called_once_with("Paris")


def test_get_forecast_success(service, api):
    api.get_forecast.return_value = [
        {"temp_c": 22, "humidity": 55, "condition": "Cloudy"},
        {"temp_c": 18, "humidity": 60, "condition": "Rain"},
    ]
    result = service.get_forecast("Lyon", 2)
    assert len(result) == 2
    assert result[1].condition == "Rain"
    api.get_forecast.assert_called_once_with("Lyon", 2)


def test_cache_prevents_repeated_calls(service, api):
    api.get_current_weather.return_value = {
        "temp_c": 25,
        "humidity": 40,
        "condition": "Clear",
    }
    service.get_current_weather("Paris")
    service.get_current_weather("Paris")
    api.get_current_weather.assert_called_once()


def test_cache_expires_after_one_hour(service, api):
    api.get_current_weather.return_value = {
        "temp_c": 20,
        "humidity": 50,
        "condition": "Sunny",
    }
    service.get_current_weather("Paris")
    api.get_current_weather.reset_mock()

    # Simuler expiration
    for k in service.cache.keys():
        service.cache[k] = (time.time() - 4000, service.cache[k][1])

    service.get_current_weather("Paris")
    api.get_current_weather.assert_called_once()


def test_temperature_conversion():
    wd = WeatherData("Paris", 0, 50, "Snow")
    assert wd.to_fahrenheit() == pytest.approx(32)
    assert WeatherData.from_fahrenheit(212) == pytest.approx(100)


def test_api_timeout_exception(service, api):
    api.get_current_weather.side_effect = TimeoutError("timeout")
    with pytest.raises(RuntimeError):
        service.get_current_weather("Paris")


def test_api_404_exception(service, api):
    api.get_current_weather.side_effect = Exception("404 Not Found")
    with pytest.raises(RuntimeError):
        service.get_current_weather("Lille")


def test_api_500_exception(service, api):
    api.get_forecast.side_effect = Exception("500 Internal Server Error")
    with pytest.raises(RuntimeError):
        service.get_forecast("Nice")


def test_forecast_cache(service, api):
    api.get_forecast.return_value = [
        {"temp_c": 21, "humidity": 45, "condition": "Windy"}
    ]
    service.get_forecast("Bordeaux", 1)
    service.get_forecast("Bordeaux", 1)
    api.get_forecast.assert_called_once()


def test_multiple_cities_cache_independent(service, api):
    api.get_current_weather.return_value = {
        "temp_c": 10,
        "humidity": 80,
        "condition": "Fog",
    }
    service.get_current_weather("Paris")
    service.get_current_weather("Lyon")
    assert api.get_current_weather.call_count == 2


def test_forecast_with_different_days(service, api):
    api.get_forecast.return_value = [
        {"temp_c": 25, "humidity": 40, "condition": "Sunny"}
    ]
    service.get_forecast("Paris", 3)
    service.get_forecast("Paris", 5)
    assert api.get_forecast.call_count == 2


def test_network_error(service, api):
    api.get_current_weather.side_effect = ConnectionError("Network down")
    with pytest.raises(RuntimeError):
        service.get_current_weather("Toulouse")
