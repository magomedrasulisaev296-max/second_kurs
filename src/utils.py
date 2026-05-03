import json
import os


class Dataformating:

    def get_json(self, data):
        os.makedirs("json_files", exist_ok=True)
        with open("json_files/data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
