import pprint

from src.api import APIAdapter
from src.classes import Airplanes, Dataformating


def main():
    aeroplanes = Airplanes()
    api = APIAdapter()
    form_json = Dataformating()

    user_input = input("здравствуйте хотите получить информацию о самолетах?:")
    if user_input.lower() == "да":
        user_input = input(
            "введите название страны по которой хотите получить информацию(на английском):"
        )
        result = api.get_aeroplanes(user_input)
        data = aeroplanes.format_data(result)
        user_input_int = int(
            input("введите число топ которого по высоте хотите получить:")
        )
        sorted_data = sorted(
            [i for i in data if i["высота"] is not None],
            key=lambda x: x["высота"],
            reverse=True,
        )
        top_x_result = sorted_data[0 : user_input_int + 1]
        pprint.pprint(top_x_result)
        user_input_ans = input("вы хотите получить полный список самолетов?")
        if user_input_ans.lower() == "да":
            user_input_ans = input(
                """в каком виде вы хотите получить список самолетов?
1: вывести в консоль.
2: записать в виде файла.
введите ответ(1 или 2):"""
            )
            if user_input_ans == "1":
                pprint.pprint(data)
            elif user_input_ans == "2":
                form_json.get_json(data)
            else:
                pass
    else:
        print("хорошо, до свидания")


main()

# api = APIAdapter()
# aeroplanes = Airplanes()
#
# if __name__ == '__main__':
#     result = api.get_aeroplanes('Canada')
#     d = aeroplanes.format_data(result)
# pprint.pprint(d)
# form_json = Dataformating()
# form_json.get_json(d)
# sorted_data = sorted([i for i in d if i['высота'] is not None],
#                     key=lambda x: x['высота'], reverse=True)
# pprint.pprint(sorted_data)
