"""
Implementation of the LZF compression algorithm.
"""

import math

from app.infrastructure.compressors import utils
from app.infrastructure.compressors.lzf.configuration import Configuration, Constants, LzfMode


class Compressor:
    """
    The implementation of the (string) compressor.
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

    def compress(
            self, source, start_position=0, maximum_output_length=-1, mode=LzfMode.VERY_FAST
    ):
        """
        Compress the given source buffer using the LZF algorithm.

        .. note::
           This uses a slightly different approach for writing the literal instructions
           which should generally be more readable.

        :param source: The source buffer to compress.
        :type source: bytearray

        :param start_position: The position (offset) to start at in the source buffer.
        :type start_position: int

        :param maximum_output_length: The maximum output length to use. If the output
                                      (compressed data) would be longer, :code:`None`
                                      will be returned. Use :code:`-1` to not limit the
                                      output length. The original implementation of the
                                      terminal interface uses :code:`len(source) - 4`.
        :type maximum_output_length: int

        :param mode: The LZF mode to use.
        :type mode: `int`

        :return: The compression result. Will be :code:`None` if the maximum output
                 length would be exceeded.
        :rtype: bytearray or None
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = start_position
        source_length = len(source)

        # The destination buffer, the current position inside it (which corresponds to
        # the output length) and the final position inside the destination buffer to
        # use.
        destination = bytearray()
        destination_position = 0
        destination_end = (
            math.inf if maximum_output_length == -1 else maximum_output_length
        )

        # If the source is empty, return the empty destination buffer.
        if source_length == 0:
            return destination
        # We know that the source has at least one byte. So if the output should be
        # empty, we would exceed the output length and can return `None` for this
        # reason.
        if maximum_output_length == 0:
            return None

        # The hash table itself.
        # This gets initialized by zero for all entries. Unlike the C implementation,
        # we will always initialize this.
        hash_table = [0] * self.configuration.HASH_TABLE_SIZE

        # Retrieve the hash value for the first two bytes.
        hash_value = self._get_first_two_bytes_as_integer(source, source_position)

        # We start with a zero-length literal.
        literal_length = 0

        # Iterate until the end of the input has been reached.
        # The "- 2" is due to the match length requiring at least 3 bytes.
        while source_position < source_length - 2:
            # Retrieve the current entry from the hash table. Then save the current
            # position inside the hash table.
            hash_value = self._concatenate_value_with_third_byte(
                hash_value, source, source_position
            )
            hash_slot = self._hash(hash_value, mode)
            referenced_position = hash_table[hash_slot]
            hash_table[hash_slot] = source_position

            # Determine the offset. This might still reference invalid entries.
            # We can subtract 1 as we do not have offsets of 0 (this would be the source
            # position itself).
            # This assignment has been moved from the if condition to before the check
            # to increase readability.
            offset = source_position - referenced_position - 1

            # Determine the instruction type.
            # Conditions explained:
            #   1. The reference cannot appear after the current input position. In
            #      fact the next test already takes care of this and we do not have any
            #      speed improvement due to assigning the offset variable beforehand,
            #      but to keep it as similar as possible in regards to the original C
            #      implementation I decided to leave this here.
            #   2. Make sure the offset does not exceed the limit which can encode.
            #   3. The reference cannot be before the start of the input.
            #   4. Make sure that at least the first 3 bytes match.
            if (
                    source_position > referenced_position >= 0
                    and offset < self.configuration.MATCH_OFFSET_MAX
                    and utils.compare_first_bytes(
                source, referenced_position, source_position, 3
            )
            ):
                # This is a match.

                # The minimum match length is 3, but as the match length checking loop
                # starts by incrementing this before doing the check (do ... while
                # loop), we have to use 2 here.
                match_length = 2

                # The maximum match length we can have.
                # This avoids exceeding the overall match length limit as well as the
                # source length.
                match_length_max = source_length - source_position - match_length
                match_length_max = min(
                    match_length_max, self.configuration.MATCH_LENGTH_MAX
                )

                # Stop if we have reached the requested output size.
                # Our implementation slightly differs, as unlike in the C version we do
                # not write to literal bytes directly when increasing the literal
                # length counter. For this reason, we have to add the value of
                # `literal_length` to the condition.
                # Parts of the sums explained:
                #   * The literal length is required as we might have to emit a literal
                #     instruction before the actual match instruction.
                #   * The `3` probably represents the bytes required for a long match
                #     instruction, which corresponds to the "worst case" for a match
                #     instruction.
                #   * The `1` probably represents the literal byte we have to write with
                #     a minimal match instruction.
                #   * `not literal_length`, which is only part of the second formula,
                #     improves the first estimation.
                #     If `literal_length == 0`, we will subtract 1, which erases the
                #     `+ 1` part as a literal of length 0 would not have to be written.
                #     If `literal_length > 0`, `not literal_length` will be 0 and we
                #     therefore will not subtract anything. We have to use 1 byte for
                #     encoding the literal length (the `+ 1` part) and `literal_length`
                #     bytes for writing the actual literal bytes.
                # Please note that these explanations are just my own assumptions - they
                # might be false as well, but at least they make sense from a logical
                # point of view.
                if destination_position + literal_length + 3 + 1 >= destination_end:
                    # `!lit` - as it is used in the original C implementation - is a
                    # little bit tricky. Python does not understand this directly, so
                    # we have to convert the boolean result to an integer.
                    # We could provide an own implementation of this as well, as it
                    # corresponds to
                    #   1 if literal_length == 0 else 0
                    # The C# version omits this construct completely by boiling down the
                    # two conditions into one, while it calculates one byte too much by
                    # not subtracting `!lit` in the condition. If the literal length is
                    # zero, it still assumes that it needs one byte to write the
                    # literal instruction, while it is clear that each literal
                    # instruction requires at least two bytes when actually written (one
                    # byte for the literal length of 1, encoded as the byte `0`, and one
                    # byte for the literal byte itself).
                    not_literal_length = int(not literal_length)
                    if (
                            destination_position
                            - not_literal_length
                            + 1
                            + literal_length
                            + 3
                            >= destination_end
                    ):
                        return None

                # This is the end of the current literal instruction, a match
                # instruction will start afterwards. So write the literal instruction
                # if needed.
                bytes_written = self._emit_literal_instruction(
                    source, destination, source_position, literal_length
                )
                destination_position += bytes_written

                # Determine the match length.
                while True:
                    match_length += 1

                    # Use 2 separate conditions to improve readability.
                    if match_length >= match_length_max:
                        break
                    if (
                            source[referenced_position + match_length]
                            != source[source_position + match_length]
                    ):
                        break

                # A match of the minimal length 3 will be encoded using the value `1`,
                # so we have to subtract 2. The encoded value `0` represents a literal
                # instruction.
                match_length -= 2

                # Make sure that the match length is at least 1.
                # If the match length would be 0 here, the instruction would be
                # interpreted as a literal one instead of a match during decompression.
                # A match length of 3 should be `1` here, a match length of 4 should be
                # `2` here and so on.
                assert match_length >= 1

                # Move to the next input position.
                # This has to be seen in combination with the line above and
                # `source_position += match_length + 1`.
                # In the line above we have a match length which is actually reduced by
                # one (this is what we encode as length 0 is not possible). With
                # `match_length + 1` we basically revert this for the input position
                # change. Here we have to add another 1 as the next match will start
                # after the current match, but without this statement would point to
                # the end of the match inside the source buffer (look-ahead buffer).
                # To make this more clear, this might have been better below at the
                # actual window shift, but let us keep it as similar to the original C
                # version as possible.
                source_position += 1

                # Perform the encoding itself.
                # This will write all bytes except of the last byte with the second
                # part of the offset as this is common to all.
                if match_length < 7:
                    # This is a short match using 2 bytes.
                    # Format: LLLooooo oooooooo
                    #         LLL = length 3-8 with values 1-6 (actual length - 2).
                    #         ooooo oooooooo = offset using 13 bits.

                    # This will write the first byte only.
                    # Format: the length using 3 bits (2^3 = 8), then the 5 most
                    #         significant bits of the offset (the offset will have 13
                    #         bits, so we remove the last byte with the shift).
                    value = (match_length << 5) + (offset >> 8)
                    destination.append(value)

                    # Move to the next output position.
                    destination_position += 1
                else:
                    # This is a long match using 3 bytes.
                    # Format: 111ooooo LLLLLLLL oooooooo
                    #         111 = 0x7 = indicator for a long reference.
                    #         ooooo = 5 most significant bits of the offset.
                    #         LLLLLLLL = lengths 9-264 with values 0-255
                    #                    (actual length - 9).
                    #         oooooooo = 8 least significant bits of the offset.

                    # This will write the first 2 bytes only.

                    # Write the first byte.
                    # Format: indicator 0x7 3 bits, then the 5 most significant bits of
                    #         the offset (the offset will have 13 bits, so we remove the
                    #         last byte with the shift).
                    value = (7 << 5) + (offset >> 8)
                    destination.append(value)

                    # Write the second byte.
                    # Just write the length value using 1 byte.
                    # We are subtracting 7 from this length value as we know that this
                    # length cannot be smaller - otherwise we would have chosen a short
                    # match instruction instead of the long match instruction.
                    destination.append(match_length - 7)

                    # We have written 2 bytes.
                    destination_position += 2

                # Write the last byte of the offset, then move to the next output
                # position.
                destination.append(utils.get_last_bytes(offset, 1))
                destination_position += 1

                # Reset the literal length as we just had a match instruction and wrote
                # the literal instruction beforehand.
                literal_length = 0

                # Move the input forward based on the match length.
                source_position += match_length + 1

                # Stop the loop if the input is nearly exhausted.
                # The "- 2" is due to the match length requiring at least 3 bytes.
                if source_position >= (source_length - 2):
                    break

                # Handle hash table updates.
                if mode == LzfMode.ULTRA_FAST or mode == LzfMode.VERY_FAST:
                    # The faster modes only perform some updates.

                    # Move to the previous input position.
                    source_position -= 1

                    if mode == LzfMode.VERY_FAST:
                        # If we are not in the fastest mode, go back another byte.
                        source_position -= 1

                    # Save the current entry inside the hash table.
                    hash_value = self._get_first_two_bytes_as_integer(
                        source, source_position
                    )
                    hash_value = self._concatenate_value_with_third_byte(
                        hash_value, source, source_position
                    )
                    hash_slot = self._hash(hash_value, mode)
                    hash_table[hash_slot] = source_position

                    # Move to the next input position.
                    source_position += 1

                    if mode == LzfMode.VERY_FAST:
                        # If we are not in the fastest mode, add the next entry as well.
                        hash_value = self._concatenate_value_with_third_byte(
                            hash_value, source, source_position
                        )
                        hash_slot = self._hash(hash_value, mode)
                        hash_table[hash_slot] = source_position

                        # Move to the next input position.
                        source_position += 1
                else:
                    # This is the slowest mode where we add all seen byte groups to the
                    # hash table.

                    # Go back to the start of the match.
                    source_position -= match_length + 1

                    # Move through the input byte by byte and update the hash table
                    # accordingly. This is slow, but leads to the best compression
                    # ratio.
                    for _ in range(match_length + 1):
                        hash_value = self._concatenate_value_with_third_byte(
                            hash_value, source, source_position
                        )
                        hash_slot = self._hash(hash_value, mode)
                        hash_table[hash_slot] = source_position
                        source_position += 1

            else:
                # There is no match, so we have a literal instruction.

                # Stop if we have reached the requested output size.
                if destination_position >= destination_end:
                    return None

                # Increase the literal length and move to the next input position.
                literal_length += 1
                source_position += 1

                # Write the literal instruction if we have reached the maximum length.
                if literal_length == self.configuration.LITERAL_MAX:
                    bytes_written = self._emit_literal_instruction(
                        source, destination, source_position, literal_length
                    )
                    destination_position += bytes_written
                    literal_length = 0

        # Handle the remaining input.
        while source_position < source_length:
            # We cannot have a match instruction anymore as we would not have exited the
            # loop otherwise.
            # So increase the literal length and move to the next input position.
            literal_length += 1
            source_position += 1

            # Write the literal instruction if we have reached the maximum length.
            if literal_length == self.configuration.LITERAL_MAX:
                bytes_written = self._emit_literal_instruction(
                    source, destination, source_position, literal_length
                )
                destination_position += bytes_written
                literal_length = 0

        # If we have some remaining bytes to write, emit them as a literal instruction.
        bytes_written = self._emit_literal_instruction(
            source, destination, source_position, literal_length
        )
        destination_position += bytes_written

        # Return the destination buffer.
        return destination

    @staticmethod
    def _emit_literal_instruction(
            source, destination, source_start_position, literal_length
    ):
        """
        Emit the a literal instruction with the given length. If the literal length is
        zero, no instruction will be emitted.

        :param source: The source buffer to retrieve the literal bytes from.
        :type source: bytearray

        :param destination: The destination buffer to write the literal instruction to.
        :type destination: bytearray

        :param source_start_position: The position to start at inside the source buffer.
        :type source_start_position: int

        :param literal_length: The length of the literal to emit.
        :type literal_length: int

        :return: The number of bytes written to the destination buffer.
        :rtype: int
        """
        # If the literal length is zero, no literal has to be emitted.
        if literal_length == 0:
            return 0

        # Add the literal length to the output buffer.
        destination.append(literal_length - 1)

        # Write the literal bytes one at a time.
        offset = -literal_length
        while offset < 0:
            destination.append(source[source_start_position + offset])
            offset += 1

        # We always have one byte for the literal length and `literal_length` bytes for
        # the bytes itself.
        return 1 + literal_length

    @staticmethod
    def _get_first_two_bytes_as_integer(buffer, start_position):
        """
        Get the first two bytes of the buffer starting at the given position as an
        integer value.

        This method corresponds to the `FRST` macro of the C implementation.

        :param buffer: The buffer to get the values from.
        :type buffer: bytearray

        :param start_position: The position to start at.
        :type start_position: int

        :return: The integer value created from the first two bytes of the buffer when
                 starting at the given position.
        :rtype: int
        """
        return (buffer[start_position] << 8) | buffer[start_position + 1]

    @staticmethod
    def _concatenate_value_with_third_byte(value, buffer, start_position):
        """
        Concatenate the given value with the third byte of the buffer starting at the
        given position as an integer value.

        This method corresponds to the `NEXT` macro of the C implementation.

        :param value: The value to concatenate the third byte with.
        :type value: int

        :param buffer: The buffer to get the values from.
        :type buffer: bytearray

        :param start_position: The position to start at.
        :type start_position: int

        :return: The integer value created by concatenating the given value with the
                 third byte of the buffer when starting at the given position.
        :rtype: int
        """
        # Concatenate the values itself.
        new_value = (value << 8) | buffer[start_position + 2]

        # If we would return the value from the previous line, the value would grow
        # unlimited theoretically. The C implementation uses an `unsigned int` with
        # `sizeof(unsigned int) = 4`, id est it is restricted to 4 bytes. So we are
        # keeping the last (least significant) 32 bits = 4 bytes here only.
        new_value = utils.get_last_bytes(new_value, 4)

        return new_value

    def _hash(self, hash_value, mode):
        """
        Get the index for the hash value, while taking the selected mode into account.

        This method corresponds to the `IDX` macro of the C implementation. Quoting the
        author about the general hash calculations: "the hash function might seem
        strange, just believe me, it works".

        :param hash_value: The hash value to get the index for.
        :type hash_value: int

        :param mode: The LZF mode which influences the actual index calculation formula
                     (and with this the calculation speed).
        :type mode: int

        :return: The index for the given hash value while considering the given working
                 mode.
        :rtype: int
        """
        # Retrieve the configuration value for convenience.
        hash_log = self.configuration.HASH_TABLE_LOGARITHM

        # Choose the calculation formula depending on the working mode.
        # The formula will generally be easier if the speed should be increased.
        if mode == LzfMode.ULTRA_FAST:
            index = (hash_value >> (3 * 8 - hash_log)) - hash_value
        elif mode == LzfMode.VERY_FAST:
            index = (hash_value >> (3 * 8 - hash_log)) - hash_value * 5
        else:
            index = (
                            (hash_value ^ (hash_value << 5)) >> (3 * 8 - hash_log)
                    ) - hash_value * 5

        # AND-ing with `HASH_TABLE_SIZE - 1` only keeps the last
        # `log2(HASH_TABLE_SIZE - 1)` bits of the index and ensures that the index is in
        # the correct range.
        return index & (self.configuration.HASH_TABLE_SIZE - 1)


