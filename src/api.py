import logging
import time
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.INFO)


class API(ABC):
    @abstractmethod
    def get_aeroplanes(self):
        pass


class APIAdapter(API):
    def __init__(self):
        self.__openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.__opensky_url = "https://opensky-network.org/api/states/all"
        self.__session = requests.Session()

        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )
        self.__session.mount("https://", HTTPAdapter(max_retries=retries))

        self.__session.headers.update(
            {
                "User-Agent": "MyAwesomeApp/2.0 (magomedrasulisaev296@gmail.com)"  # Лучше указать почту
            }
        )

    def get_aeroplanes(self, country: str):
        logging.info(f"Ищем координаты для: {country}")

        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            resp = self.__session.get(
                self.__openstreetmap_url, params=params_nominatim, timeout=10
            )
            resp.raise_for_status()

            data = resp.json()

            if not data:
                logging.error(f"Страна '{country}' не найдена в Nominatim")
                return None

            bbox = data[0].get("boundingbox")
            if not bbox or len(bbox) < 4:
                logging.error("Не удалось получить boundingbox")
                return None

            lamin, lamax, lomin, lomax = map(float, bbox)

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка сети при запросе к Nominatim: {e}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            logging.error(f"Ошибка парсинга ответа Nominatim: {e}")
            return None

        logging.info("Ждем 2 секунды, чтобы не получить бан...")
        time.sleep(2)

        params_opensky = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax,
        }

        try:
            logging.info(f"Запрашиваем самолеты в зоне: {params_opensky}")
            resp = self.__session.get(
                self.__opensky_url, params=params_opensky, timeout=15
            )
            resp.raise_for_status()

            aeroplanes_data = resp.json()

            if "states" not in aeroplanes_data:
                logging.warning(
                    "В ответе OpenSky нет ключа 'states'. Возможно, лимит запросов или пусто."
                )
                return None

            states = aeroplanes_data["states"]
            count = len(states) if states else 0
            logging.info(f"Найдено самолетов: {count}")

            return aeroplanes_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка сети OpenSky: {e}")
            return None
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
            return None
