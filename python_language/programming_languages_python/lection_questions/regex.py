import re

text = """
100 \t ИНФ Информатика
213 \t МАТ Математика
156 \t АНГ Английский
"""

result = filter(lambda x: not x.isspace(), re.split(r"\s+", text))

# Поиск всех элементов с помощью findall
all_numbers = re.findall(r"\d+", text)

# search ищет первое вхождение элемента в строку и возвращает индекс начала и конца соотв.
number = re.search(r"\d+", text)

# match по сути то же самое, что и search, правда natch = ^search
number_match = re.match(r"\d+", text)  # -> None, так как там есть enter

# для изменения текста используется sub
new_text = re.sub(r"\s+", " ", text)


#

def check_numbers(number_str: str):
    """
    check_numbers("+7 989-706-45-96")
    """
    return bool(re.fullmatch(r"\+7 \d{3,}-\d{3,}-\d{2,}-\d{2,}", number_str))


def extract_name():
    emails = """zuck26@facebook.com  
    page33@google.com  
    jeff42@amazon.com"""
    return re.findall(r"(\w+)@(\w+)\.(\w+)", emails)
