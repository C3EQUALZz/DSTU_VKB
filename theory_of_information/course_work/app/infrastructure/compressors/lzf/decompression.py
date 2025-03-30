"""
Implementation of the LZF decompression algorithm.
"""


from app.infrastructure.compressors.lzf.configuration import Configuration

from app.exceptions.infrastructure import BadDataException


class Decompressor:
    """
    The implementation of the (string) decompressor.
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

    def decompress(self, source, start_position=0, source_length=-1):
        """
        Decompress the given source buffer using the LZF algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :param start_position: The position (offset) to start at in the source buffer.
        :type start_position: int

        :param source_length: The source length to assume. All buffer content after
                              :code:`start_position + source_length` will be ignored.
                              Set to :code:`-1` to not limit the source length.
        :type source_length: int

        :return: The uncompressed data.
        :rtype: bytearray

        :raises BadData: The source buffer content is malformed.
        """
        # The source parameters: the current position inside the source buffer and the
        # final position inside the source buffer to use.
        source_position = start_position
        source_end_position = (
            source_position + source_length if source_length != -1 else len(source)
        )

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # Iterate until the (requested) end of the input has been reached.
        while source_position < source_end_position:
            # The first byte allows us to decide which instruction type we have in the
            # current step.
            # After reading this byte, move one position forward.
            instruction_type_byte = source[source_position]
            source_position += 1

            # Handle the instruction.
            if instruction_type_byte < (1 << 5):
                # If the first byte is less than 2^5 = 32, we have a literal
                # instruction.
                # The format of a literal instruction is `000LLLLL`, so the largest
                # value for the first byte is 00011111_2 = 31_10 < 32.

                # As we can ignore the leading zeros, the first byte corresponds to the
                # literal length. We have to add 1, as literals of length 0 do not make
                # much sense.
                literal_length = instruction_type_byte + 1

                # No need to check the output overflow here.

                # Abort if there are less bytes left than requested by the literal
                # instruction.
                if source_position + literal_length > source_end_position:
                    raise BadDataException(
                        "Should copy {} bytes, but only {} left inside the source "
                        + "buffer.".format(
                            literal_length, source_end_position - source_position
                        )
                    )

                # We cannot have overlaps, so just copy the bytes from the source
                # buffer to the destination buffer.
                destination += source[
                    source_position : source_position + literal_length
                ]

                # Represent the literal instruction within the positions.
                source_position += literal_length
                destination_position += literal_length
            else:
                # If the first byte is at least 2^5 = 32, we have a match instruction.

                # Retrieve the first three bits. This can either be the length for short
                # matches or the indicator for long matches (if the value is 7).
                match_length = instruction_type_byte >> 5

                # Retrieve the first value part of the offset.
                # The AND-ing retrieves the last 5 bits of the first byte. This are the
                # 5 most significant bits of the offset.
                # The shift by 1 byte makes space for the second byte.
                match_offset_part1 = (instruction_type_byte & 0x1F) << 8

                # We can already calculate the position of the copy operation here.
                # This is possible as we are already working with the shifted offset
                # value here.
                # The `-1` basically means `offset + 1`, as an offset of 0 does not
                # make much sense. We could write
                #     destination_position - (match_offset_part1 + 1)
                # as well to make it more obvious, but without the brackets it may
                # actually be faster.
                copy_start_position = destination_position - match_offset_part1 - 1

                # Abort if there are no bytes left for retrieving the next bytes of the
                # instruction.
                if source_position >= source_end_position:
                    raise BadDataException(
                        "Input exhausted before match instruction handling is complete."
                    )

                # Handle long matches if needed.
                if match_length == 7:
                    # This is a long match, indicated by the first 3 bits being
                    # 111_2 = 1 + 2 + 4 = 7_10.

                    # The second byte of the current input holds the actual length
                    # value for long matches.
                    # We are adding this length value to 7 as we know that this length
                    # cannot be smaller - otherwise we would have chosen a short match
                    # instruction instead of the long match instruction.
                    match_length += source[source_position]

                    # Move to the next input position.
                    source_position += 1

                    # Abort if there are no bytes left for retrieving the next bytes of
                    # the instruction.
                    if source_position >= source_end_position:
                        raise BadDataException(
                            "Input exhausted before match instruction handling is "
                            + "complete."
                        )

                # The second (short match) or third (long match) byte holds the 8 least
                # significant bits of the offset, so retrieve it, correct the match
                # position and move the input forward.
                copy_start_position -= source[source_position]
                source_position += 1

                # No need to check the output overflow here.

                # Abort if the referenced position is before the start of the
                # destination buffer.
                # Please note that this could cause errors if used with a dictionary
                # shared across the different blocks, but as we are starting with an
                # empty dictionary on every block compression run, this is no problem
                # for us.
                if copy_start_position < 0:
                    raise BadDataException(
                        "Copy position {} outside of range.".format(copy_start_position)
                    )

                # The match length is still off-by-two, so correct this.
                # This corresponds to "minimum match length - unused length zero =
                # 3 - 1 = 2".
                match_length += 2

                # This copy operation is actually much shorter than in the original
                # implementation as we are using direct copying whenever possible
                # instead of deciding this based on the length (and only using `memcpy`
                # when there are no overlaps and the match length is at least 10).
                if destination_position >= copy_start_position + match_length:
                    # There is no overlap, so we are save to copy the data over
                    # directly.
                    destination += destination[
                        copy_start_position : copy_start_position + match_length
                    ]
                else:
                    # We have an overlap, so we copy the data byte-wise.
                    for i in range(match_length):
                        destination.append(destination[copy_start_position + i])

                # Represent the match instruction within the destination position.
                destination_position += match_length

        # Return the destination buffer.
        return destination


class FileDecompressor:
    """
    The implementation of the (file) decompressor.
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
        Decompress the given source buffer using the LZF algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :return: The uncompressed data.
        :rtype: bytearray

        :raises BadDataException: The source buffer content is malformed.
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer.
        destination = bytearray()

        # TODO: Test this overflow handling.
        # The current overflow size.
        overflow_size = 0

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Determine the start position while taking the overflow into account.
            start_position = source_position - overflow_size

            # Retrieve the header.
            header = source[
                start_position : start_position + self.configuration.HEADER_SIZE_MAX
            ]
            header_length = len(header)

            # Reset the overflow size.
            overflow_size = 0

            # The input is empty. `header[0] == 0` checks for the null byte (= EOF).
            if header_length == 0 or header[0] == 0:
                return bytearray()

            # Detect malformed input.
            if header_length < self.configuration.HEADER_SIZE_MIN:
                # The header is not long enough.
                raise BadDataException("Invalid data stream - short header.")
            if header[0] != ord("Z") or header[1] != ord("V"):
                # The magic values could not be found.
                raise BadDataException("Invalid data stream - magic not found.")

            # Retrieve the compression type and the different values from the header.
            compression_type = header[2]
            if compression_type == 0:
                # This is uncompressed data.
                is_compressed = False

                # We do not have any compressed size as this data is uncompressed.
                compressed_size = -1

                # Retrieve the uncompressed size from the header.
                uncompressed_size = (header[3] << 8) | header[4]

                # The data starts after the entries for header type 0.
                data_start_offset = self.configuration.HEADER_SIZE_TYPE0
            elif compression_type == 1:
                # This is compressed data.
                is_compressed = True

                # Avoid index errors.
                if header_length < self.configuration.HEADER_SIZE_TYPE1:
                    # The header is too short for type 1.
                    raise BadDataException("Too short header.")

                # Retrieve the compressed size from the header.
                compressed_size = (header[3] << 8) | header[4]

                # Retrieve the uncompressed size from the header.
                uncompressed_size = (header[5] << 8) | header[6]

                # The data starts after the entries for header type 1.
                data_start_offset = self.configuration.HEADER_SIZE_TYPE1
            else:
                # This is no known block type.
                raise BadDataException("Unknown block type {}.".format(compression_type))

            # Determine the number of bytes we have to read.
            number_of_bytes = (
                uncompressed_size if not is_compressed else compressed_size
            )
            # Determine the number of not used header bytes.
            not_used_header_bytes = header_length - data_start_offset
            # Determine the position at which the data starts.
            data_start_position = start_position + data_start_offset

            # Copy over not used header bytes.
            # This is only true for block type 0 (uncompressed data), as the header is
            # just 5 bytes, but we always read 7 bytes.
            if not_used_header_bytes > 0:
                destination += source[
                    data_start_position : data_start_position + not_used_header_bytes
                ]
                if not is_compressed:
                    uncompressed_size -= not_used_header_bytes

            # TODO: Is there a case where this holds true?
            if not_used_header_bytes > number_of_bytes:
                # overflow_size = not_used_header_bytes - number_of_bytes
                # TODO: Implement this.
                raise NotImplementedError()

            # We have already copied the not used header bytes to the output, so we can
            # move our position forward.
            data_start_position += not_used_header_bytes

            # Determine the number of unused bytes of the current chunk.
            unused_chunk_bytes = number_of_bytes - not_used_header_bytes
            if unused_chunk_bytes > 0:
                # We have unused chunk bytes.
                # This should nearly always be the case.

                # Retrieve the current part from the source buffer and make sure there
                # actually are enough bytes available.
                temp = source[
                    data_start_position : data_start_position + unused_chunk_bytes
                ]
                if len(temp) != unused_chunk_bytes:
                    raise BadDataException("Too short data.")

            # Perform the decompression itself.
            if not is_compressed:
                # This is an uncompressed block, so just write the data to the output.
                destination += source[
                    data_start_position : data_start_position + uncompressed_size
                ]
            else:
                # This is a compressed block.

                # Decompress the data.
                decompressed = Decompressor(self.configuration).decompress(
                    source, data_start_position, compressed_size
                )

                # Make sure that the uncompressed size encoded inside the header and
                # the actual uncompressed size match.
                if len(decompressed) != uncompressed_size:
                    raise BadDataException("Invalid stream - data corrupted.")

                # Write the decompressed data to the output.
                destination += decompressed

            # Determine the actual block size and move the input position forward by
            # this value.
            block_size = header_length - not_used_header_bytes + number_of_bytes
            source_position += block_size

        # Return the destination buffer.
        return destination
