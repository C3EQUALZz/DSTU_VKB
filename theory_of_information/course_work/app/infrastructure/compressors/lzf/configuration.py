"""
Configuration values for the LZF algorithm.
"""

import enum


class Configuration:
    """
    The configuration values for executing the algorithm, as they are defined inside
    the original files.
    """

    HASH_TABLE_LOGARITHM = 16
    """
    The hash table logarithm base to use.

    With the default value of 16, the hash table will have 2^16 = 65536 entries.

    According to the original author the difference between 15 and 14 is very small for
    small blocks (and 14 is usually a bit faster). For a low memory/faster configuration
    he recommends using a value of 13. For best compression, 15 or 16 (or more, up to
    22) should be used.

    :type: :class:`int`
    """

    HASH_TABLE_SIZE = 1 << HASH_TABLE_LOGARITHM
    """
    The size of the search buffer (hash table/dictionary).

    :type: :class:`int`
    """

    LITERAL_MAX = 1 << 5
    """
    The maximum literal length we can encode.

    This corresponds to 2^5 = 32.

    :type: :class:`int`
    """

    MATCH_OFFSET_MAX = 1 << 13
    """
    The maximum match offset we can encode.

    This corresponds to 2^13 = 8192.

    :type: :class:`int`
    """

    MATCH_LENGTH_MAX = (1 << 8) + (1 << 3)
    """
    The maximum match length we can encode.

    This corresponds to 2^8 + 2^3 = 256 + 8 = 264.

    With (offset + length) = (13 + (8 + 3)) = 24 bits = 3 bytes, a match will always
    have 3 bytes.

    :type: :class:`int`
    """

    HEADER_SIZE_TYPE0 = 5
    """
    The header size in bytes for blocks of type 0 (= uncompressed blocks).

    :type: :class:`int`
    """

    HEADER_SIZE_TYPE1 = 7
    """
    The header size in bytes for blocks of type 1 (= compressed blocks).

    :type: :class:`int`
    """

    HEADER_SIZE_MAX = 7
    """
    The maximum header size in bytes.

    :type: :class:`int`
    """

    HEADER_SIZE_MIN = 5
    """
    The minimum header size in bytes.

    :type: :class:`int`
    """


class Constants:
    """
    Constants to use within the whole application.

    You should only change them if you know what you are doing.
    """

    BLOCK_SIZE_MAX = 1024 * 64 - 1
    """
    The maximum block size to use for file compression.

    This corresponds to 65535 = 2^16 - 1.

    :type: :class:`int`
    """


class LzfMode(enum.IntEnum):
    """
    The different LZF modes available which influence compression speed and ratio.
    """

    NORMAL = 0
    """
    The regular mode with the best compression quality, but worst speed.

    :type: :class:`int`
    """

    VERY_FAST = 1
    """
    Very fast mode. This is the recommended option.

    This sacrifices very little compression quality in favour of compression speed.
    It gives almost the same compression as the normal mode, and is - according to
    the original author - (very roughly) 15 % faster.

    :type: :class:`int`
    """

    ULTRA_FAST = 2
    """
    Ultra fast mode. This is recommended for binary data.

    This sacrifices some more compression quality in favour of compression speed.
    According to the original author this is roughly 1-2 % worse for large blocks and
    9-10 % for small, redundant blocks, but has >> 20 % better speed in both cases.

    The original author concludes that this should be enabled when in need for speed
    and using binary data, while possibly disabling it for text data.

    :type: :class:`int`
    """
