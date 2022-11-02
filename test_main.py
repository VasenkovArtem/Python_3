from main import Advert
import json


def check_example(str_object: str, attributes: list, values: list,
                  error: bool, color_code: int, color: str) -> bool:
    json_object = json.loads(str_object)
    try:
        adv = Advert(json_object)
    except ValueError:
        return error
    else:
        flag = True
        var = vars(adv)
        for i in range(len(attributes)):
            value = values[i]
            if attributes[i].split('.')[0] == 'location':
                attribute = attributes[i].split('.')[1]
                location_var = vars(var['location'])
                flag *= (location_var[attribute] == value)
            elif attributes[i] == 'price':
                flag *= (adv.price == value)
            else:
                attribute = attributes[i]
                flag *= (var[attribute] == value)
        adv.repr_color_code = color_code
        print(adv)
        result = input(f'\033[mIs adv {color}? Press y or n: ')
        flag *= (result == 'y')
        return bool(flag)


if __name__ == '__main__':
    adverts = [
        """{
            "title": "iPhone X",
            "price": 100,
            "location": {
                "address": "город Самара, улица Мориса Тореза, 50",
                "metro_stations": ["Спортивная", "Гагаринская"]
            }
        }""",
        """{
            "title": "Вельш-корги",
            "price": 1000,
            "class": "dogs",
            "location": {
                "address":
                "сельское поселение Ельдигинское, поселок санатория Тишково"
            }
        }""",
        """{
            "title": "python",
            "price": 0,
            "location": {
                "address": "город Москва, Лесная, 7",
                "metro_stations": ["Белорусская"]
            }
        }""",
        """{
            "title": "work on factory",
            "price": -250
        }""",
        """{
            "title": "Бублик",
            "price": 10,
            "class": "food",
            "location": {
                "address": "улица Пса Барбоса, 22"
            }
        }""",
        """{
            "title": "python"
        }"""
    ]
    attributes = [
        ['title', 'price', 'location.address', 'location.metro_stations'],
        ['title', 'price', 'class_', 'location.address'],
        ['title', 'price', 'location.address', 'location.metro_stations'],
        ['title', 'price'],
        ['title', 'price', 'class_', 'location.address'],
        ['title', 'price']
    ]
    values = [
        ['iPhone X', 100, 'город Самара, улица Мориса Тореза, 50',
         ['Спортивная', 'Гагаринская']],
        ['Вельш-корги', 1000, 'dogs',
         'сельское поселение Ельдигинское, поселок санатория Тишково'],
        ['python', 0, 'город Москва, Лесная, 7', ['Белорусская']],
        ['work on factory', -250],
        ['Бублик', 10, 'food', 'улица Пса Барбоса, 22'],
        ['python', 0]
    ]
    errors = [False, False, False, True, False, False]
    repr_color_codes = [30, 31, 32, 33, 34, 35]
    colors = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Purple']
    for i in range(len(adverts)):
        result = check_example(adverts[i], attributes[i], values[i],
                               errors[i], repr_color_codes[i], colors[i])
        print(f"\033[mTest No {i+1}. Result: {result}")
