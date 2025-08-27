import re
from typing import Final

PASSWORD_MIN_LEN: Final[int] = 6

MIN_TELEGRAM_ID_VALUE: Final[int] = 1
MIN_TELEGRAM_USERNAME_LENGTH: Final[int] = 1
MAX_TELEGRAM_USERNAME_LENGTH: Final[int] = 128

USERNAME_MIN_LEN: Final[int] = 1
USERNAME_MAX_LEN: Final[int] = 125

# Pattern for validating a username:
# - starts with a letter (A-Z, a-z) or a digit (0-9)
PATTERN_START: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Zа-яА-Я0-9]",  # noqa: RUF001
)
# - can contain multiple special characters . - _ between letters and digits,
PATTERN_ALLOWED_CHARS: Final[re.Pattern[str]] = re.compile(
    r"[a-zA-Zа-яА-Я0-9._-]*", # noqa: RUF001
)
#   but only one special character can appear consecutively
PATTERN_NO_CONSECUTIVE_SPECIALS: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Zа-яА-Я0-9]+([._-]?[a-zа-яА-ЯA-Z0-9]+)*[._-]?$",  # noqa: RUF001
)
# - ends with a letter (A-Z, a-z) or a digit (0-9)
PATTERN_END: Final[re.Pattern[str]] = re.compile(
    r".*[a-zA-Zа-яА-Я0-9]$",  # noqa: RUF001
)
