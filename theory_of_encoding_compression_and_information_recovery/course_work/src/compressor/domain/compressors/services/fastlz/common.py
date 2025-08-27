# mypy: ignore-errors
# ruff: noqa

"""
Common utility methods for the FastLZ algorithm.
"""

from compressor.domain.compressors.services.fastlz.configuration import FastLZConstants, FastLzLevel
from compressor.domain.compressors.services.fastlz.level1 import Decompressor as DecompressorLevel1
from compressor.domain.compressors.services.fastlz.level2 import Decompressor as DecompressorLevel2


def determine_level_from_buffer(buffer):
    """
    Determine the FastLZ level from the given buffer.

    :param buffer: The buffer to get the level from.
    :type buffer: bytearray

    :return: The level used in the buffer.
    :rtype: int

    :raises ValueError: The level is invalid.
    """
    # Read the magic identifier for the compression level.
    # This will read the first 3 bits and decide which level has been used.
    # We have to increase this by one as level 2 uses identifier 1 and level 1 uses
    # identifier 0.
    level = (buffer[0] >> 5) + 1

    # Map the level.
    # Fail if the level value is invalid.
    if level == 1:
        return FastLzLevel.LEVEL1
    if level == 2:
        return FastLzLevel.LEVEL2
    raise ValueError(f"Invalid level {level}.")


def call_decompressor_for_buffer_level(buffer):
    """
    Call the decompressor for the FastLZ level determined from the given buffer.

    :param buffer: The buffer to get the level from and to decompress.
    :type buffer: bytearray

    :return: The decompression result.
    :rtype: bytearray

    :raises ValueError: The level is invalid.
    """
    level = determine_level_from_buffer(buffer)

    if level == FastLzLevel.LEVEL1:
        # Use level 1.
        return DecompressorLevel1().decompress(buffer)
    if level == FastLzLevel.LEVEL2:
        # Use level 2.
        return DecompressorLevel2().decompress(buffer)

    raise ValueError(f"Invalid level {level} for decompression.")


def update_adler32(checksum, buffer):
    """
    Update the running Adler-32 checksum with the bytes of the buffer and return the
    updated checksum.

    The checksum should be initialized by 1 in the first run.

    For more information on the checksum calculation, see
    `RFC 1950 Section 8.2 <https://tools.ietf.org/html/rfc1950#section-8>`_ or the
    corresponding `Wikipedia article <https://en.wikipedia.org/wiki/Adler-32>`_.

    :param checksum: The old checksum value.
    :type checksum: int

    :param buffer: The buffer to update the checksum with. The complete buffer will be
                   consumed.
    :type buffer: bytearray

    :return: The updated checksum value.
    :rtype: int
    """
    # The current position inside the buffer.
    buffer_position = 0

    # Split the checksum into component sums.
    # `sum1` holds the last 4 bytes.
    # For `sum2` we remove the last 4 bytes, then get the last 4 bytes again (this
    # finally corresponds in `sum2` containing the first 4 bytes).
    sum1 = checksum & 0xFFFF
    sum2 = (checksum >> 16) & 0xFFFF

    # Retrieve the buffer length.
    length = len(buffer)

    # Iterate until the input is exhausted.
    while length > 0:
        # The modulo operation on unsigned long accumulators can be delayed for 5552
        # bytes, so the modulo operation time is negligible.
        # Check if we can delay it another time or not.
        # 5552 is the largest `n` such that
        # `255n(n+1)/2 + (n+1)(ADLER32_BASE-1) <= 2^32-1`.
        k = min(length, 5552)
        length -= k

        # Add the values up for the current "block".
        for _ in range(k):
            # `sum1` is the sum of the input data bytes.
            sum1 += buffer[buffer_position]
            buffer_position += 1

            # `sum2` is the sum of the values from each step.
            sum2 += sum1

        # Perform the modulo once per 5552 values.
        sum1 = sum1 % FastLZConstants.ADLER32_BASE
        sum2 = sum2 % FastLZConstants.ADLER32_BASE

    # Concatenate the values.
    return (sum2 << 16) + sum1


def read_unsigned_integer_16_bit(buffer, start_position):
    """
    Read an unsigned 16 bit integer value (= 2 bytes) from the buffer starting at the
    given index.

    :param buffer: The buffer to read from.
    :type buffer: bytearray

    :param start_position: The index to start at inside the buffer.
    :type start_position: int

    :return: The unsigned 16 bit integer value read from the buffer starting at the
             given index.
    """
    return buffer[start_position] + (buffer[start_position + 1] << 8)


def read_unsigned_integer_32_bit(buffer, start_position):
    """
    Read an unsigned 32 bit integer value (= 4 bytes) from the buffer starting at the
    given index.

    :param buffer: The buffer to read from.
    :type buffer: bytearray

    :param start_position: The index to start at inside the buffer.
    :type start_position: int

    :return: The unsigned 32 bit integer value read from the buffer starting at the
             given index.
    """
    return (
            buffer[start_position]
            + (buffer[start_position + 1] << 8)
            + (buffer[start_position + 2] << 16)
            + (buffer[start_position + 3] << 24)
    )


def memmove(buffer, start_position, byte_count):
    """
    Basic re-implementation of the classical `memmove` method. This method is able to
    handle buffer overlaps.

    The copy operation will start at the given index, new values will be appended at the
    end of the buffer.

    :param buffer: The buffer to work on.
    :type buffer: bytearray

    :param start_position: The start index inside the buffer.
    :type start_position: int

    :param byte_count: The number of bytes to copy over.
    :type byte_count: int
    """
    # Use `memcpy` if possible to avoid the manual loop.
    if start_position + byte_count < len(buffer):
        memcpy(buffer, buffer, start_position, byte_count)
        return

    # There is an overlap, so we have to copy the data byte-wise.
    for index in range(start_position, start_position + byte_count):
        buffer.append(buffer[index])


