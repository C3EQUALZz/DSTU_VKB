from enum import Enum


class SingularityStatus(str, Enum):
    """Status of elliptic curve singularity."""

    NON_SINGULAR = "non_singular"
    SINGULAR = "singular"


