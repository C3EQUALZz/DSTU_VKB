"""
Interface to the LZJB implementations itself.

This should be the correct entry point for most applications.
"""

import enum

from app.infrastructure.compressors.lzjb.zfs_lzjb import (
    Compressor as ZfsLzjbCompressor,
    Decompressor as ZfsLzjbDecompressor,
)
from app.infrastructure.compressors.lzjb.os_compress import (
    Compressor as OsCompressCompressor,
    Decompressor as OsCompressDecompressor,
)


class LzjbVariant(enum.IntEnum):
    """
    The different LZJB variants available.
    """

    ZFS_LZJB = 0
    """
    The version from the `zfs/lzjb.c` file of OpenSolaris.

    :type: :class:`int`
    """

    OS_COMPRESS = 1
    """
    The version from the `os/compress.c` file of OpenSolaris.

    :type: :class:`int`
    """


class LzjbInterface:
    """
    LZJB interface.

    This should be the entrypoint for most applications.
    """

    @staticmethod
    def compress(decompressed, variant=LzjbVariant.ZFS_LZJB):
        """
        Compress the given buffer using the given LZJB variant.

        :param decompressed: The buffer to compress.
        :type decompressed: bytearray

        :param variant: The LZJB variant to use.
        :type variant: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        if variant == LzjbVariant.ZFS_LZJB:
            return ZfsLzjbCompressor().compress(decompressed)
        elif variant == LzjbVariant.OS_COMPRESS:
            return OsCompressCompressor().compress(decompressed)

    @staticmethod
    def compress_file(input_file, output_file=None, variant=LzjbVariant.ZFS_LZJB):
        """
        Compress the given file using the given LZJB variant.

        :param input_file: The name of the file to compress.
        :type input_file: str

        :param output_file: The name of the file to write the compressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :param variant: The LZJB variant to use.
        :type variant: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            decompressed = bytearray(infile.read())
        compressed = LzjbInterface.compress(decompressed, variant)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(compressed)

        return compressed

    @staticmethod
    def decompress(compressed, variant=LzjbVariant.ZFS_LZJB):
        """
        Decompress the given buffer using the given LZJB variant.

        :param compressed: The buffer to decompress.
        :type compressed: bytearray

        :param variant: The LZJB variant to use.
        :type variant: `int`

        :return: The decompressed buffer.
        :rtype: bytearray
        """
        if variant == LzjbVariant.ZFS_LZJB:
            return ZfsLzjbDecompressor().decompress(compressed)
        elif variant == LzjbVariant.OS_COMPRESS:
            return OsCompressDecompressor().decompress(compressed)

    @staticmethod
    def decompress_file(input_file, output_file=None, variant=LzjbVariant.ZFS_LZJB):
        """
        Decompress the given file using the given LZJB variant.

        :param input_file: The name of the file to decompress.
        :type input_file: str

        :param output_file: The name of the file to write the decompressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :param variant: The LZJB variant to use.
        :type variant: `int`

        :return: The decompressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            compressed = bytearray(infile.read())
        decompressed = LzjbInterface.decompress(compressed, variant)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(decompressed)

        return decompressed
