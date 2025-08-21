"""
Configuration values for the FastLZ algorithm.
"""

import enum


class FastLZConfiguration:
    """
    The configuration values for executing the algorithm, as they are defined inside
    the original files.
    """

    LITERAL_MAX = 32
    """
    The maximum literal length we can encode.

    This corresponds to 2^5 = 32.

    :type: :class:`int`
    """

    MATCH_LENGTH_MAX = 264
    """
    The maximum match length we can encode.

    This corresponds to 2^8 + 8 = 256 + 8. At least 9 bytes are needed for a long match
    (below there are short matches).

    :type: :class:`int`
    """

    MATCH_OFFSET_MAX_LEVEL1 = 8192
    """
    The maximum match offset we can encode with level 1.

    This corresponds to 2^13 = 8192.

    :type: :class:`int`
    """

    MATCH_OFFSET_MAX_LEVEL2 = 8191
    """
    The maximum match offset we can encode with level 2 in the regular case.

    This corresponds to 2^13 - 1 = 8192 - 1.

    :type: :class:`int`
    """

    MATCH_OFFSET_MAX_LEVEL2_FAR = 65535 + MATCH_OFFSET_MAX_LEVEL2 - 1
    """
    The maximum match offset we can encode with level 2 in the extended case.

    This corresponds to (2^16 - 1) + (2^13 - 1). Besides the known minimum value of
    `MATCH_OFFSET_MAX_LEVEL2` in this case, we have 2 additional offset bytes, which
    corresponds to 16 bits (therefore the 2^16 part).

    :type: :class:`int`
    """

    HASH_TABLE_LOGARITHM = 14
    """
    The hash table logarithm base to use.

    With the default value of 14, the hash table will have 2^14 = 16384 entries.

    :type: :class:`int`
    """

    HASH_TABLE_SIZE = 1 << HASH_TABLE_LOGARITHM
    """
    The size of the search buffer (hash table/dictionary).

    :type: :class:`int`
    """

    HASH_TABLE_MASK = HASH_TABLE_SIZE - 1
    """
    The hash table mask to limit the maximum value of the hash table index (using the
    modulo operator).

    :type: :class:`int`
    """


class FastLzLevel(enum.IntEnum):
    """
    The different FastLZ levels available.
    """

    AUTOMATIC = 0
    """
    Let the application decide which level to use depending on the input size.

    This working mode is not recommended.

    :type: :class:`int`
    """

    LEVEL1 = 1
    """
    Level 1, which is recommended for shorter blocks.

    :type: :class:`int`
    """

    LEVEL2 = 2
    """
    Level 2, which is recommended for larger blocks.

    :type: :class:`int`
    """


class FastLZConstants:
    """
    Constants to use within the whole application.
    """

    SIXPACK_MAGIC_IDENTIFIER = bytearray.fromhex("89 36 50 4B 0D 0A 1A 0A")
    """
    The magic identifier for 6pack files.

    This corresponds to the original magic numbers, while translating the decimal values
    to hexadecimal ones for constructing the byte array. These values have been
    converted using the following code:

    .. code-block:: python

       magic = [137, ord("6"), ord("P"), ord("K"), 13, 10, 26, 10]
       magic_hex = [hex(x) for x in magic]

    :type: :class:`bytearray`
    """

    BLOCK_SIZE_DECOMPRESSION = 65536
    """
    The block size to use during decompression.

    This corresponds to 2^16, which means that each block can be indexed using a 16 bit
    unsigned integer variable. It is actually half as large as the block size during the
    compression.

    :type: :class:`int`
    """

    BLOCK_SIZE_COMPRESSION = 2 * 64 * 1024
    """
    The block size to use during compression.

    This corresponds to 2 * 64 * 1024 = 2^1 * 2^6 * 2^10 = 2^17 = 131072, which means
    that each block can be indexed using a 17 bit unsigned integer variable. It is
    actually twice as large as the block size during the decompression.

    :type: :class:`int`
    """

    ADLER32_BASE = 65521
    """
    The Adler-32 base to use.

    This is the largest prime number smaller than 2^16 = 65536.

    :type: :class:`int`
    """