from pathlib import Path
from functools import lru_cache


class CommonSettings:
    ...


class DatabaseSettings:
    ...


class PerformanceSettings:
    select_benchmark: Path = Path(__file__).parent.parent.parent / "performance" / "select_benchmark.csv"


class Settings:
    performance: PerformanceSettings = PerformanceSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
