"""
Configuration values for the LZSS algorithm.
"""


class Configuration:
    """
    The configuration values for executing the algorithm, as they are defined inside
    the original file.
    """

    RING_BUFFER_SIZE = 4096
    """
    The size of the ring buffer to use.

    The default are 12 bits, which corresponds to 2^12 = 4096 entries.

    :type: :class:`int`
    """

    MATCH_LENGTH_MAX = 18
    """
    The maximum match length we can encode.

    With the default implementation, the match length cannot exceed 18 bytes.

    :type: :class:`int`
    """

    MATCH_LENGTH_MIN_THRESHOLD = 2
    """
    The threshold value to use for the minimum match length.

    With this value, a match needs to have at least 3 bytes.

    :type: :class:`int`
    """

    TREE_ROOT_INDEX = RING_BUFFER_SIZE
    """
    The index of the root of the binary search tree.
    """
