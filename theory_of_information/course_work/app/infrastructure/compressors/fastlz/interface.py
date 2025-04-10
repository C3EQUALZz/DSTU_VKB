"""
Interface to the FastLZ implementations itself.

This should be the correct entry point for most applications.
"""

from app.infrastructure.compressors.fastlz import common
from app.infrastructure.compressors.fastlz.configuration import FastLzLevel
from app.infrastructure.compressors.fastlz.files import (FileCompressor,
                                                         FileDecompressor)
from app.infrastructure.compressors.fastlz.level1 import \
    Compressor as CompressorLevel1
from app.infrastructure.compressors.fastlz.level2 import \
    Compressor as CompressorLevel2


class FastLzInterface:
    """
    FastLZ interface.

    This should be the entrypoint for most applications.
    """

    @staticmethod
    def compress(decompressed, level=FastLzLevel.AUTOMATIC):
        """
        Compress the given buffer using the given FastLZ level.

        :param decompressed: The buffer to compress.
        :type decompressed: bytearray

        :param level: The FastLZ level to use.
        :type level: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        # Use the selected level if possible.
        if level == FastLzLevel.LEVEL1:
            return CompressorLevel1().compress(decompressed)
        elif level == FastLzLevel.LEVEL2:
            return CompressorLevel2().compress(decompressed)

        # For short blocks, choose level 1.
        if len(decompressed) < 65536:
            # Use level 1.
            return CompressorLevel1().compress(decompressed)

        # Use level 2.
        return CompressorLevel2().compress(decompressed)

    @staticmethod
    def compress_file(input_file, output_file=None, level=FastLzLevel.AUTOMATIC):
        """
        Compress the given file using the given FastLZ level.

        :param input_file: The name of the file to compress.
        :type input_file: str

        :param output_file: The name of the file to write the compressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :param level: The FastLZ level to use.
        :type level: `int`

        :return: The compressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            decompressed = bytearray(infile.read())

        if level != FastLzLevel.AUTOMATIC:
            # Use the selected level.
            compressed = FileCompressor().compress(decompressed, input_file, level)
        elif len(decompressed) < 65536:
            # For short blocks, choose level 1.
            compressed = FileCompressor().compress(decompressed, input_file, FastLzLevel.LEVEL1)
        else:
            # Use level 2.
            compressed = FileCompressor().compress(decompressed, input_file, FastLzLevel.LEVEL2)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(compressed)

        return compressed

    @staticmethod
    def decompress(compressed):
        """
        Decompress the given buffer using the FastLZ algorithm.

        :param compressed: The buffer to decompress.
        :type compressed: bytearray

        :return: The decompressed buffer.
        :rtype: bytearray

        :raises ValueError: The level is invalid.
        """
        return common.call_decompressor_for_buffer_level(compressed)

    @staticmethod
    def decompress_file(input_file, output_file=None):
        """
        Decompress the given file using the FastLZ algorithm.

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
