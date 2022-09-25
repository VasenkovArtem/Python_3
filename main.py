import json
from keyword import iskeyword


class JSONToPythonWithAttributes:
    """Dynamically adds attributes to an object of this class
    (and its descendants) by reading them from a dictionary called
    json_object. If there are nested dictionaries, defines the corresponding
    attribute as a new instance of this class. Does not add the attributes
    specified in excluded_attributes to the object"""
    def __init__(self, json_object: dict, excluded_attributes: list):
        for i in json_object:
            # if name of attribute matches reserved word
            attr_name = i + '_' * iskeyword(i)
            value = json_object[i]
            if i not in excluded_attributes:
                if type(json_object[i]) == dict:
                    self.__dict__[attr_name] =\
                        JSONToPythonWithAttributes(value, [])
                else:
                    self.__dict__[attr_name] = value


class ColorizeMixin:
    """Changes the color of the text defined in the object representation
    (method __repr__) when displayed on the console. The text color
    is determined by the repr_color_code attribute.
    Specifies a string representation to display to users"""
    def __str__(self):
        return '\033[0;' + str(self.repr_color_code) + 'm' + self.__repr__()


class Advert(ColorizeMixin, JSONToPythonWithAttributes):
    """Creates ad objects from a dictionary with a required attribute 'title'.
    Raise an error if the product price is negative, if it's absent, sets it
    to zero. Displays a representation of the object as 'title | price ₽'.
    Sets the color of the representation in the attribute 'repr_color_code'"""
    repr_color_code = 32

    def __init__(self, json_object: dict):
        super().__init__(json_object, ['price'])
        # 'title' is a required attribute
        assert 'title' in self.__dict__, "There is no title in adding advert"
        if 'price' in json_object:
            self.price = json_object['price']

    @property
    def price(self) -> float:
        if '_price' not in self.__dict__:
            self._price = 0
            return self._price
        else:
            return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError('price must be >= 0')
        self._price = value

    def __repr__(self) -> str:
        return f'{self.title} | {self.price} ₽'


if __name__ == '__main__':
    lesson_str = """{
        "title": "python",
        "price": 10,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        },
        "class": "язык"
    }"""
    lesson = json.loads(lesson_str)
    adv = Advert(lesson)
    print(adv.price)  # Out: 10
    print(adv.location.address)  # Out: город Москва, Лесная, 7
    print(adv)  # Out_green: python | 10 ₽
    adv.repr_color_code = 31
    print(adv)  # Out_red: python | 10 ₽
