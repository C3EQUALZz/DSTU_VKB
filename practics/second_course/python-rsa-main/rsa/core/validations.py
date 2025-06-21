def assert_int(var: int, name: str) -> None:
    if isinstance(var, int):
        return

    raise TypeError("{} should be an integer, not {}".format(name, var.__class__))
