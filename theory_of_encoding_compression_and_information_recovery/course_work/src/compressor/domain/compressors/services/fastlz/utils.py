"""
Collection of common utility methods.
"""


def shift_left_and_cut(value: int, shift: int = 1, bits: int = 8) -> int:
    """
    Shift the given value to the left and cut it to the desired size.

    :param value: The value to shift.
    :type value: int

    :param shift: The number of bits to shift too the left.
    :type shift: int

    :param bits: The number of bits of the output. Only the last `bits` bits will be
                 kept.
    :type bits: int

    :return: The value being shifted with a maximum of `bits` bits.
    :rtype: int
    """
    result: int = get_last_bits(value << shift, bits)
    return result


def get_last_bits(value: int, bits: int = 8) -> int:
    """
    Get the last `bits` bits from the given value.

    :param value: The value to get the bits from.
    :type value: int

    :param bits: The number of bits of the output. Only the last `bits` bits will be
                 kept.
    :type bits: int

    :return: The value with a maximum of `bits` bits.
    :rtype: int
    """
    mask = (1 << bits) - 1
    return value & mask


def get_last_bytes(value: int, byte_count: int = 1) -> int:
    """
    Get the last `byte_count` bytes from the given value.

    :param value: The value to get the bits from.
    :type value: int

    :param byte_count: The number of bytes of the output. Only the last `byte_count`
                       bytes will be kept.
    :type byte_count: int

    :return: The value with a maximum of `byte_count` bytes.
    :rtype: int
    """
    # Multiply by 2^3 = 8 to get the number of bits.
    bits = byte_count << 3
    return get_last_bits(value, bits)


def compare_first_bytes(data_buffer: bytearray, start_position1: int, start_position2: int, byte_count: int) -> bool:
    """
    Compare the first `byte_count` bytes of the buffer using the given start positions.

    :param data_buffer: The buffer to work on.
    :type data_buffer: bytearray

    :param start_position1: The first start position for the comparison.
    :type start_position1: int

    :param start_position2: The second start position for the comparison.
    :type start_position2: int

    :param byte_count: The number of bytes to compare.
    :type byte_count: int

    :return: Whether the first `byte_count` bytes of the buffer - when starting at both
             positions - match. This will be :code:`False` if there are not enough bytes
             available starting at one of the positions.
    :rtype: bool
    """
    # Retrieve the first `byte_count` bytes from the buffer starting at each position.
    buffer1 = data_buffer[start_position1 : start_position1 + byte_count]
    buffer2 = data_buffer[start_position2 : start_position2 + byte_count]

    # As slicing does not fail if the number of bytes is less than the requested one,
    # check it manually and fail if needed.
    if len(buffer1) != byte_count:
        return False
    if len(buffer2) != byte_count:
        return False

    # Perform the comparison itself.
    return buffer1 == buffer2
