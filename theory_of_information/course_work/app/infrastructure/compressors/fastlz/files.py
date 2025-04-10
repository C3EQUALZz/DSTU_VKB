"""
Implementation of the file-based FastLZ compression algorithm (6pack).
"""

import os

from app.exceptions.infrastructure import BadDataException
from app.infrastructure.compressors.fastlz import common
from app.infrastructure.compressors.fastlz.configuration import (Configuration,
                                                                 Constants,
                                                                 FastLzLevel)
from app.infrastructure.compressors.fastlz.level1 import \
    Compressor as CompressorLevel1
from app.infrastructure.compressors.fastlz.level2 import \
    Compressor as CompressorLevel2


class FileCompressor:
    """
    The implementation of the (file) compressor (6pack).
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration=Configuration):
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration = configuration

    def compress(self, source, filename, level=FastLzLevel.LEVEL1):
        """
        Compress the given source buffer using the FastLZ algorithm.

        :param source: The source buffer to compress.
        :type source: bytearray

        :param filename: The path to the input file.
        :type filename: str

        :param level: The FastLZ level to use. This cannot be `AUTOMATIC`.
        :type level: `int`

        :return: The compression result.
        :rtype: bytearray

        :raises ValueError: The automatic compression level is selected.
        :raises BadDataException: This file already is a 6pack archive.
        """
        # Forbid the automatic level.
        if level == FastLzLevel.AUTOMATIC:
            raise ValueError("Automatic level not supported for 6pack.")

        # Check if this already is a 6pack archive.
        if common.detect_magic_bytes(source):
            raise BadDataException("File already is a 6pack archive.")

        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # Write the magic identifier.
        destination += Constants.SIXPACK_MAGIC_IDENTIFIER
        destination_position += len(Constants.SIXPACK_MAGIC_IDENTIFIER)

        # Determine the actual filename.
        shown_name = bytearray(os.path.basename(filename), encoding="utf8")

        # Write the file size to the buffer and add the length of the filename using 2
        # bytes.
        buffer = self._get_file_size_buffer(source)
        buffer.append((len(shown_name) + 1) & 255)
        buffer.append((len(shown_name) + 1) >> 8)

        # Calculate the initial checksum.
        # Initialize with 1 as per Adler-32 specification.
        checksum = 1
        # Update the checksum for the buffer with the file size and filename length.
        checksum = common.update_adler32(checksum, buffer)
        # Update the checksum using the filename with a null-byte added at the end.
        # This is not directly obvious, but can be derived from passing
        #   strlen(shown_name) + 1
        # to the checksum calculation in the original implementation.
        checksum = common.update_adler32(checksum, shown_name + bytearray(1))

        # Write the header of the first chunk to the output, which takes 16 bytes.
        header = ChunkHeader()
        header.chunk_id = 1
        header.chunk_options = 0
        header.chunk_size = 10 + len(shown_name) + 1
        header.chunk_checksum = checksum
        header.chunk_extra = 0
        self._write_chunk_header(destination, header)
        destination_position += 16

        # Write the original file size and the length of the original filename to the
        # output, which takes 10 bytes (8 bytes for the file size, 2 bytes for the
        # filename length).
        destination += buffer
        destination_position += 10

        # Write the original filename to the output, including the trailing null-byte
        # (probably as string terminator). This is done to keep the application as
        # similar as possible to the original implementation.
        destination += shown_name + bytearray(1)
        destination_position += len(shown_name) + 1

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # The compression method to use. The default value is set by `pack_file`
            # in the original implementation and means "compress if possible and
            # useful".
            compression_method = 1

            # Retrieve the current block from the input.
            buffer = source[source_position : source_position + Constants.BLOCK_SIZE_COMPRESSION]
            bytes_read = len(buffer)
            source_position += bytes_read

            # If the input is too small, disable compression as it does not make any
            # sense.
            if bytes_read < 32:
                compression_method = 0

            # Write to the output.
            if compression_method == 1:
                # Compress using FastLZ.

                # Perform the compression itself using the desired level. We cannot
                # have the `AUTOMATIC` level here as we already sort this out at the
                # beginning of this function.
                if level == FastLzLevel.LEVEL1:
                    result = CompressorLevel1(self.configuration).compress(buffer)
                else:
                    result = CompressorLevel2(self.configuration).compress(buffer)
                chunk_size = len(result)

                # Update the checksum.
                checksum = common.update_adler32(1, result)

                # Write the header for the current chunk, which takes 16 bytes.
                header = ChunkHeader()
                header.chunk_id = 17
                header.chunk_options = 1
                header.chunk_size = chunk_size
                header.chunk_checksum = checksum
                header.chunk_extra = bytes_read
                self._write_chunk_header(destination, header)
                destination_position += 16

                # Add the compression result itself to the output.
                destination += result
                destination_position += chunk_size
            else:
                # Uncompressed data (and fallback method).

                # Determine the checksum for the current buffer content.
                checksum = common.update_adler32(1, buffer)

                # Write the header for the current chunk, which takes 16 bytes.
                header = ChunkHeader()
                header.chunk_id = 17
                header.chunk_options = 0
                header.chunk_size = bytes_read
                header.chunk_checksum = checksum
                header.chunk_extra = bytes_read
                self._write_chunk_header(destination, header)
                destination_position += 16

                # Add the plain bytes itself to the output.
                destination += buffer
                destination_position += bytes_read

        # Return the destination buffer.
        return destination

    @staticmethod
    def _get_file_size_buffer(source):
        """
        Write the file size to a buffer of size 8, while only the first 4 bytes are
        actually used for the file size.

        :param source: The source buffer to determine the write the size.
        :type source: bytearray

        :return: A new buffer of size 8 with the first 4 bytes holding the input size
                 and the last 4 bytes being 0.
        :rtype: bytearray
        """
        # Create the buffer.
        buffer = bytearray(8)

        # Determine the input buffer size.
        size = len(source)

        # Write the input size to the buffer.
        buffer[0] = size & 255
        buffer[1] = (size >> 8) & 255
        buffer[2] = (size >> 16) & 255
        buffer[3] = (size >> 24) & 255

        # Return the newly created buffer.
        return buffer

    @staticmethod
    def _write_chunk_header(buffer, header):
        """
        Write the header for the current chunk.

        :param buffer: The buffer to write to.
        :type buffer: bytearray

        :param header: The header to write.
        :type header: ChunkHeader
        """
        # Write the chunk ID, taking the first 2 bytes.
        buffer.append(header.chunk_id & 255)
        buffer.append(header.chunk_id >> 8)

        # Write the chunk options, taking the next 2 bytes.
        buffer.append(header.chunk_options & 255)
        buffer.append(header.chunk_options >> 8)

        # Write the size, taking the next 4 bytes.
        buffer.append(header.chunk_size & 255)
        buffer.append((header.chunk_size >> 8) & 255)
        buffer.append((header.chunk_size >> 16) & 255)
        buffer.append((header.chunk_size >> 24) & 255)

        # Write the checksum, taking the next 4 bytes.
        buffer.append(header.chunk_checksum & 255)
        buffer.append((header.chunk_checksum >> 8) & 255)
        buffer.append((header.chunk_checksum >> 16) & 255)
        buffer.append((header.chunk_checksum >> 24) & 255)

        # Write the extra data, taking the next 4 bytes.
        buffer.append(header.chunk_extra & 255)
        buffer.append((header.chunk_extra >> 8) & 255)
        buffer.append((header.chunk_extra >> 16) & 255)
        buffer.append((header.chunk_extra >> 24) & 255)


class FileDecompressor:
    """
    The implementation of the (file) decompressor (6unpack).
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration=Configuration):
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration = configuration

    def decompress(self, source):
        """
        Decompress the given source buffer using the FastLZ algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :return: The decompression result.
        :rtype: bytearray

        :raises ValueError: The level of one of the blocks is invalid.
        :raises BadDataException: Something is wrong with the archive.
        """
        # Check if this is a 6pack archive.
        if not common.detect_magic_bytes(source):
            raise BadDataException("File is not a 6pack archive.")

        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        # We already skip the magic identifier bytes with the position.
        source_position = len(Constants.SIXPACK_MAGIC_IDENTIFIER)
        source_length = len(source)

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # The original (uncompressed) file size.
        decompressed_size = 0

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Retrieve the chunk header, which occupies 16 bytes.
            header = self._read_chunk_header(source, source_position)
            source_position += 16

            # Handle the different chunk types.

            if header.chunk_id == 1 and 10 < header.chunk_size < Constants.BLOCK_SIZE_DECOMPRESSION:
                # This is the first chunk in the file.
                # It cannot be smaller than 11 bytes, as it contains the original file
                # size (using 8 bytes), the number of bytes for the original filename
                # (using 2 bytes) and at least 1 byte for the original filename itself.

                # Clear the output buffer.
                destination = bytearray()
                destination_position = 0

                # Retrieve the current chunk from the source buffer.
                buffer = source[source_position : source_position + header.chunk_size]
                source_position += len(buffer)

                # Calculate the initial checksum value.
                # The `1` is coming from the Adler-32 initialization.
                checksum = common.update_adler32(1, buffer)

                # Make sure that the checksums match.
                if checksum != header.chunk_checksum:
                    raise BadDataException(
                        "Checksum mismatch: Expected {}, got {}".format(hex(header.chunk_checksum), hex(checksum))
                    )

                # Get the uncompressed size (the original file size) by reading 4 bytes
                # from the buffer.
                # This value will be followed by 4 empty (null) bytes inside the buffer.
                decompressed_size = common.read_unsigned_integer_32_bit(buffer, 0)

                # Get the name of the input file.
                # In the first step we read the number of bytes for this name, which is
                # encoded using 2 bytes (the offset of 8 bytes is due to the original
                # file size, see above).
                # Afterwards we make sure that we will not exceed the buffer limits and
                # retrieve the file name itself.
                # Please note that we do not use this value in our implementation, but
                # let the user enter the output filename on their own. This is done to
                # keep the general interface as similar as possible.
                # Another note: The output file name still has the trailing null-byte.
                name_length = common.read_unsigned_integer_16_bit(buffer, 8)
                name_length = min(name_length, header.chunk_size - 10)
                output_file_name = buffer[10 : 10 + name_length]
                assert len(output_file_name) == name_length

            if header.chunk_id == 17 and decompressed_size:
                # This is not the first chunk.

                # Handle the different compression variants.
                if header.chunk_options == 0:
                    # This is uncompressed data, so we can just copy it to the output.

                    # Initialize the remaining size and the checksum (see Adler-32
                    # initialization notes).
                    remaining = header.chunk_size
                    checksum = 1

                    # Read one block at a time, write it and update the checksum.
                    while remaining > 0:
                        # Make sure to not read across the source buffer bounds.
                        if source_position >= source_length:
                            raise BadDataException("Reached end while copying data.")

                        # Determine the size of the current block.
                        bytes_in_block = min(remaining, Constants.BLOCK_SIZE_DECOMPRESSION)

                        # Read the current block from the source buffer and make sure
                        # that it actually has the desired length.
                        buffer = source[source_position : source_position + bytes_in_block]
                        assert len(buffer) == bytes_in_block
                        source_position += bytes_in_block

                        # Add the current block to the output.
                        destination += buffer
                        destination_position += bytes_in_block

                        # Update the checksum.
                        checksum = common.update_adler32(checksum, buffer)

                        # We have read some bytes.
                        remaining -= bytes_in_block

                    # Make sure that everything has been read/written correctly by
                    # comparing the checksum.
                    if checksum != header.chunk_checksum:
                        raise BadDataException(
                            "Checksum mismatch: Expected {}, got {}".format(hex(header.chunk_checksum), hex(checksum))
                        )

                elif header.chunk_options == 1:
                    # This has been compressed using FastLZ.

                    # Read the current chunk from the input.
                    compressed_buffer = source[source_position : source_position + header.chunk_size]
                    source_position += header.chunk_size

                    # Update the checksum.
                    checksum = common.update_adler32(1, compressed_buffer)

                    # Make sure that everything has been read correctly.
                    if checksum != header.chunk_checksum:
                        raise BadDataException(
                            "Checksum mismatch: Expected {}, got {}".format(hex(header.chunk_checksum), hex(checksum))
                        )

                    # Decompress the given data.
                    decompressed_buffer = common.call_decompressor_for_buffer_level(compressed_buffer)
                    decompressed_size = len(decompressed_buffer)

                    # Make sure that we did not lose/added some data.
                    if decompressed_size != header.chunk_extra:
                        raise BadDataException(
                            "Expected {} bytes after decompression, got {} "
                            + "bytes.".format(header.chunk_extra, decompressed_size)
                        )

                    # Add the decompressed buffer to the output.
                    destination += decompressed_buffer
                    destination_position += decompressed_size

                else:
                    # This is using a compression method not (yet) known.
                    raise BadDataException("Unknown compression method {}.".format(header.chunk_options))

        # Return the destination buffer.
        return destination

    @staticmethod
    def _read_chunk_header(buffer, start_position):
        """
        Read the header for the current chunk.

        :param buffer: The buffer to read from.
        :type buffer: bytearray

        :param start_position: The start index to use inside the buffer.
        :type start_position: int

        :return: The chunk header read from the buffer.
        :rtype: ChunkHeader
        """
        header = ChunkHeader()

        # Get the chunk ID, taking the first 2 bytes.
        header.chunk_id = common.read_unsigned_integer_16_bit(buffer, start_position)

        # Get the chunk options, taking the next 2 bytes.
        header.chunk_options = common.read_unsigned_integer_16_bit(buffer, start_position + 2)

        # Get the size, taking the next 4 bytes.
        header.chunk_size = common.read_unsigned_integer_32_bit(buffer, start_position + 4)

        # Get the checksum, taking the next 4 bytes.
        header.chunk_checksum = common.read_unsigned_integer_32_bit(buffer, start_position + 8)

        # Get the extra data, taking the next 4 bytes.
        header.chunk_extra = common.read_unsigned_integer_32_bit(buffer, start_position + 12)

        # Return the header data.
        return header


