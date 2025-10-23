import time
from dataclasses import dataclass


@dataclass
class WeatherData:
    city: str
    temperature_c: float
    humidity: int
    condition: str

    def to_fahrenheit(self) -> float:
        return self.temperature_c * 9 / 5 + 32

    @staticmethod
    def from_fahrenheit(temp_f: float) -> float:
        return (temp_f - 32) * 5 / 9


class WeatherAPI:
    """Interface d'une API météo externe (à mocker dans les tests)."""

    def get_current_weather(self, city: str) -> dict:
        raise NotImplementedError

    def get_forecast(self, city: str, days: int) -> list[dict]:
        raise NotImplementedError


class WeatherService:
    def __init__(self, api: WeatherAPI):
        self.api = api
        self.cache = {}  # { (city, type): (timestamp, data) }
        self.cache_ttl = 3600  # 1h en secondes

    def _is_cache_valid(self, key):
        if key not in self.cache:
            return False
        timestamp, _ = self.cache[key]
        return (time.time() - timestamp) < self.cache_ttl

    def _get_from_cache(self, key):
        _, data = self.cache[key]
        return data

    def _update_cache(self, key, data):
        self.cache[key] = (time.time(), data)

    def get_current_weather(self, city: str) -> WeatherData:
        key = (city, "current")
        if self._is_cache_valid(key):
            return self._get_from_cache(key)

        try:
            data = self.api.get_current_weather(city)
            wd = WeatherData(
                city=city,
                temperature_c=data["temp_c"],
                humidity=data["humidity"],
                condition=data["condition"],
            )
            self._update_cache(key, wd)
            return wd
        except Exception as e:
            raise RuntimeError(f"Erreur API météo: {e}")

    def get_forecast(self, city: str, days: int = 5) -> list[WeatherData]:
        key = (city, f"forecast_{days}")
        if self._is_cache_valid(key):
            return self._get_from_cache(key)

        try:
            data_list = self.api.get_forecast(city, days)
            result = [
                WeatherData(
                    city=city,
                    temperature_c=d["temp_c"],
                    humidity=d["humidity"],
                    condition=d["condition"],
                )
                for d in data_list
            ]
            self._update_cache(key, result)
            return result
        except Exception as e:
            raise RuntimeError(f"Erreur API météo: {e}")
