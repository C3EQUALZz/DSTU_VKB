import logging
import os
import struct

import rsa.helpers.decorators as decorators
from rsa.helpers import common, transform

logger = logging.getLogger(__name__)


@decorators.log_decorator(logger)
def read_random_bits(n_bits: int) -> bytes:
    """Reads 'nbits' random bits.

    If nbits isn't a whole number of bytes, an extra byte will be appended with
    only the lower bits set.
    """

    n_bytes, r_bits = divmod(n_bits, 8)

    # Get the random bytes
    randomdata = os.urandom(n_bytes)

    # Add the remaining random bits
    if r_bits > 0:
        randomvalue = ord(os.urandom(1))
        randomvalue >>= 8 - r_bits
        randomdata = struct.pack("B", randomvalue) + randomdata

    return randomdata


@decorators.log_decorator(logger)
def read_random_int(n_bits: int) -> int:
    """Reads a random integer of approximately nbits bits."""

    randomdata = read_random_bits(n_bits)
    value = transform.bytes2int(randomdata)

    # Ensure that the number is large enough to just fill out the required
    # number of bits.
    value |= 1 << (n_bits - 1)

    return value


@decorators.log_decorator(logger)
def read_random_odd_int(n_bits: int) -> int:
    """Reads a random odd integer of approximately nbits bits.

    >>> read_random_odd_int(512) & 1
    1
    """

    value = read_random_int(n_bits)

    # Make sure it's odd
    return value | 1


@decorators.log_decorator(logger)
def randint(maxvalue: int) -> int:
    """Returns a random integer x with 1 <= x <= maxvalue

    May take a very long time in specific situations. If maxvalue needs N bits
    to store, the closer maxvalue is to (2 ** N) - 1, the faster this function
    is.
    """

    bit_size = common.bit_size(maxvalue)

    tries = 0
    while True:
        value = read_random_int(bit_size)
        if value <= maxvalue:
            break

        if tries % 10 == 0 and tries:
            # After a lot of tries to get the right number of bits but still
            # smaller than maxvalue, decrease the number of bits by 1. That'll
            # dramatically increase the chances to get a large enough number.
            bit_size -= 1
        tries += 1

    return value
