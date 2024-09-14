from datetime import datetime


def hello(name):
    a = datetime.now().hour
    if 0 <= a < 6:
        hi = f"Доброй ночи, {name}!👇"
    elif 6 <= a < 12:
        hi = f"Доброе утро, {name}!👇"
    elif 12 <= a < 18:
        hi = f"Добрый день, {name}!👇"
    else:
        hi = f"Добрый вечер, {name}!👇"
    return hi
