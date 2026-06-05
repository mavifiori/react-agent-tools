from unittest.mock import patch, MagicMock
from src.tools._geocoding import geocode_city


def _mock_response(status_code: int, json_data):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status = MagicMock()
    return mock


def test_geocode_returns_lat_lon():
    mock_resp = _mock_response(200, [{"lat": -23.5, "lon": -46.6}])
    with patch("src.tools._geocoding.requests.get", return_value=mock_resp):
        result = geocode_city("Sao Paulo")
    assert result == (-23.5, -46.6)


def test_geocode_city_not_found():
    mock_resp = _mock_response(200, [])
    with patch("src.tools._geocoding.requests.get", return_value=mock_resp):
        result = geocode_city("CidadeInexistente")
    assert "not found" in result


def test_geocode_invalid_api_key():
    mock_resp = _mock_response(401, {})
    with patch("src.tools._geocoding.requests.get", return_value=mock_resp):
        result = geocode_city("London")
    assert "Invalid API key" in result


def test_geocode_timeout():
    import requests
    with patch("src.tools._geocoding.requests.get", side_effect=requests.exceptions.Timeout):
        result = geocode_city("Tokyo")
    assert "timed out" in result