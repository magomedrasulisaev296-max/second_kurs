from unittest.mock import MagicMock, patch

from requests.exceptions import RequestException

from src.api import APIAdapter


def test_get_aeroplanes_success():
    with patch("time.sleep"), patch("requests.Session.get") as mock_get:
        api = APIAdapter()

        mock_nominatim = MagicMock()
        mock_nominatim.json.return_value = [{"boundingbox": ["55", "56", "37", "38"]}]

        mock_opensky = MagicMock()
        mock_opensky.json.return_value = {"states": [["abc", "RA123", "Russia"]]}

        mock_get.side_effect = [mock_nominatim, mock_opensky]

        result = api.get_aeroplanes("Russia")
        assert result is not None


def test_country_not_found():
    with patch("time.sleep"), patch("requests.Session.get") as mock_get:
        api = APIAdapter()
        mock_get.return_value.json.return_value = []
        assert api.get_aeroplanes("X") is None


def test_network_error():
    with patch("time.sleep"), patch("requests.Session.get") as mock_get:
        api = APIAdapter()
        mock_get.side_effect = RequestException("Error")
        assert api.get_aeroplanes("Russia") is None


def test_no_states_key():
    with patch("time.sleep"), patch("requests.Session.get") as mock_get:
        api = APIAdapter()

        mock_nominatim = MagicMock()
        mock_nominatim.json.return_value = [{"boundingbox": ["55", "56", "37", "38"]}]

        mock_opensky = MagicMock()
        mock_opensky.json.return_value = {}

        mock_get.side_effect = [mock_nominatim, mock_opensky]

        assert api.get_aeroplanes("Russia") is None
