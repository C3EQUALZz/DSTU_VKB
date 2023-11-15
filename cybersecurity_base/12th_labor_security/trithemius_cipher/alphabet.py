from string import ascii_lowercase, ascii_uppercase, digits, punctuation

whitespace = " \t"
EN = (ascii_lowercase, ascii_uppercase, digits, punctuation, whitespace)
RU = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя", digits, punctuation, whitespace)
UA = ("АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЭЮЯ", "абвгґдеєжзиіїйклмнопрстуфхцчшщьэюя", digits, punctuation, whitespace)


def get_alphabet(lang=None):
    alphabets = {
        "EN": EN,
        "RU": RU,
        "UA": UA
    }

    return alphabets.get(lang, EN)