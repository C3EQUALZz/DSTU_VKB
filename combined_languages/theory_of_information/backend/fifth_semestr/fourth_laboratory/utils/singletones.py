class Registry:
    _instance = None
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
        return cls._instance

    def add(self, key: str, value):
        self._data[key] = value

    def get(self, key: str):
        return self._data.get(key)

    def get_all(self):
        return self._data