def memcpy(source, destination, source_start_position, byte_count):
    """
    Basic re-implementation of the classical `memcpy` method. This method is not able to
    handle buffer overlaps.

    The copy operation will start at the given index inside the source buffer, new
    values will be appended at the end of the destination buffer.

    :param source: The source buffer to read from.
    :type source: bytearray

    :param destination: The destination buffer to write to.
    :type destination: bytearray

    :param source_start_position: The start index inside the source buffer.
    :type source_start_position: int

    :param byte_count: The number of bytes to copy over.
    :type byte_count: int

    :raises ValueError: The copy operation would result in an overlap.
    """
    # Make sure that there is no overlap.
    if source_start_position + byte_count > len(source):
        raise ValueError("`memcpy` cannot handle overlaps. Please use `memmove`.")

    # Use slicing for the copy operation.
    destination += source[source_start_position: source_start_position + byte_count]


def calculate_hash_value(value, configuration):
    """
    Hash the given 32 bit unsigned integer value into a 16 bit unsigned integer value.

    :param value: The 32 bit unsigned integer value to hash.
    :type value: int

    :param configuration: The configuration to use.
    :type configuration: lz77_variants.fastlz.configuration.Configuration

    :return: The 16 bit unsigned integer value being the hash of the given value.
    :rtype: int
    """
    # The multiplication value seems to be
    #   (2 ** 32) * (math.sqrt(5) - 1) // 2
    # (calculation in Python), see `Doxygen source for OpenADFortTk, file
    # Open64.osprey1.0.common.util.id_map.h
    # <https://web.archive.org/web/20170624215708/https://www.mcs.anl.gov/OpenAD/OpenADFortTkExtendedDox/id__map_8h_source.html>`_
    # for example.
    hash_value = (value * 2654435769) >> (32 - configuration.HASH_TABLE_LOGARITHM)
    return hash_value & configuration.HASH_TABLE_MASK


def compare_buffer_content_until_mismatch(buffer, start1, start2, end2):
    """
    Compare the content of the buffer starting at the both positions. Stop if a mismatch
    occurs or the second position (which should be the greater one) has reached the
    given end position.

    This corresponds to the 32-bit variant of `flz_cmp` in the original implementation.

    :param buffer: The buffer to work on.
    :type buffer: bytearray

    :param start1: The first start index (the smaller one).
    :type start1: int

    :param start2: The second start index (the larger one).
    :type start2: int

    :param end2: The position for the second (greater) index value.
    :type end2: int

    :return: The length of the match. This will always be at least 1.
    :rtype: int
    """
    # Initialize the length value.
    length = 0

    # Compare byte-wise until the position limit has been reached.
    while start2 < end2:
        # Increase the length value before the comparison as the we are doing `*p++`
        # in the condition before the `break`.
        # We could move this length change after the comparison as well when
        # initializing the length value with `1` above.
        length += 1

        # Compare the current byte and stop if they do not match.
        if buffer[start1] != buffer[start2]:
            break

        # Move to the next bytes.
        start1 += 1
        start2 += 1

    # Return the length of the match.
    return length


def emit_literal_instructions(source, destination, source_start_position, length, configuration):
    """
    Emit the given number of literal bytes. Each group of `LITERAL_MAX` bytes is
    preceded by the literal command itself (`000` followed by the length value using 5
    bytes), so this function will emit multiple literal instructions if required.

    :param source: The source buffer to get the data from.
    :type source: bytearray

    :param destination: The destination buffer to write the data to.
    :type destination: bytearray

    :param source_start_position: The start index inside the source buffer.
    :type source_start_position: int

    :param length: The number of bytes to emit.
    :type length: int

    :param configuration: The configuration to use.
    :type configuration: lz77_variants.fastlz.configuration.Configuration

    :return: The number of bytes written to the destination buffer.
    :rtype: int
    """
    # We have written nothing until now.
    bytes_written = 0

    # Save the value for easier access.
    literal_max = configuration.LITERAL_MAX

    # Initialize the current source position.
    source_position = source_start_position

    # Handle full groups.
    while length >= literal_max:
        # Set the current value inside the output buffer to 31 (`- 1` as a literal
        # length of 0 does not make any sense).
        destination.append(literal_max - 1)
        bytes_written += 1

        # Copy the 32 characters of the current group.
        destination += source[source_position: source_position + literal_max]
        source_position += literal_max
        bytes_written += literal_max

        # We have written 32 characters.
        length -= literal_max

    # Handle the last 31 bytes.
    if length > 0:
        # Set the current value inside the output buffer to the remaining literal
        # length (`- 1` as a literal length of 0 does not make any sense).
        destination.append(length - 1)
        bytes_written += 1

        # Copy the required number of characters.
        destination += source[source_position: source_position + length]
        bytes_written += length

    # Return the number of bytes written.
    return bytes_written


def detect_magic_bytes(buffer):
    """
    Check if the buffer represents a 6pack archive.

    :param buffer: The buffer to check.
    :type buffer: bytearray

    :return: :code:`True` if the buffer represents a 6pack archive, :code:`False`
             otherwise.
    :rtype: bool
    """
    # Stop if the buffer is too short to hold the header.
    if len(buffer) < len(FastLZConstants.SIXPACK_MAGIC_IDENTIFIER):
        return False

    # Perform a byte-wise check.
    for index, value in enumerate(FastLZConstants.SIXPACK_MAGIC_IDENTIFIER):
        if buffer[index] != value:
            return False

    # No problems could be detected with the magic identifier.
    return True
