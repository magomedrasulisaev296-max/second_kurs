import json
import os
from abc import ABC, abstractmethod


class Coordinates(ABC):
    api = None

    @abstractmethod
    def format_data(self):
        pass

    @abstractmethod
    def get_api_clear(self):
        pass


class Airplanes(Coordinates):
    def __init__(self):
        pass

    def format_data(self, data):
        result = []
        for i in data["states"]:
            bort_number = i[0]
            rais_1 = i[1]
            country = i[2]
            geo_altitude = i[13]
            result.append(
                {
                    "страна": country,
                    "бортовой номер": bort_number,
                    "номер рейса": rais_1,
                    "высота": geo_altitude,
                }
            )
        return result


    def get_api_clear(self):
        return self.api

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.api == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Coordinates):
            return self.api < other.api
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Coordinates):
            return self.api > other.api
        return NotImplemented


class Dataformating(Airplanes):

    def get_json(self, data):
        os.makedirs("json_files", exist_ok=True)
        with open("json_files/data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
