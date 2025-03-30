"""
Interface to the LZF implementations itself.

This should be the correct entry point for most applications.
"""

from app.infrastructure.compressors.lzf.compression import Compressor, FileCompressor
from app.infrastructure.compressors.lzf.configuration import Constants, LzfMode
from app.infrastructure.compressors.lzf.decompression import Decompressor, FileDecompressor


class LzfInterface:
    """
    LZF interface.

    This should be the entrypoint for most applications.
    """

    @staticmethod
    def compress(decompressed, mode=LzfMode.VERY_FAST):
        """
        Compress the given buffer using the given LZF mode.

        :param decompressed: The buffer to compress.
        :type decompressed: bytearray

        :param mode: The LZF mode to use.
        :type mode: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        return Compressor().compress(decompressed, mode)

    @staticmethod
    def compress_file(
            input_file,
            output_file=None,
            mode=LzfMode.VERY_FAST,
            block_size=Constants.BLOCK_SIZE_MAX,
    ):
        """
        Compress the given file using the given LZF mode and block size.

        :param input_file: The name of the file to compress.
        :type input_file: str

        :param output_file: The name of the file to write the compressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :param mode: The LZF mode to use.
        :type mode: `int`

        :param block_size: The block size to use.
        :type block_size: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            decompressed = bytearray(infile.read())
        compressed = FileCompressor().compress(decompressed, mode, block_size)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(compressed)

        return compressed

    @staticmethod
    def decompress(compressed):
        """
        Decompress the given buffer using the LZF algorithm.

        :param compressed: The buffer to decompress.
        :type compressed: bytearray

        :return: The decompressed buffer.
        :rtype: bytearray
        """
        return Decompressor().decompress(compressed)

    @staticmethod
    def decompress_file(input_file, output_file=None):
        """
        Decompress the given file using the LZF algorithm.

        :param input_file: The name of the file to decompress.
        :type input_file: str

        :param output_file: The name of the file to write the decompressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :return: The decompressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            compressed = bytearray(infile.read())
        decompressed = FileDecompressor().decompress(compressed)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(decompressed)

        return decompressed