class FileCompressor:
    """
    The implementation of the (file) compressor.
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

    def compress(
            self, source, mode=LzfMode.VERY_FAST, block_size=Constants.BLOCK_SIZE_MAX
    ):
        """
        Compress the given source buffer using the LZF algorithm.

        :param source: The source buffer to compress.
        :type source: bytearray

        :param mode: The LZF mode to use.
        :type mode: `int`

        :param block_size: The block size to use.
        :type block_size: `int`

        :return: The compression result.
        :rtype: bytearray
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer.
        destination = bytearray()

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Retrieve the current block.
            block = source[source_position: source_position + block_size]
            # Determine the actual size of the current block (<= block_size).
            current_block_size = len(block)

            # Determine the maximum output length to determine whether the output is
            # compressible or not.
            maximum_output_length = (
                current_block_size - 4 if current_block_size > 4 else current_block_size
            )

            # Compress the current block.
            block_compressed = Compressor(self.configuration).compress(
                block, 0, maximum_output_length, mode
            )

            # The compression result is `None` if the maximum output length would have
            # been exceeded, so if the result is `None` the original block data has to
            # be written.
            is_compressed = block_compressed is not None

            # Prepare the header as an own byte array.
            header = bytearray()

            # Write the archive type identifier.
            header.append(ord("Z"))
            header.append(ord("V"))

            if is_compressed:
                # We were able to compress the data, so use header type 1 with 7 bytes.

                # Write the compression type (1 = compressed chunk).
                header.append(1)

                # Write the chunk size (compressed length) using 2 bytes.
                compressed_size = len(block_compressed)
                header.append(utils.get_last_bytes(compressed_size >> 8, 1))
                header.append(compressed_size & 0xFF)

                # Write the original size (uncompressed length) using 2 bytes.
                header.append(utils.get_last_bytes(current_block_size >> 8, 1))
                header.append(current_block_size & 0xFF)

                # Add the header and the compressed data buffer to the output buffer.
                destination += header
                destination += block_compressed
            else:
                # We were not able to compress the data, so user header type 0 with 5
                # bytes.

                # Write the compression type (0 = uncompressed chunk).
                header.append(0)

                # Write the original size (uncompressed length) using 2 bytes.
                header.append(utils.get_last_bytes(current_block_size >> 8, 1))
                header.append(current_block_size & 0xFF)

                # Add the header buffer and the current chunk to the output buffer.
                destination += header
                destination += block

            # Move to the next block.
            source_position += block_size

        # Return the destination buffer.
        return destination
