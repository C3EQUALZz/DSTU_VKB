"""
Interface to the LZSS implementations itself.

This should be the correct entry point for most applications.
"""

from app.infrastructure.compressors.lzss.compression import Compressor
from app.infrastructure.compressors.lzss.decompression import Decompressor


class LzssInterface:
    """
    LZSS interface.

    This should be the entrypoint for most applications.
    """

    @staticmethod
    def compress(decompressed):
        """
        Compress the given buffer using the LZSS algorithm.

        :param decompressed: The buffer to compress.
        :type decompressed: bytearray

        :return: The compressed buffer.
        :rtype: bytearray
        """
        return Compressor().compress(decompressed)

    @staticmethod
    def compress_file(
        input_file,
        output_file=None,
    ):
        """
        Compress the given file using the LZSS algorithm.

        :param input_file: The name of the file to compress.
        :type input_file: str

        :param output_file: The name of the file to write the compressed data to. Set
                            to :code:`None` to not write the output to a file.
        :type output_file: str or None

        :return: The compressed buffer.
        :rtype: bytearray
        """
        with open(input_file, mode="rb") as infile:
            decompressed = bytearray(infile.read())
        compressed = LzssInterface.compress(decompressed)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(compressed)

        return compressed

    @staticmethod
    def decompress(compressed):
        """
        Decompress the given buffer using the LZSS algorithm.

        :param compressed: The buffer to decompress.
        :type compressed: bytearray

        :return: The decompressed buffer.
        :rtype: bytearray
        """
        return Decompressor().decompress(compressed)

    @staticmethod
    def decompress_file(input_file, output_file=None):
        """
        Decompress the given file using the LZSS algorithm.

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
        decompressed = LzssInterface.decompress(compressed)

        if output_file:
            with open(output_file, mode="wb") as outfile:
                outfile.write(decompressed)

        return decompressed
