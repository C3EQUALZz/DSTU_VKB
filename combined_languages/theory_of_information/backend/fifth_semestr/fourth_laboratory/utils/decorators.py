from functools import wraps
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.singletones import Registry


def register_to_registry(key: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            registry = Registry()
            registry.add(key, result)
            return result
        return wrapper
    return decorator

