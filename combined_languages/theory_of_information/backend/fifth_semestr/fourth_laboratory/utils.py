from functools import wraps


class Report:
    def __init__(self):
        self.__data = {}

    def add(self, key: str, value: str) -> None:
        self.__data[key] = value

    def get(self, key: str) -> str:
        return self.__data.get(key)

    def get_all(self) -> dict[str, str]:
        return self.__data


def collect_data(report: Report):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            report.add(func.__name__, result)
            return result

        return wrapper

    return decorator
