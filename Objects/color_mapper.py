
def color_mapper(color):
    """
    Функция определения кода цвета по названию
    :param color: Строка с названием цвета
    :return: код цвета RGB
    """
    color = color.upper()
    color_map = {
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),
        'RED': (255, 0, 0),
        'GREEN': (0, 255, 0),
        'BLUE': (0, 0, 255)
    }
    try:
        return color_map[color]
    except KeyError:
        return color_map['WHITE']
