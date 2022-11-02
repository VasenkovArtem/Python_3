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
                if isinstance(json_object[i], dict):
                    setattr(self, attr_name,
                            JSONToPythonWithAttributes(value, []))
                else:
                    setattr(self, attr_name, value)


class ColorizeMixin:
    """Changes the color of the text defined in the object representation
    (method __repr__) when displayed on the console. The text color
    is determined by the repr_color_code attribute.
    Specifies a string representation to display to users"""
    def __str__(self):
        return f'\033[0;{str(self.repr_color_code)}m{repr(self)}'


class Advert(ColorizeMixin, JSONToPythonWithAttributes):
    """Creates ad objects from a dictionary with a required attribute 'title'.
    Raise an error if the product price is negative, if it's absent, sets it
    to zero. Displays a representation of the object as 'title | price ₽'.
    Sets the color of the representation in the attribute 'repr_color_code'"""
    repr_color_code = 32

    def __init__(self, json_object: dict):
        super().__init__(json_object, ['price'])
        # 'title' is a required attribute
        assert hasattr(self, 'title'), "There is no title in adding advert"
        if 'price' in json_object:
            price = json_object['price']
        else:
            price = 0
        self.price = price

    @property
    def price(self) -> float:
        return getattr(self, '_price')

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError('price must be >= 0')
        setattr(self, '_price', value)

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
