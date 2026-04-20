from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.classes import Airplanes, Coordinates, Dataformating


class TestAirplanes:

    @pytest.fixture
    def sample_data(self):
        return {
            "states": [
                [
                    "ABC123",
                    "RA1234",
                    "Russia",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    10000.0,
                ],
                [
                    "DEF456",
                    "RA5678",
                    "USA",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    5000.0,
                ],
                [
                    "GHI789",
                    "RA9012",
                    "Germany",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ]
        }

    def test_format_data(self, sample_data):
        airplanes = Airplanes()
        result = airplanes.format_data(sample_data)

        assert len(result) == 3
        assert result[0]["страна"] == "Russia"
        assert result[0]["бортовой номер"] == "ABC123"
        assert result[0]["номер рейса"] == "RA1234"
        assert result[0]["высота"] == 10000.0
        assert result[2]["высота"] is None

    def test_format_data_empty(self):
        airplanes = Airplanes()
        result = airplanes.format_data({"states": []})
        assert result == []

    def test_get_api_clear(self):
        airplanes = Airplanes()
        airplanes.api = "test_api"
        assert airplanes.get_api_clear() == "test_api"

    def test_eq(self):
        airplanes = Airplanes()
        airplanes.api = 100
        other = MagicMock()
        other.api = 100
        result = airplanes.__eq__(other)
        assert result == NotImplemented

    def test_lt(self):
        a1 = Airplanes()
        a2 = Airplanes()
        a1.api = 100
        a2.api = 200
        assert a1.__lt__(a2) is True
        assert a2.__lt__(a1) is False

    def test_gt(self):
        a1 = Airplanes()
        a2 = Airplanes()
        a1.api = 200
        a2.api = 100
        assert a1.__gt__(a2) is True
        assert a2.__gt__(a1) is False


class TestDataformating:

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_get_json(self, mock_makedirs, mock_file):
        formatter = Dataformating()
        test_data = {"test": "data"}

        formatter.get_json(test_data)

        mock_makedirs.assert_called_once_with("json_files", exist_ok=True)
        mock_file.assert_called_once_with("json_files/data.json", "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_get_json_with_cyrillic(self, mock_makedirs, mock_file):
        formatter = Dataformating()
        test_data = {"страна": "Россия", "высота": 10000}

        formatter.get_json(test_data)

        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        assert "Россия" in written_data

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_get_json_empty_data(self, mock_makedirs, mock_file):
        formatter = Dataformating()
        formatter.get_json({})

        mock_makedirs.assert_called_once()
        mock_file.assert_called_once()


class TestCoordinates:

    def test_abstract_methods(self):
        with pytest.raises(TypeError):
            Coordinates()


def test_airplanes_inheritance():
    airplanes = Airplanes()
    assert isinstance(airplanes, Coordinates)
    assert isinstance(airplanes, Airplanes)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