class ChunkHeader:
    """
    Container for the chunk header data.
    """

    chunk_id = 0
    """
    The ID of the chunk, using 2 bytes.

    This is either 1 (= first chunk) or 17 (= not the first chunk).

    :type: :class:`int`
    """

    chunk_options = 0
    """
    The options of the chunk, using 2 bytes.

    This is either 0 (= uncompressed data, simply copy the data to the output) or 1
    (= compressed using FastLZ).

    :type: :class:`int`
    """

    chunk_size = 0
    """
    The size of the current chunk, using 4 bytes.

    This is either `10 + len(filename) + 1` if this is the first chunk, the compressed
    size for compressed data or the original size of the block for uncompressed data.

    :type: :class:`int`
    """

    chunk_checksum = 0
    """
    The checksum of the current chunk, using 4 bytes.

    This is the current Adler-32 checksum based upon the content.

    :type: :class:`int`
    """

    chunk_extra = 0
    """
    The extra data of the current chunk, using 4 bytes.

    This is 0 for the first chunk and the number of bytes read from the input file
    during compression. This will never exceed the block size.

    :type: :class:`int`
    """

    def __init__(self):
        self.chunk_id = 0
        self.chunk_options = 0
        self.chunk_size = 0
        self.chunk_checksum = 0
        self.chunk_extra = 0
