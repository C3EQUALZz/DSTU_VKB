def calculate_ttg(t_blast: float, humidity: float, oxygen: float, gas: float) -> float:
    """Теоретическая температура горения, °C (формула ЛР2)."""
    return (
        2405
        + 0.75 * (t_blast - 1200)
        - 5.40 * humidity
        + 43.00 * (oxygen - 21)
        - 52.00 * gas
    )
